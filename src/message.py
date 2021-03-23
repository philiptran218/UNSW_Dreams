from src.error import InputError, AccessError 
from src.database import data
import src.helper as helper
from datetime import timezone, datetime

def message_send_v1(auth_user_id, channel_id, message):
    return {
        'message_id': 1,
    }

def message_remove_v1(auth_user_id, message_id):
    return {
    }

def message_edit_v1(auth_user_id, message_id, message):
    return {
    }

def message_details(message_id):
    for message in data['messages']:
        if message['message_id'] == message_id:
            return message
            
def is_message_empty(message):
    message = message.replace(' ', '')
    message = message.replace('\n', '')
    message = message.replace('\t', '')
    return len(message) == 0

def is_valid_dm_id(dm_id):
    for dm in data['DM']:
        if dm['dm_id'] == dm_id:
            return True
    return False
    
def is_message_deleted(message):
    if message['channel_id'] == -1 and message['dm_id'] == -1:
        return True
    else:
        return False
    
def message_share_v1(auth_user_id, og_message_id, message, channel_id, dm_id):
    # Check for valid u_id
    if not helper.is_valid_uid(auth_user_id):
        raise AccessError("Please enter a valid u_id")
    if channel_id != -1 and dm_id == -1:
        # Check for valid channel_id
        if not helper.is_valid_channelid(channel_id):
            raise InputError("Please enter a valid channel_id")
        # Check if user has joined the channel
        if not is_already_in_channel(auth_user_id, channel_id):
            raise AccessError("User is not a member in the channel they are sharing the message to")        
    else:
        # Check for valid dm_id
        if not is_valid_dm_id(dm_id):
            raise InputError("Please enter a valid dm_id")
        # Check if user has joined the DM
        if not is_already_in_dm(auth_user_id, dm_id):
            raise AccessError("User is not a member in the DM they are sharing the message to")
    # Check if og_message_id is valid
    if not message_exists(og_message_id):
        raise InputError("og_message_id does not exist")
    og_msg = message_details(og_message_id)
    # Check if og_message_id has been removed
    if is_message_deleted(og_msg):
        raise InputError("Message has already been deleted")
    # Check if og_message + optional message > 1000 characters
    if not is_message_empty(message):
        if len(og_msg['message']) + len(message) + 1 > 1000:
            raise InputError("Message is longer than 1000 characters")

    message_id = len(data['messages']) + 1
    time = datetime.today()
    time = time.replace(tzinfo=timezone.utc).timestamp()
    # If the optional message is empty or just whitespace, it will not be
    # appended to the og_message 
    if is_message_empty(message):
        app_message = ''
    else:
        app_message = ' ' + message
    msg = {
        'message_id': message_id,
        'channel_id': channel_id,
        'dm_id': dm_id,
        'u_id': auth_user_id,
        'message': og_msg['message'] + app_message,
        'time_created': round(time),
    }
    data['messages'].append(msg)
    return {'shared_message_id': message_id}
     
