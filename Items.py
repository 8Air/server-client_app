
import json

with open('db/items.json') as items_json:
    data = json.load(items_json)

def show_item_info(item):
    print(f"Type........{item['data']['type']}")
    print(f"Name........{item['data']['name']}")
    print(f"Price.......{item['data']['price']}")
    print(f"Description:\n{item['data']['description']}")

def show_items_list():
    for item in data:
        print(f"______________________________________________")
        show_item_info(item)
        print(f"______________________________________________")
        

def find_item_by_id(id):
    for item in data:
        if item['id'] == int(id):
            return item