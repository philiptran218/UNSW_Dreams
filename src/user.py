import pytest
from src.error import InputError, AccessError
import re
from src.database import data
import jwt
from src.helper import is_valid_token, is_valid_uid

SECRET = 'COMP1531PROJECT'

def user_profile(token, u_id):
    
    if is_valid_token(token) == False:
        raise AccessError(description="Token invalid")

    if is_valid_uid(u_id) == False:
        raise AccessError(description="Invalid u_id")
    
    for user in data['users']:
        if user['u_id'] == u_id:
            user_details = {
                'user' : {
                    'u_id': user.get('u_id'),
                    'email': user.get('email'),
                    'name_first': user.get('first_name'),
                    'name_last': user.get('last_name'),
                    'handle_str': user.get('handle'),
                }
            }
        return user_details

        
def user_profile_setname(token, name_first, name_last):
       
    if is_valid_token(token) == False:
        raise AccessError(description="Token invalid")

    if (len(name_first) < 1) or (len(name_first) > 50):
        raise InputError("First name is invalid")
    
    if (len(name_last) < 1) or (len(name_last) > 50):
        raise InputError("Last name is invalid")

    user[name_first] = name_first
    user[name_last] = name_last
        

def user_profile_setemail_v2(token, email):

    REGEX = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    
    if is_valid_token(token) == False:
        raise AccessError(description="Token invalid")

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
    if is_valid_token(token) == False:
        raise AccessError("Token invalid")

    if len(handle_str) < 3 or len(handle_str) > 20:
        raise InputError("Handle_str invalid")
    
    for user in data['users']:
        if user['handle_str'] == handle_str:
            raise InputError("Handle taken")
    
    user["handle"] = handle_str
    
    return {}

def user_all_v1(token):
    if is_valid_token(token) == False:
        raise AccessError("Token invalid")
    
    for user in data['users']:
        return user

