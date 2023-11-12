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

    class Meta:
        database = db
        db_table = "users"

def add_new_user(nickname):
    start_coins = 500
    User(nickname=nickname, coins=start_coins, items=json.dumps({})).save()
    return find_user_by_nickname(nickname)

def find_user_by_nickname(nickname):
     try:
        return User.get(User.nickname == nickname)
     except User.DoesNotExist:
         pass

def change_coins_count(user, coins_count):
    user.coins = user.coins + coins_count
    user.save()

def add_new_item_to_user(user, item_id):
    user_items = user.get_items()
    try:
        item_count = int(user_items[f'{item_id}']) + 1
        user_items[f'{item_id}'] = f'{item_count}'
    except KeyError:
        user_items[f'{item_id}'] = '1'
    user.set_items(user_items)
    user.save()
    print(user_items)

def remove_item_from_user_inventory(user, item_id):
    pass