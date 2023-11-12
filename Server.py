from StateMachine import *

sm = StateMachine('login')

try:
    ServerModule.Connection.start_server()
    client_address = ServerModule.Connection.get_client_address()
    print(f"Connection from {client_address}")

    while sm.current_state != 'logout':
        if sm.current_state == 'leave_or_stay':
            sm.choose_state()
        elif sm.current_state == 'login':
            if sm.login():
                sm.current_state = 'welcome'
            else:
                sm.current_state = 'leave_or_stay'
        elif sm.current_state == 'welcome':
            sm.welcome()
        elif sm.current_state == 'view_profile':
            sm.view_profile()
        elif sm.current_state == 'show_items_list':
            sm.show_items_list()
        elif sm.current_state == 'get_items_list':
            items_list = sm.send_items_list()
        elif sm.current_state == 'buy_item':
            sm.trade('buy')
        elif sm.current_state == 'sell_item':
            sm.trade('sell')
        else:
            print("State error: there is no such state or state is empty")
            break


    ServerModule.Connection.get_client_socket().close()
except ConnectionResetError:
    print("Connection has been broken.")
finally:
    ServerModule.Connection.get_server_socket().close()