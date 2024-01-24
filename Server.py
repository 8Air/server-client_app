import ServerModule
from StatesEnum import State

class StateMachine():
    current_state: State = None
    nickname: str = None

    def __init__(self, start_state):
        self.current_state = start_state

    def choose_state(self):
        self.current_state = ServerModule.Connection.receive_utf_message()
        if self.current_state == 'show_items_listget_items_list':
            pass
    
    def set_state(self, state: str):
        self.current_state = state

    def get_state(self):
        return self.current_state

sm = StateMachine(State.LOGIN.value)

try:
    ServerModule.Connection.start_server()

    while sm.get_state() != State.LOGOUT.value:
        state: str = sm.get_state()

        if state == State.LEAVE.value:
            sm.choose_state()

        elif state == State.LOGIN.value:
            sm.nickname = ServerModule.login()
            if sm.nickname != None:
                sm.set_state(State.WELCOME.value)
            else:
                sm.set_state(State.LEAVE.value)

        elif state == State.WELCOME.value:
            sm.choose_state()

        elif state == State.PROFILE.value:
            ServerModule.send_user_profile_data(sm.nickname)
            sm.choose_state()

        elif state == State.SHOW_ITEMS.value:
            sm.choose_state()

        elif state == State.GET_ITEMS.value:
            ServerModule.send_items_list()
            sm.choose_state()

        elif state == State.BUY_ITEM.value:
            type = 'buy'
            if not ServerModule.trade(sm.nickname, type):
                sm.set_state(State.WELCOME.value)

        elif state == State.SELL_ITEM.value:
            type = 'sell'
            if not ServerModule.trade(sm.nickname, type):
                sm.set_state(State.WELCOME.value)
        else:
            print("State error: there is no such state or state is empty")
            break


    ServerModule.Connection.get_client_socket().close()
except ConnectionResetError:
    print("Connection has been broken.")
finally:
    ServerModule.Connection.get_server_socket().close()