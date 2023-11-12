from StateMachine import *

sm = StateMachine('login')
items_list = None

try:
    Connection.connect_to_server()

    while sm.current_state != 'logout':
        if sm.current_state == 'leave_or_stay':
            sm.leave_or_stay()
        elif sm.current_state == 'login':
            sm.current_state = sm.login(input("Enter nickname: "))
        elif sm.current_state == 'welcome':
            sm.welcome()
        elif sm.current_state == 'view_profile':
            sm.view_profile()
        elif sm.current_state == 'show_items_list':
            if items_list == None:
                sm.current_state = 'get_items_list'
            else:
                sm.show_items_list(items_list)
        elif sm.current_state == 'get_items_list':
            items_list = sm.get_items_list()
            if items_list:
                sm.current_state = 'show_items_list'
        elif sm.current_state == 'buy_item':
            sm.trade()
        elif sm.current_state == 'sell_item':
            sm.trade()
        else:
            print("State error: there is no such state or state is empty")
            break


except ConnectionRefusedError:
    print("Connection failed.")
finally:
     Connection.get_client_socket().close()