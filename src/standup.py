from src.error import AccessError, InputError
from src.database import data, update_data
import src.helper as helper
from src.message import message_send_v1, add_tag_notification
from datetime import timezone, datetime, timedelta
import threading 
import time

#helper to check if msg empty
def is_message_empty(message):
    message = message.replace(' ', '')
    message = message.replace('\n', '')
    message = message.replace('\t', '')
    return len(message) == 0

def standup_msg_send(auth_user_id, channel_id, message):
    message_id = len(data['messages']) + 1
    time = datetime.now()
    time = int(time.timestamp())
    message_info = {
        'message_id': message_id,
        'channel_id': channel_id,
        'dm_id': -1,
        'u_id': auth_user_id,
        'message': message,
        'time_created': time,
        'reacts': helper.create_reacts(),
        'is_pinned': None
    }
    data['messages'].append(message_info)
    add_tag_notification(auth_user_id, channel_id, -1, message)
    update_data()

#function that creates a standup and adds it to the list of standups.
def standup_create(auth_user_id,channel_id,length,token):
    curr_time = datetime.now()+ timedelta(seconds=length)
    curr_time = int(curr_time.timestamp())
    standup = {
        'channel_id':channel_id,
        'u_id': auth_user_id,
        'messages':[],
        'finish_time': curr_time,
        'is_active': True
    }
    data['standups'].append(standup)
    update_data()
    time.sleep(length)
    
    for stands in data['standups']:
        if stands['channel_id'] == channel_id:
            if len (stands['messages']) > 0:
                final_msg = '\n'.join(stands['messages'])
                standup_msg_send(auth_user_id, channel_id, final_msg)
    for stand in data['standups']:
        if stand['channel_id'] == channel_id:
            data['standups'].remove(stand)
    update_data()

def standup_running(channel_id):
    for standup in data['standups']:
        if standup['channel_id'] == channel_id:
            return True
    return False

def standup_start_v1(token,channel_id,length):
    '''
    Function:
    For a given channel, start the standup period whereby for the next "length" seconds
        if someone calls "standup_send" with a message, it is buffered during the X second window 
        then at the end of the X second window a message will be added to the message queue
        in the channel from the user who started the standup. X is an integer that denotes 
        the number of seconds that the standup occurs for

    Arguments:
        token (str) - this is the token of a registered user during their
                      session
        channel_id (int) - this is the ID of an existing channel

        length (int) - this is the length that the standup is going to run for in seconds

    Exceptions:
        InputError - the channel ID is not a valid ID
                   - An active standup is currently running in this channel
        AccessError - the user's token is not a valid token
                    - the user is not in the channel
  

    Return value:
        Returns a dictionary containing the type {time_finish}
    '''

    # Check for token
    if not helper.is_valid_token(token):
        raise AccessError(description="Please enter a valid token")  
    auth_user_id = helper.detoken(token)    
    # Check for valid channel_id
    if not helper.is_valid_channelid(channel_id):
        raise InputError(description="Please enter a valid channel_id")       
    # Check if user is not in the channel
    if not helper.is_already_in_channel(auth_user_id, channel_id):
        raise AccessError(description="User is not a member in the channel")
    if standup_running(channel_id):
        raise InputError(description="An active standup is currently running in this channel") 

    curr_time = datetime.now()+ timedelta(seconds=length)
    curr_time = int(curr_time.timestamp())
    mythread = threading.Thread(target=standup_create,args=(auth_user_id,channel_id,length,token))
    mythread.start()
    return{'time_finish':curr_time}

def standup_active_v1(token,channel_id):
    '''
    Function:
        For a given channel, return whether a standup is active in it,
        and what time the standup finishes. If no standup is active, then time_finish returns None

    Arguments:
        token (str) - this is the token of a registered user during their
                      session
        channel_id (int) - this is the ID of an existing channel



    Exceptions:
        InputError - the channel ID is not a valid ID
        
        AccessError - the user's token is not a valid token
                    - the user is not in the channel
  

    Return value:
        Returns a dictionary containing the type {time_finish}
    '''
    # Check for token
    if not helper.is_valid_token(token):
        raise AccessError(description="Please enter a valid token")  
    auth_user_id = helper.detoken(token)    
    # Check for valid channel_id
    if not helper.is_valid_channelid(channel_id):
        raise InputError(description="Please enter a valid channel_id")       
    # Check if user is not in the channel
    if not helper.is_already_in_channel(auth_user_id, channel_id):
        raise AccessError(description="User is not a member in the channel")
    
    for standup in data['standups']:
        if standup['channel_id'] == channel_id:
            return {'is_active':True,'time_finish':standup['finish_time']}
    return {'is_active':False,'time_finish':None}
    

def standup_send_v1(token,channel_id,message):
    # Check for token
    if not helper.is_valid_token(token):
        raise AccessError(description="Please enter a valid token")  
    auth_user_id = helper.detoken(token)    
    # Check for valid channel_id
    if not helper.is_valid_channelid(channel_id):
        raise InputError(description="Please enter a valid channel_id")       
    # Check if user is not in the channel
    if not helper.is_already_in_channel(auth_user_id, channel_id):
        raise AccessError(description="User is not a member in the channel they are sending the message to")
    # Check if message is empty
    if is_message_empty(message):
        return {}
    # Check if message surpasses accepted length
    if len(message) > 1000:
        raise InputError(description="Message is longer than 1000 characters")
    if not standup_running(channel_id):
        raise InputError(description='no standup running in this channel')
    handle = helper.get_handle(auth_user_id)
    for standup in data['standups']:
        if standup['channel_id'] == channel_id:
            msg = ''
            msg = handle + ':' + ' ' + message
            standup['messages'].append(msg)
            update_data()
    return{}
