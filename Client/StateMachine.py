import Connection

class StateMachine():
    current_state = None
    nickname = None
    def __init__(self, start_state):
        self.current_state = start_state

    def login(self, nickname):
        self.nickname = nickname
        Connection.send_message(nickname)
        return_code = Connection.get_client_socket().recv(1024)
        if return_code == b'no_user_return_code':
            message = f'''There is no user with nickname {nickname}.
Do you want to create a new accaunt? [Y/N]\n'''
            answer = input(message).upper()
            Connection.send_message(answer)
            if answer == 'Y':
                return_code = Connection.get_client_socket().recv(1024)
            else:
                state = 'leave_or_stay'
                return state
        elif return_code == b'create_error_return_code':
            print("Account creating error")
            state = 'leave_or_stay'
            return state
        state = 'welcome'
        return state

    def leave_or_stay(self):
        states = [['C','login', 'continue'], 
                  ['E', 'logout', 'exit']]
        self.choose_state(states)

    def view_profile(self):
        profile = Connection.recive_message()
        print(profile)
        states = [['BC','welcome', 'go back'], 
                  ['SL', 'sell_item', 'sell item']]
        self.choose_state(states)

    def sell_item(self, item_id):
        pass

    def get_items_list(self):
        Connection.sendall_message(self.current_state)
        received_data = ""
        stop_code = "stop_code"
        while True:
            chunk = Connection.recive_message()
            if chunk == stop_code:
                break
            received_data += chunk
        self.current_state = 'show_items_list'
        Connection.send_message(self.current_state)
        return received_data
        

    def show_items_list(self, items_list):
        print(items_list)
        states = [['BC','welcome', 'go back'], 
                  ['BY', 'buy_item', 'buy item']]
        self.choose_state(states)

    def buy_item(self):
        string = input("Enter item id (or CL to return)\n")
        if string.upper() == 'CL':
            self.current_state = 'welcome'
            Connection.send_message(string)
            return
        try:
            item_id = int(string)
            Connection.send_message(string)
        except ValueError:
            print("Wrong id format. Try again.")

        
    def welcome(self):
        print(f'\nNice to see you {self.nickname}!\nWhat do you wanna do?\n')
        states = [['IN', 'view_profile', 'show inventory'], 
                  ['IT', 'show_items_list', 'show items list'], 
                  ['LO','leave_or_stay', 'logout']]
        self.choose_state(states)
        
    def choose_state(self, states):
        state_has_been_changed = False
        for state in states:
             print(f"Press '{state[0]}' to {state[2]}")
        state_key = input().upper()
        for state in states:
            if state_key == state[0]:
                self.current_state = state[1]
                Connection.send_message(state[1])
                state_has_been_changed = True

        if not state_has_been_changed:
            print('Something went wrong. Try again.')
            self.choose_state(states)

