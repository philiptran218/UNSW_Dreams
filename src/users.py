from src.error import InputError, AccessError
import re
from src.database import data, update_data
from src.helper import is_valid_token, is_valid_uid, detoken, is_already_in_channel
from datetime import timezone, datetime

def get_utlilisation_rate(token):

    num_users = len(data['users'])

    utilised_id_list = []

    for channel in data['channels']:
        for member in channel['all_members']:
            utilised_id_list.append(member['u_id'])

    for dm in data['DM']:
        for member in dm['dm_members']:
            for utilised_id in utilised_id_list:
                if member['u_id'] == utilised_id:
                    break
                utilised_id_list.append(member['u_id'])

    util_users = len(utilised_id_list)

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
            'profile_img_url': user['profile_img_url']
        }
        users_list.append(user_info)
    return {'users': users_list}

def update_stats(old_stats, stats_log):
    change_data = False
    if old_stats['channels_exist'][-1]['num_channels_exist'] != stats_log['channels_exist'][0]['num_channels_exist']:
        change_data = True
    if old_stats['dms_exist'][-1]['num_dms_exist'] != stats_log['dms_exist'][0]['num_dms_exist']:
        change_data = True
    if old_stats['messages_exist'][-1]['num_messages_exist'] != stats_log['messages_exist'][0]['num_messages_exist']:
        change_data = True
    if change_data:
        old_stats['messages_exist'].append(stats_log['messages_exist'][0])
        old_stats['channels_exist'].append(stats_log['channels_exist'][0])
        old_stats['dms_exist'].append(stats_log['dms_exist'][0])
    old_stats.update({'utilization_rate': stats_log['utilization_rate']})

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

    if is_valid_token(token) == False:
        raise AccessError(description='token invalid')

    num_channels_exist = len(data['channels'])
    num_dms_exist = len(data['DM'])
    num_msg_exist = len(data['messages'])
    util_rate = get_utlilisation_rate(token)

    time = datetime.now()
    time = time.timestamp()
    time_issued = int(time)

    stats_log = {
        'channels_exist': [{'num_channels_exist': num_channels_exist, 'time_stamp': time_issued}],
        'dms_exist': [{'num_dms_exist': num_dms_exist, 'time_stamp': time_issued}],
        'messages_exist': [{'num_messages_exist': num_msg_exist, 'time_stamp': time_issued}],
        'utilization_rate': util_rate,
    }
    if len(data['stats_log']) == 0:
        data['stats_log'].append(stats_log)
    else:    
        update_stats(data['stats_log'][0], stats_log)  
    update_data()

    return {'dreams_stats': data['stats_log'][0]}

