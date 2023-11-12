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

    def send_items_list(self):
        items_list = ServerModule.get_items_list()
        ServerModule.Connection.get_client_socket().sendall(items_list.encode('utf-8'))
        print('List has been sent')
        ServerModule.Connection.get_client_socket().sendall('stop_code'.encode('utf-8'))
        self.choose_state()

    def show_items_list(self):
        self.choose_state()
        
    def check_client_item_id(self):
        message = ServerModule.Connection.recive_message()
        if message.upper() == 'BC':
            self.current_state = 'welcome'
            return
        return int(message)

    def trade(self, type):
        item_id = self.check_client_item_id()
        if not item_id:
            return
        user = ServerModule.find_user_by_nickname(self.nickname)
        if type == 'sell':
            return_code = ServerModule.sell_item_by_id(user, item_id)
        else:
            return_code = ServerModule.check_buy_operation(user, item_id)
            if return_code == 'Success':
                ServerModule.buy_item_by_id(user, item_id)
        ServerModule.Connection.send_message(return_code)

    def welcome(self):
        self.choose_state()
        
    def choose_state(self):
        self.current_state = ServerModule.Connection.recive_message()

