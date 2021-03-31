from src.error import InputError, AccessError
import re
from src.database import data
from src.helper import is_valid_token, is_valid_uid, detoken

def users_all_v1(token):
    """
    Function:
        This function displays information about all users

    Arguments:
        token(str) - token of the registered user.

    Exceptions:
        AccessError - If token is invalid

    Return Type:
        Function returns a list of all the users
    """

    if is_valid_token(token) == False:
        raise AccessError(description="Token invalid")
    
    users_list = []
    for user in data['users']:
        user_info = {
            'u_id': user['u_id'],
            'email': user['email'],
            'name_first': user['name_first'],
            'name_last': user['name_last'],
            'handle_str': user['handle_str'],
        }
        users_list.append(user_info)
    return {'users': users_list}
