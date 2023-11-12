from DataBase import *
from Items import *
import Connection

with db:
    db.create_tables([User])

def get_user_data(user):
    request = f'\nUser coins: {user.coins}\n'
    user_items = user.get_items().items()
    if len(user_items) == 0:
        request += f'|Inventory is empty|\n'
        return request

    request = request + f'User items:\n'
    for id, count in user_items:
        item = find_item_by_id(id)
        request += f'           |{item["data"]["type"]} \"{item["data"]["name"]}\"\n'
        request += f'           |Item ID  : {id}\n'
        if item["is_stackable"]:
            request += f'           |Count    : {count}\n'
        request += f'           |Price    : {item["data"]["price"]}\n'
        request += '           ______________________________\n'
    return request

def print_users_data_base(): # debug only
    for user in User.select():
        print('_________________________________________')
        print(f'\nUser name : {user.nickname}')
        show_user_data(user)
        print('_________________________________________')


def add_user_login_reward(user):
    login_reward = random.randint(1000, 3000)
    change_coins_count(user, login_reward)

def login(nickname):
    user = find_user_by_nickname(nickname)
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
    add_user_login_reward(user)
    return_code = b'success_return_code'
    Connection.get_client_socket().send(return_code)
    return True

def player_have_item(user, item_id):
    user_items = user.get_items()
    try:
        item = user_items[f'{item_id}']
        return True
    except KeyError:
        return False

def player_have_enought_money(user, item):
    price = item['data']['price']
    return user.get_coins() >= price


def check_buy_operation(user, item_id):
    item = find_item_by_id(item_id)
    if item == None:
        return "There is no such item"
    if not player_have_enought_money(user, item):
        return "You have no enought money"
    if player_have_item(user, item_id) and not item["is_stackable"]:
        return "You have this unstackable item already"
    return "Success"

def buy_item_by_id(user, item_id):
    item = find_item_by_id(item_id)
    price = item['data']['price']
    change_coins_count(user, -price)
    add_new_item_to_user(user, item_id)

def sell_item_by_id(item_id):
    pass