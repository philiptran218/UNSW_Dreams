from src.error import InputError, AccessError
import re
from src.database import data, update_data
from src.helper import is_valid_token, is_valid_uid, detoken, is_already_in_channel
from datetime import timezone, datetime

def get_utlilisation_rate(token):

    token_u_id = detoken(token)
    num_users = len(data['users'])
    unutilised = True
    util_users = 0

    for user in data['users']:
        for channel in data['channels']:
            if is_already_in_channel(user['u_id'], channel['channel_id']) == False:
                unutilised == False

        for dm in data['DM']:
            for member in dm['dm_members']:
                if member['u_id'] == token_u_id:
                    unutilised == False

        if unutilised == False:
            util_users += 1

    util_rate = float(util_users/num_users)
        
    return util_rate

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

    if not is_valid_token(token):
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

def users_stats_v1(token):
    '''
    Function:
       Returns the stats useful for the analytics of dreams. 

    Arguments:
        token (str) - token of a registered user during their session

    Exceptions:     
        AccessError - the user who calls the fucntion is not a valid user (invalid token).

    Return Type:
        This function returns the dreams_stats data type; a dictionary with several integers / floats describing key 
        statistics about all dreams users.
    ''' 

    if is_valid_token == False:
        raise AccessError(description='token invalid')

    num_channels = len(data['channels'])
    num_dms = len(data['DM'])
    num_msg = len(data['messages'])
    util_rate = get_utlilisation_rate(token)

    time = datetime.today()
    time = time.replace(tzinfo=timezone.utc).timestamp()
    time_issued = round(time)

    data['users_stats_log'].update({
        'num_channels': [{num_channels, time_issued}],
        'num_dms': [{num_dms, time_issued}],
        'num_msg': [{num_msg, time_issued}],
        'utilisation_rate': util_rate,
    })
    update_data()

    return data['users_stats_log']

    



    
