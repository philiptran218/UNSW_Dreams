import pytest
from src.error import InputError
import re
from src.database import data

# To test whether the email is valid
REGEX = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'


def generate_handle(name_first, name_last):
    handle = name_first + name_last
    handle = handle.lower()
    handle = handle.replace("@", "")
    handle = handle.replace(" ", "")

    if len(handle) > 20:
        handle = handle[:20]
    else:
        pass
    
    handle_num = 0

    while is_handle_taken(handle):
        if len(handle) == 20:
            handle = handle[:len(handle) - len(str(handle_num))]
        elif len(str(handle_num)) != len(str(handle_num - 1)) and handle_num > 0:
            handle = handle[:len(handle) - len(str(handle_num - 1))]  
        elif handle_num >= 1:
             handle = handle[:len(handle) - len(str(handle_num))]
        handle += str(handle_num)
        handle_num += 1
    return handle

def is_handle_taken(handle):
    for user in data['users']:
        if user['handle_str'] == handle:
            return True
    return False



def auth_login_v1(email, password):

    # invalid email entered
    if not re.search(REGEX, email):
        raise InputError("Invalid Email")

    # Check whether the email used is registered with the site
    user_not_found = True
    for user in data['users']:
        if user.get('email') == email:
            user_not_found = False
            break

    if user_not_found:
        raise InputError("User not found")

    incorrect_password = True

    # Check if enter password matches the password used to register
    for user in data['users']:
        if user.get('email') == email:
            if user.get('password') == password:
                incorrect_password = False

    if incorrect_password:
        raise InputError("Invalid Password")

    for user in data['users']:
        if user.get('email') == email:
            break

    return {'auth_user_id': user.get('u_id')}

def auth_register_v1(email, password, name_first, name_last):
    if len(data['users']) == 0:
        pass
    else:
        for user in data['users']:
            if user.get("email") == email:
                raise InputError("Email is already taken")
    # check if email entered has the correct format
    if not re.search(REGEX, email):
        raise InputError("Invalid Email")
    
    # Check whether the password is valid
    if len(password) < 6:
        raise InputError("Invalid Password")
    
    # Check whether the first name is valid
    if len(name_first) == 0 or len(name_first) > 50:
        raise InputError("Invalid First Name")

    # Check whether the last name is valid
    if len(name_last) == 0 or len(name_last) > 50:
        raise InputError("Invalid Last Name")
    
    # Check the number of registered users 
    number_users = len(data['users'])

    # Assign a permissions_id to users. The first user is defaulted as perm_id 1 and everyone else is perm_id 2
    if (number_users == 0):
        perm_id = 1
    else:
        perm_id = 2


    user = {
        'u_id': number_users + 1,
        'name_first': name_first,
        'name_last': name_last,
        'perm_id': perm_id,
        'password': password,
        'email': email,
        'handle_str': generate_handle(name_first, name_last),
    }
    
    data['users'].append(user)
    return {'auth_user_id': number_users + 1}
