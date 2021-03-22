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
 
def is_valid_dmid(dm_id):
    for dm in data['DM']:
        if dm['dm_id'] == dm_id:
            return True
    return False
    
def is_already_in_dm(u_id, dm_id):
    for dm in data['DM']:
        for member in dm['dm_members']:
            if member['u_id'] == u_id:
                return True
    return False
 
def is_message_empty(message):
    message = message.replace(' ', '')
    message = message.replace('\n', '')
    message = message.replace('\t', '')
    return len(message) == 0
   
def message_senddm_v1(auth_user_id, dm_id, message):
    # Check for valid u_id
    if helper.is_valid_uid(auth_user_id) == False:
        raise AccessError("Please enter a valid u_id")  
    # Check for valid dm_id
    if is_valid_dmid(dm_id) == False:
        raise InputError("Please enter a valid dm_id")       
    # Check if user is not in the DM
    if is_already_in_dm(auth_user_id, dm_id) == False:
        raise AccessError("User is not a member in the DM they are sending the message to")
    # Check if message is empty
    if is_message_empty(message):
        raise InputError("Empty messages cannot be posted to DMs")
    # Check if message surpasses accepted length
    if len(message) > 1000:
        raise InputError("Message is longer than 1000 characters")
    message_id = len(data['messages']) + 1   
    time = datetime.today()
    time = time.replace(tzinfo=timezone.utc).timestamp()
    
    message_info = {
        'message_id': message_id,
        'channel_id': -1,
        'dm_id': dm_id,
        'u_id': auth_user_id,
        'message': message,
        'time_created': round(time),
    }
    data['messages'].append(message_info)
    return {
        'message_id': message_id,
    }
       
