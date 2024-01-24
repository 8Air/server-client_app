from DataBase import *
import Items
import Connection

with db:
    db.create_tables([User])

def make_item_list(user_items: set):
    item_list: str = ''
    for id, count in user_items:  
        item = Items.find_item_by_id(id)
        item_list += f'           |{item["data"]["type"]} \"{item["data"]["name"]}\"\n'
        item_list += f'           |Item ID  : {id}\n'
        if item["is_stackable"]:
            item_list += f'           |Count    : {count}\n'
        item_list += f'           |Price    : {item["data"]["price"]}\n'
        item_list += '           ______________________________\n'
    return item_list

def get_user_data(user: User):
    request: str = f'\nUser coins: {user.coins}\n'
    user_items: set = user.get_items().items()
    if len(user_items) == 0:
        request += f'|Inventory is empty|\n'
        return request
    request += f'User items:\n'
    request += make_item_list(user_items)
    return request

def send_user_profile_data(nickname: str):
    user: User = find_user_by_nickname(nickname)
    message: str = get_user_data(user)
    Connection.send_utf_message(message)

def send_items_list():
    items_list = Items.get_items_list()
    Connection.send_items_list(items_list) 

def trade(nickname: str, type: str):
    message = Connection.receive_utf_message()
    if message.upper() == 'BC':
        return False
    item_id = int(message)
    if item_id:
        user = find_user_by_nickname(nickname)
        if type == 'sell':
            return_code = sell_item_by_id(user, item_id)
        else:
            return_code = check_buy_operation(user, item_id)
            if return_code == 'Success':
                buy_item_by_id(user, item_id)
    Connection.send_utf_message(return_code)
    return True

def create_new_user(nickname: str):
    user = add_new_user(nickname)
    if not user:
        return_code: bytes = Connection.ReturnCode.CREATE_ERROR.value
        Connection.send_byte_message(return_code)
        return None
    return user

def check_user_exist(nickname: str):
    user = find_user_by_nickname(nickname)
    if user == None:
        return_code: bytes = Connection.ReturnCode.NO_USER.value
        Connection.send_byte_message(return_code)
        return None
    return user

def login():
    nickname: str = Connection.receive_utf_message()
    user: User = check_user_exist(nickname)
    if not user:
        if not Connection.create_check():
            return None
        user: User = create_new_user(nickname)
    add_user_login_reward(user)
    return_code: bytes = Connection.ReturnCode.SUCCESS.value
    Connection.send_byte_message(return_code)
    return nickname

def user_have_item(user: User, item_id: int):
    user_items: set = user.get_items()
    try:
        item: str = user_items[f'{item_id}']
        return True
    except KeyError:
        return False

def user_have_enought_money(user: User, item: str):
    price: int = int(item['data']['price'])
    return user.get_coins() >= price

def check_buy_operation(user: User, item_id: int):
    item = Items.find_item_by_id(item_id)
    if item == None:
        return "There is no such item"
    if not user_have_enought_money(user, item):
        return "You have no enought money"
    if user_have_item(user, item_id) and not item["is_stackable"]:
        return "You have this unstackable item already"
    return "Success"

def buy_item_by_id(user: User, item_id: int):
    buy_price: int = Items.get_item_price(item_id)
    user.change_coins_count(- buy_price)
    add_item_to_user(user, item_id)

def sell_item_by_id(user: User, item_id: int):
     if not user_have_item(user, item_id):
         return "Error: you have no item with such ID"
     sell_price: int = Items.get_item_price(item_id)
     user.change_coins_count(sell_price)
     decrease_item_count(user, item_id)
     return "Success"