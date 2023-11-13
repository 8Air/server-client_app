import Connection

def create_user(nickname: str):
    user_message = f'''There is no user with nickname {nickname}.
Do you want to create a new account? [Y/N]\n'''
    answer = input(user_message).upper()
    Connection.send_utf_message(answer)
    if answer == 'Y':
        return True
    return False

def receive_items_data():
    received_data = ""
    endswith = '\0'
    while True:
        chunk = Connection.receive_utf_message()
        if not chunk or chunk.endswith(endswith):
            received_data += chunk[:-1]
            break
        received_data += chunk
    return received_data

def check_login_success(nickname: str):
    Connection.send_utf_message(nickname)
    return_code = Connection.receive_byte_message()
    if return_code == Connection.ReturnCode.NO_USER.value:
        if create_user(nickname):
            return_code = Connection.receive_utf_message()
            print(return_code)
        else:
            return False
    return True