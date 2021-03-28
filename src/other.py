from src.database import data
from src.error import InputError, AccessError
import src.helper as helper

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


def get_channel_name(channel_id):
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            return channel['name']
            
def get_dm_name(dm_id):
    for dm in data['DM']:
        if dm['dm_id'] == dm_id:
            return dm['dm_name']
 
def get_channel_dm_id(message_id):
    for message in data['messages']:
        if message['message_id'] == message_id:
            return (message['channel_id'], message['dm_id'])
 
def get_tag_notifications(u_id):
    handle = helper.get_handle(u_id)
    handle = '@' + handle
    notifs = []

    tags = search_v1(u_id, handle)['messages']
    for message in tags:
        tagger_handle = helper.get_handle(message['u_id'])
        chan_dm = get_channel_dm_id(message['message_id'])
        if chan_dm[0] != -1 and chan_dm[1] == -1:
            channel_dm_name = get_channel_name(chan_dm[0])
        else:
            channel_dm_name = get_dm_name(chan_dm[1])
            
        tag_msg = message['message']
        if tag_msg > 20:
            tag_msg = tag_msg[:20]
        notif_msg = tagger_handle + ' tagged you in '
        notif_msg = notif_msg + channel_dm_name + ': ' + tag_msg    
        tag_info = {
            'notification_message': notif_msg,
            'channel_id': chan_dm[0],
            'dm_id': chan_dm[1],
            'time_created': message['time_created'],
        }
        notifs.append(tag_info)
    return notifs

def get_invite_notifications(u_id):
    notifs = []
    for notif in data['notifications']:
        if notif['u_id'] == u_id:
            
            if notif['channel_id'] != -1 and notif['dm_id'] == -1:
                channel_dm_name = get_channel_name(notif['channel_id'])
            else:
                channel_dm_name = get_dm_name(notif['dm_id'])        
            invite_handle = helper.get_handle(notif['auth_user_id'])
            notif_msg = invite_handle + ' added you to ' + channel_dm_name
            invite_info = {
                'notification_message': notif_msg,
                'channel_id': notif['channel_id'],
                'dm_id': notif['dm_id'],
                'time_created': notif['time_created']
            }
            notifs.append(invite_info)
    return notifs
                  
def notifications_get_v1(auth_user_id):
    '''
    Function:
        Returns the user's most recent 20 notifications. A notification is
        raised when the user is added to a channel/DM or is tagged in a message.
    
    Arguments:
        token (str) - this is the token of a registered user during their
                      session
    
    Exceptions:
        AccessError - occurs when the user's token is not a valid token
    
    Return value:
        Returns a list of dictionaries containing types {channel_id, dm_id,
        notification_message}
    '''
    if not helper.is_valid_uid(auth_user_id):
        raise AccessError(description="Please enter a valid uid")
        
    time_notifs = get_tag_notifications(auth_user_id) + get_invite_notifications(auth_user_id)
    time_notifs = sorted(time_notifs, key = lambda i: i['time_created'], reverse=True)
    counter = 0
    recent_notifs = []
    for notif in time_notifs:
        if counter >= 20:
            break
        
        notif_info = {
            'channel_id': notif['channel_id'],
            'dm_id': notif['dm_id'],
            'notification_message': notif['notification_message']
        }
        recent_notifs.append(notif_info)
        counter += 1
    return recent_notifs
        
