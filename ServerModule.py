from DataBase import *
from Items import *

with db:
    db.create_tables([User])

def show_user_data(user_or_nickname):
    if type(user_or_nickname) == str:
       user = find_user_by_nickname(user_or_nickname)
    else:
        user = user_or_nickname
    print(f'User coins: {user.coins}')
    user_items = user.get_items().items()
    if len(user_items) == 0:
        print(f'|Inventory is empty|')
        return

    print(f'User items:')
    for id, count in user_items:
        item = find_item_by_id(id)
        print(f'           |{item["data"]["type"]} \"{item["data"]["name"]}\"')
        print(f'           |Item ID  : {id}')
        if item["is_storable"]:
            print(f'           |Count    : {count}')
        print(f'           |Price    : {item["data"]["price"]}')
        print('           ______________________________')

def print_data_base():
    for user in User.select():
        print('_________________________________________')
        print(f'\nUser name : {user.nickname}')
        show_user_data(user)
        print('_________________________________________')

def add_user_login_reward(user_or_nickname):
    if type(user_or_nickname) == str:
       user = find_user_by_nickname(user_or_nickname)
    else:
        user = user_or_nickname
    login_reward = random.randint(1000, 3000)
    change_coins_count(user, login_reward)

def login(nickname):
    user = find_user_by_nickname(nickname)
    if user == None:
        print('There is no user with nickname {nickname}.')
        create_user = input(f'Do you want to create a new accaunt? [Y/N]\n').upper()
        if create_user == 'Y':
            user = add_new_user(nickname)
        else:
            return False
    add_user_login_reward(user)
    return True

def sell_item_by_id(item_id):
    pass