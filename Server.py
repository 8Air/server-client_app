from StateMachine import *

sm = StateMachine('login')

while sm.current_state != 'logout':
    if sm.current_state == 'leave_or_stay':
        sm.choose_stage(['C','login', 'continue'], ['E', 'logout', 'exit'])
    elif sm.current_state == 'login':
        if sm.login(input("Enter nickname: ")):
            sm.current_state = 'welcome'
        else:
            sm.current_state = 'leave_or_stay'
    elif sm.current_state == 'welcome':
        sm.welcome()
    elif sm.current_state == 'view_profile':
        sm.view_profile(sm.nickname)
    elif sm.current_state == 'show_items_list':
        sm.show_items_list()
