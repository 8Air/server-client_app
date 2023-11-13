import json

with open('db/items.json') as items_json:
    data = json.load(items_json)

def get_item_info(item):
    item_info = f"""ID..........{item['id']}
Type........{item['data']['type']}
Name........{item['data']['name']}
Price.......{item['data']['price']}
Description:\n{item['data']['description']}""".strip()
    return item_info

def get_items_list():
    items_list = ''
    for item in data:
        items_list += f"""______________________________________________
{get_item_info(item)}
______________________________________________\n"""
    return items_list
        

def find_item_by_id(id: int):
    for item in data:
        if item['id'] == int(id):
            return item
    return None

def get_item_price(item_id: int):
    item = find_item_by_id(item_id)
    return item['data']['price']