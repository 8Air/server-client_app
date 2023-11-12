import ServerModule

class StateMachine():
    current_state = None
    nickname = None
    def __init__(self, start_state):
        self.current_state = start_state

    def login(self):
        self.nickname = ServerModule.Connection.recive_message()
        return ServerModule.login(self.nickname)

    def view_profile(self):
        user = ServerModule.find_user_by_nickname(self.nickname)
        message = ServerModule.get_user_data(user)
        ServerModule.Connection.send_message(message)
        self.choose_state()

    def sell_item(self, item_id):
        user = ServerModule.find_user_by_nickname(self.nickname)
        ServerModule.get_user_data(user)
        ServerModule.sell_item_by_id(input('Press item id\n'))

    def send_items_list(self):
        items_list = ServerModule.get_items_list()
        ServerModule.Connection.get_client_socket().sendall(items_list.encode('utf-8'))
        print('List has been sent')
        ServerModule.Connection.get_client_socket().sendall('stop_code'.encode('utf-8'))
        self.choose_state()

    def show_items_list(self):
        self.choose_state()

    def buy_item(self):
        message = ServerModule.Connection.recive_message()
        if message.upper() == 'CL':
            self.current_state = 'welcome'
            return
        item_id = int(message)
        user = ServerModule.find_user_by_nickname(self.nickname)
        return_code = ServerModule.check_buy_operation(user, item_id)
        if return_code == 'Success':
            ServerModule.buy_item_by_id(user, item_id)
        ServerModule.Connection.send_message(return_code)

    def welcome(self):
        self.choose_state()
        
    def choose_state(self):
        self.current_state = ServerModule.Connection.recive_message()

