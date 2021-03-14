from src.error import InputError, AccessError 
from src.database import data
import src.helper as helper
from datetime import timezone, datetime

def message_send_v1(auth_user_id, channel_id, message):
    # Check for valid u_id
    if helper.is_valid_uid(auth_user_id) == False:
        raise AccessError("Please enter a valid u_id")  
    # Check for valid channel_id
    if helper.is_valid_channelid(channel_id) == False:
        raise InputError("Please enter a valid channel_id")       
    # Check if user is not in the channel
    if helper.is_already_in_channel(auth_user_id, channel_id) == False:
        raise AccessError("User is not a member in the channel they are sending the message to")
    # Check is message is empty
    if message == '':
        raise InputError("Empty messages cannot be posted to channels")
    # Check if message surpasses accepted length
    if len(message) > 1000:
        raise InputError("Message is longer than 1000 characters long")
    
    message_id = len(data['messages']) + 1   
    time = datetime.today()
    time = time.replace(tzinfo=timezone.utc).timestamp()
    
    message_info = {
        'message_id': message_id,
        'channel_id': channel_id,
        'dm_id': -1,
        'u_id': auth_user_id,
        'message': message,
        'time_created': round(time),
    }
    data['messages'].append(message_info)
    return {
        'message_id': message_id,
    }

def message_remove_v1(auth_user_id, message_id):
    return {
    }

def message_edit_v1(auth_user_id, message_id, message):
    return {
    }
    
