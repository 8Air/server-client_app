from enum import Enum

class State(Enum):
    LEAVE       = 'leave_or_stay'
    LOGIN       = 'login'
    WELCOME     = 'welcome'
    PROFILE     = 'view_profile'
    SHOW_ITEMS  = 'show_items_list'
    GET_ITEMS   = 'get_items_list'
    BUY_ITEM    = 'buy_item'
    SELL_ITEM   = 'sell_item'
    LOGOUT      = 'logout'

class StateDescription(Enum):
                   #key        value            user message
    BACK        = ['BC', State.WELCOME.value,   'go back']
    BUY         = ['BY', State.BUY_ITEM.value,  'buy item']
    SELL        = ['SL', State.SELL_ITEM.value, 'sell item']
    CONTINUE    = ['C',  State.LOGIN.value,     'continue']
    EXIT        = ['E',  State.LOGOUT.value,    'exit']
    INVENTORY   = ['IN', State.PROFILE.value,   'show inventory']
    ITEMS_LIST  = ['IT', State.SHOW_ITEMS.value,'see items list']
    LEAVE       = ['LO', State.LEAVE.value,     'logout']
