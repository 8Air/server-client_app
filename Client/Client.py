import ClientModule
from StatesEnum import *

items_list = None

class StateMachine():
    current_state: State = None
    nickname: str = None

    def __init__(self, start_state):
        self.current_state = start_state

    def set_state(self, state: str):
        self.current_state = state

    def get_state(self):
        return self.current_state

    def login(self):
        enter_string = "Enter nickname: "
        self.nickname: str = input(enter_string)
        if ClientModule.check_login_success(self.nickname):
            state = State.WELCOME.value
        else:
            state = State.LEAVE.value
        return state

    def leave_or_stay(self):
        states = [StateDescription.CONTINUE.value, 
                  StateDescription.EXIT.value]
        self.choose_state(states)

    def view_profile(self):
        profile = ClientModule.Connection.receive_utf_message()
        print(profile)
        states = [StateDescription.BACK.value, 
                  StateDescription.SELL.value]
        self.choose_state(states)

    def get_items_list(self):
        ClientModule.Connection.send_utf_message(self.get_state())
        received_data = ClientModule.receive_items_data()
        self.set_state(State.SHOW_ITEMS.value)
        ClientModule.Connection.send_utf_message(State.SHOW_ITEMS.value)
        return received_data     

    def show_items_list(self, items_list):
        print(items_list)
        states = [StateDescription.BACK.value, 
                  StateDescription.BUY.value]
        self.choose_state(states)

    def trade(self):
        ask_id_message = "Enter item id (or BC to return)\n"
        string = input(ask_id_message)
        if string.upper() == StateDescription.BACK.value[0]:
            self.set_state(StateDescription.BACK.value[1])
            ClientModule.Connection.send_utf_message(string)
            return
        try:
            item_id = int(string)
            ClientModule.Connection.send_utf_message(string)
            return_code = ClientModule.Connection.receive_utf_message()
            print(f"{return_code}")
        except ValueError:
            id_error = "Wrong id format. Try again."
            print(id_error)
     
    def welcome(self):
        welcome_message = f'\nNice to see you {self.nickname}!\nWhat do you wanna do?\n'
        print(welcome_message)
        states = [StateDescription.INVENTORY.value, 
                  StateDescription.ITEMS_LIST.value,
                  StateDescription.LEAVE.value]
        self.choose_state(states)

    def choose_state(self, states):
        state_has_been_changed = False
        for state in states:
             print(f"Press '{state[0]}' to {state[2]}")
        state_key = input().upper()
        for state in states:
            if state_key == state[0]:
                self.set_state(state[1])
                ClientModule.Connection.send_utf_message(state[1])
                state_has_been_changed = True
        if not state_has_been_changed:
            print('Something went wrong. Try again.')
            self.choose_state(states)

sm = StateMachine(State.LOGIN.value)

try:
    ClientModule.Connection.connect_to_server()

    while sm.get_state() != State.LOGOUT.value:
        state: str = sm.get_state()

        if state == State.LEAVE.value:
            sm.leave_or_stay()

        elif state == State.LOGIN.value:
            sm.set_state(sm.login())

        elif state == State.WELCOME.value:
            sm.welcome()

        elif state == State.PROFILE.value:
            sm.view_profile()

        elif state == State.SHOW_ITEMS.value:
            if items_list == None:
                sm.set_state(State.GET_ITEMS.value)
            else:
                sm.show_items_list(items_list)

        elif state == State.GET_ITEMS.value:
            items_list = sm.get_items_list()
            if items_list:
                sm.set_state(State.SHOW_ITEMS.value)

        elif state == State.BUY_ITEM.value:
            sm.trade()

        elif state == State.SELL_ITEM.value:
            sm.trade()

        else:
            print("State error: there is no such state or state is empty")
            break

except ConnectionRefusedError:
    print("Connection failed.")
finally:
     ClientModule.Connection.close_connection()