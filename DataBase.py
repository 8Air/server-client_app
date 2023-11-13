from peewee import *
import json
import random

db = SqliteDatabase('db/DataBase.db')

class User(Model):
    nickname = CharField()
    coins    = IntegerField()
    items    = TextField()

    def set_items(self, items_dict):
        self.items = json.dumps(items_dict)

    def get_items(self):
        return json.loads(self.items)

    def get_coins(self):
        return self.coins

    def change_coins_count(self, coins_count: int):
        self.coins = self.coins + coins_count
        self.save()

    class Meta:
        database = db
        db_table = "users"

def add_new_user(nickname: str):
    start_coins = 500
    User(nickname=nickname, coins=start_coins, items=json.dumps({})).save()
    return find_user_by_nickname(nickname)

def find_user_by_nickname(nickname: str):
     try:
        return User.get(User.nickname == nickname)
     except User.DoesNotExist:
         pass

def add_item_to_user(user: User, item_id: int):
    user_items = user.get_items()
    try:
        item_count = int(user_items[f'{item_id}']) + 1
        user_items[f'{item_id}'] = f'{item_count}'
    except KeyError:
        user_items[f'{item_id}'] = '1'
    user.set_items(user_items)
    user.save()

def decrease_item_count(user: User, item_id: int):
    user_items: set = user.get_items()
    item_count: int = int(user_items[f'{item_id}']) - 1
    if item_count == 0:
        del user_items[f'{item_id}']
    else:
        user_items[f'{item_id}'] = f'{item_count}'
    user.set_items(user_items)
    user.save()

def add_user_login_reward(user: User):
    login_reward: int = random.randint(1000, 3000)
    user.change_coins_count(login_reward)