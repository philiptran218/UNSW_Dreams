from src.database import data
from src.helper import is_valid_token, detoken, get_handle
from src.error import AccessError, InputError

TAG = 1
INVITE = 2

# Helper fucntion that when given a key mapping to a list in a dicionary, empties that list. 
def delete(aspect):
    ((data.get(aspect)).clear())

def clear_v1():
    '''
    Function:
        Resets the internal data of the application to it's initial stateerases all information 
        about the users, erases all the channels and the messages.

    Arguments:
        This fucntion doesn't take any arguments.

    Exceptions:
        This function doesn't throw any excpetions.

    Return Value:
        This function doesn't return any value.
    '''
    delete('users')
    delete('channels')
    delete('messages')
    delete('DM')
    delete('notifications')
    delete('sessions')
    delete('session_ids')


def search_v1(auth_user_id, query_str):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
    }
    
def get_channel_dm_name(channel_id, dm_id):
    if channel_id == -1:
        for dm in data['DM']:
            if dm['dm_id'] == dm_id:
                return dm['name']
    elif dm_id == -1:
        for channel in data['channels']:
            if channel['channel_id'] == channel_id:
                return channel['name']
    
def notifications_get_v1(token):
    if not is_valid_token(token):
        raise AccessError(description="Please enter a valid token")
    auth_user_id = detoken(token)
    notif_list = list(reversed(data['notifications']))
    recent_notifs = []
    
    for notif in notif_list:
        chan_dm_name = get_channel_dm_name(notif['channel_id'], notif['dm_id'])
        if notif['u_id'] == auth_user_id:
            if notif['type'] == TAG:
                notif_msg = get_handle(notif['auth_user_id']) + ' tagged you in '
                notif_msg = notif_msg + chan_dm_name + ': ' + notif['message'][:20]
            else:
                notif_msg = get_handle(notif['auth_user_id']) + ' added you to ' + chan_dm_name
                
            notif_dict = {
                'channel_id': notif['channel_id'],
                'dm_id': notif['dm_id'],
                'notification_message': notif_msg
            }
            recent_notifs.append(notif_dict)
    return recent_notifs
        
