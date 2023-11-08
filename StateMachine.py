import ServerModule

class StateMachine():
    current_state = None
    nickname = None
    def __init__(self, start_state):
        self.current_state = start_state

    def login(self, nickname):
        self.nickname = nickname
        return ServerModule.login(nickname)

    def view_profile(self, nickname):
        ServerModule.show_user_data(nickname)
        self.choose_stage(['BC','welcome', 'go back'], ['SL', 'sell_item', 'sell item'])

    def sell_item(self, item_id):
        ServerModule.show_user_data(nickname)
        ServerModule.sell_item_by_id(input('Press item id\n'))
        pass

    def show_items_list(self):
        ServerModule.show_items_list()
        self.choose_stage(['BC','welcome', 'go back'], ['BY', 'buy_item', 'buy item'])
        
    def welcome(self):
        print(f'\nNice to see you {self.nickname}!\nWhat do you wanna to do?\n')
        self.choose_stage(['LO','leave_or_stay', 'logout'], ['IT', 'show_items_list', 'show items list'], ['IN', 'view_profile', 'show inventory'])
        
    def choose_stage(self, stage1, stage2, stage3 = ['', '', '']):
        print(f"Press '{stage1[0]}' to {stage1[2]}\nPress '{stage2[0]}' to {stage2[2]}")
        if stage3[0] != '':
            print(f"Press '{stage3[0]}' to {stage3[2]}\n")
        stage = input().upper()
        if stage == stage1[0]:
            self.current_state = stage1[1]
        elif stage == stage2[0]:
            self.current_state = stage2[1]
        elif stage3[0] != '' and stage == stage3[0]:
            self.current_state = stage3[1]
        else:
            print('Something went wrong. Try again.')
            self.choose_stage(stage1, stage2, stage3)

