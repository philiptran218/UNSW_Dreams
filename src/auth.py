import pytest
from src.error import InputError, AccessError
import re
from src.database import data
import hashlib
import jwt
from src.helper import is_valid_token

# To test whether the email is valid
REGEX = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
SECRET = 'COMP1531PROJECT'


def generate_handle(name_first, name_last):
    handle = name_first + name_last
    handle = handle.lower()
    handle = handle.replace("@", "")
    handle = handle.replace(" ", "")
    handle = handle.replace("\n", "")
    handle = handle.replace("\t", "")

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
    
def generate_session_id():
    new_session_id = len(data['session_ids']) + 1
    data['session_ids'].append(new_session_id)
    return new_session_id

def auth_login_v1(email, password):
    '''
    Function:
        Allows existing users to login using their registered email and password.
        
    Arguments:
        email(char) - The email used to sign in
        password(char) - The password used to sign in
    
    Exceptions:
        InputError when any of:
            - The email used is not in the form of a real email
            - The email used has not yet been registered
            - The password entered is incorrect

    
    Return Values:
        This function returns u_id and token of the user    
    '''
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
    enc_password = hashlib.sha256(password.encode()).hexdigest()
    # Check if enter password matches the password used to register
    for user in data['users']:
        if user.get('email') == email and user.get('password') == enc_password:
            incorrect_password = False
            break

    if incorrect_password:
        raise InputError("Invalid Password")
    # Payload for token generation
    payload = {
        'u_id': user['u_id'],
        'session_id': generate_session_id()
    }   
    token = jwt.encode(payload, SECRET, algorithm='HS256')
    session = {
        'u_id': payload['u_id'],
        'session_id': payload['session_id'],
        'token': token,
    }
    # Append the session information to sessions list in data
    data['sessions'].append(session)    
    return {
        'token': token,
        'auth_user_id': user['u_id']
    }

def auth_register_v1(email, password, name_first, name_last):
    '''
    Function:
        Allows new users to register
        
    Arguments:
        email(char) - The email used to sign up
        password(char) - The password used to sign up
        name_first - The user's first name
        name_last - The user's last name
    
    Exceptions:
        InputError when any of:
            - The email entered is not in the form of a real email
            - The email entered has been taken
            - The password entered is invalid
            - The first name is zero characters or more than 50 characters
            - The last name is zero characters or more than 50 characters

    Return Values:
        This function returns u_id and token of the user    
    '''
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
        'password': hashlib.sha256(password.encode()).hexdigest(),
        'email': email,
        'handle_str': generate_handle(name_first, name_last),
    }
    
    data['users'].append(user)
    return auth_login_v1(email, password)

def auth_logout(token):
    '''
    Function:
        Allows logged in users to log out
        
    Arguments:
        token(str) - this is the token of a registered user during their session
    
    Exceptions:
        AccessError - When the token is invalid

    Return Values:
        This function will return "is_sucess" when successful
    '''
    
    if not is_valid_token(token):
        raise AccessError(description='Please enter a valid token')
   
    for sesh in data['sessions']:
        if sesh.get('token') == token:
            sesh.remove(sesh)

    return {
        'is_success': True,
    }