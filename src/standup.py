from src.error import AccessError, InputError
from src.database import data, update_data
import src.helper as helper
from datetime import timezone, datetime, timedelta
import threading 
import time

#helper to check for valid channel_id
def is_valid_channelid(channel_id): 
    if channel_id < 1:
        return False
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            return True       
    return False

#helper to check if msg empty
def is_message_empty(message):
    message = message.replace(' ', '')
    message = message.replace('\n', '')
    message = message.replace('\t', '')
    return len(message) == 0

#function that creates a standup and adds it to the list of standups.
def standup_create(auth_user_id,channel_id,length):
    standup = {
        'channel_id':channel_id,
        'u_id': auth_user_id,
        'messages':[],
        'finish_time': datetime.now()+ timedelta(seconds=length),
        'is_active': True
    }
    data['standups'].append(standup)
    time.sleep(length)
    data['standups'].remove(standup)

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
    if not is_valid_channelid(channel_id):
        raise InputError(description="Please enter a valid channel_id")       
    # Check if user is not in the channel
    if not helper.is_already_in_channel(auth_user_id, channel_id):
        raise AccessError(description="User is not a member in the channel they are sending the message to")
    if standup_running(channel_id):
        raise InputError(description="An active standup is currently running in this channel") 


    standup_create(auth_user_id,channel_id,length)
    finishing_time = datetime.now()+ timedelta(seconds=length)
    mythread = threading.Thread(target=standup_create)
    mythread.start()
    return{'time_finish':finishing_time}




def standup_active_v1(token,channel_id):
    pass

def standup_send_v1(token,channel_id,message):
    # Check for token
    if not helper.is_valid_token(token):
        raise AccessError(description="Please enter a valid token")  
    auth_user_id = helper.detoken(token)    
    # Check for valid channel_id
    if not is_valid_channelid(channel_id):
        raise InputError(description="Please enter a valid channel_id")       
    # Check if user is not in the channel
    if not helper.is_already_in_channel(auth_user_id, channel_id):
        raise AccessError(description="User is not a member in the channel they are sending the message to")
    # Check if message is empty
    if is_message_empty(message):
        raise InputError(description="Empty messages cannot be posted to channels")
    # Check if message surpasses accepted length
    if len(message) > 1000:
        raise InputError(description="Message is longer than 1000 characters")