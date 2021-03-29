import pytest
from src.error import InputError
import re
from src.database import data
import jwt

SECRET = 'COMP1531PROJECT'

def user_profile_v1(token, u_id):
    
    if helper_functions.is_valid_token(token).get('token_status'):
        raise error.AccessError(description="Token invalid")
    
    return {
        'user': {
            'u_id': 1,
            'email': 'cs1531@cse.unsw.edu.au',
            'name_first': 'Hayden',
            'name_last': 'Jacobs',
            'handle_str': 'haydenjacobs',
        },
    }

def user_profile_setname(token, name_first, name_last):
    
    if (len(name_first) < 1) or (len(name_first) > 50):
        raise InputError("First name is invalid")
    
    if (len(name_last) < 1) or (len(name_last) > 50):
        raise InputError("Last name is invalid")
    
    return {'first_name': name_first, 'last_name': name_last}
    

def user_profile_setemail_v2(token, email):

    REGEX = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'


    #test for invalid email
    for user in data['users']:
        if user.get("email") == email:
            raise InputError("Email is already taken")

    if not re.search(REGEX, email):
        raise InputError("Invalid Email")

    for users in data['users']:
        if data.get("email") == email:
            raise InputError("Email is already taken")
   
    for users in data['users']:
        if users.get('u_id') == 'u_id':
            data['email'] = email
            break
    return {}

def user_profile_sethandle_v2(token, handle_str):
    
    
    
    return {
    }