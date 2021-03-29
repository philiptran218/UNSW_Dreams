import pytest
from src.error import InputError, AccessError
import re
from src.database import data
import jwt
from src.helper import is_valid_token, is_valid_uid

SECRET = 'COMP1531PROJECT'

def user_profile_v2(token, u_id):
    
    if is_valid_token(token) == False:
        raise AccessError(description="Token invalid")

    if is_valid_uid(u_id) == False:
        raise AccessError(description="Invalid u_id")
    
    for user in data['users']:
        user_details = {
            'user' : {
                'u_id': users.get('u_id'),
                'email': users.get('email'),
                'name_first': users.get('first_name'),
                'name_last': users.get('last_name'),
                'handle_str': users.get('handle'),
    
        return user_details
        

def user_profile_setname(token, name_first, name_last):
       
    if is_valid_token(token) == False:
        raise AccessError(description="Token invalid")

    if is_valid_uid(u_id) == False:
        raise AccessError(description="Invalid u_id")

    if (len(name_first) < 1) or (len(name_first) > 50):
        raise InputError("First name is invalid")
    
    if (len(name_last) < 1) or (len(name_last) > 50):
        raise InputError("Last name is invalid")
    
    return {'first_name': name_first, 'last_name': name_last}
    

def user_profile_setemail_v2(token, email):

    REGEX = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    
    if is_valid_token(token) == False:
        raise AccessError(description="Token invalid")

    if is_valid_uid(u_id) == False:
        raise AccessError(description="Invalid u_id")

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

    if is_valid_uid(u_id) == False:
        raise AccessError("Invalid u_id")

    if len(handle_str) < 3 or len(handle_str) > 20:
        raise error.InputError("Handle_str invalid")
    
    for user in data['users']:
        if user['handle_str'] == handle:
            raise InputError("Handle taken")
    
    for user in data['users']:
        if user.get("u_id") == u_id:
            user["handle"] = handle_str
            break

    return {}