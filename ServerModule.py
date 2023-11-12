from DataBase import *
from Items import *
import Connection

with db:
    db.create_tables([User])

def make_item_list(user_items):
    item_list = ''
    for id, count in user_items:  
        item = find_item_by_id(id)
        item_list += f'           |{item["data"]["type"]} \"{item["data"]["name"]}\"\n'
        item_list += f'           |Item ID  : {id}\n'
        if item["is_stackable"]:
            item_list += f'           |Count    : {count}\n'
        item_list += f'           |Price    : {item["data"]["price"]}\n'
        item_list += '           ______________________________\n'
    return item_list

def get_user_data(user):
    request = f'\nUser coins: {user.coins}\n'
    user_items = user.get_items().items()
    if len(user_items) == 0:
        request += f'|Inventory is empty|\n'
        return request
    request = request + f'User items:\n'
    request = request + make_item_list(user_items)
    return request

def add_user_login_reward(user):
    login_reward = random.randint(1000, 3000)
    change_coins_count(user, login_reward)

def check_user_exist(user):
    if user == None:
        return_code = b'no_user_return_code'
        Connection.get_client_socket().send(return_code)
        answer = Connection.recive_message()
        if answer == 'Y':
            user = add_new_user(nickname)
            if not user:
                return_code = b'create_error_return_code'
                Connection.get_client_socket().send(return_code)
                return False
                
        else:
            return False
    return True

def login(nickname):
    user = find_user_by_nickname(nickname)
    if not check_user_exist(user):
        return False
    add_user_login_reward(user)
    return_code = b'success_return_code'
    Connection.get_client_socket().send(return_code)
    return True

def user_have_item(user, item_id):
    user_items = user.get_items()
    try:
        item = user_items[f'{item_id}']
        return True
    except KeyError:
        return False

def user_have_enought_money(user, item):
    price = item['data']['price']
    return user.get_coins() >= price


def check_buy_operation(user, item_id):
    item = find_item_by_id(item_id)
    if item == None:
        return "There is no such item"
    if not user_have_enought_money(user, item):
        return "You have no enought money"
    if user_have_item(user, item_id) and not item["is_stackable"]:
        return "You have this unstackable item already"
    return "Success"

def get_item_price(item_id):
    item = find_item_by_id(item_id)
    return item['data']['price']

def buy_item_by_id(user, item_id):
    buy_price = -get_item_price(item_id)
    change_coins_count(user, buy_price)
    add_item_to_user(user, item_id)

def sell_item_by_id(user, item_id):
     if not user_have_item(user, item_id):
         return "Error: you have no item with such ID"
     sell_price = get_item_price(item_id)
     change_coins_count(user, sell_price)
     decrease_item_count(user, item_id)
     return "Success"
