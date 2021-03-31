from src.helper import detoken, get_email, get_first_name, get_last_name, get_handle
from src.database import data

def user_profile_v1(token, u_id):
    detoken(token)

    for member in data['users']:
        if member['u_id'] == u_id: 
            return {
                'u_id': u_id,
                'email': get_email(u_id), 
                'name_first': get_first_name(u_id),
                'name_last': get_last_name(u_id),
                'handle_str': get_handle(u_id),
            }

def user_profile_setname_v1(token, name_first, name_last):
    token_u_id = detoken(token)
    for member in data['users']:
        if member['u_id'] == token_u_id:
            member['name_first'] = name_first
            member['name_last'] = name_last

def user_profile_setemail_v1(auth_user_id, email):
    return {
    }

def user_profile_sethandle_v1(auth_user_id, handle_str):
    return {
    }
