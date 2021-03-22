from src.error import InputError, AccessError 
from src.database import data
import src.helper as helper

def message_details(message_id):
    for message in data['messages']:
        if message['message_id'] == message_id:
            return message

def message_exists(message_id):
    for message in data['messages']:
        if message['message_id'] == message_id:
            return True
    return False    
 
def dm_details(dm_id):
    for dm in data['DM']:
        if dm['dm_id'] == dm_id:
            return dm
        
def is_user_authorised(u_id, message_id):
    if helper.find_permissions(u_id) == 1:
        return True
        
    msg = message_details(message_id)
    if msg['channel_id'] != -1 and msg['dm_id'] == -1:
        owners_list = helper.channel_owners(msg['channel_id'])
        for owners in owners_list:
            if owners['u_id'] == u_id:
                return True
    elif msg['channel_id'] == -1 and msg['dm_id'] != -1:
        dm = dm_details(msg['dm_id'])
        if dm['dm_owner'] == u_id:
            return True
    else:
        owners_list = helper.channel_owners(msg['channel_id'])
        in_channel = False
        for owners in owners_list:
            if owners['u_id'] == u_id:
                in_channel = True
        if in_channel:
            dm = dm_details(msg['dm_id'])
            if dm['dm_owner'] == u_id:
                return True
    
    if msg['u_id'] == u_id:
        return True
    
    return False


def message_send_v1(auth_user_id, channel_id, message):
    return {
        'message_id': 1,
    }

def message_remove_v1(auth_user_id, message_id):
    # Check for valid u_id
    if not helper.is_valid_uid(auth_user_id):
        raise AccessError("Please enter a valid u_id")
    # Check if message_id is valid
    if not message_exists(message_id):
        raise InputError("message_id does not exist")
    # Check if message has already been removed
    msg = message_details(message_id)
    if msg['message'] == '' and msg['channel_id'] == -1 and msg['dm_id'] == -1:
        raise InputError("Message has already been deleted")
    # Check if user has permission to remove the message
    if not is_user_authorised(auth_user_id, message_id) == False:
        raise AccessError("User is not authorised to remove the message")
    # Edit message details to show that it has been removed
    for message in data['messages']:
        if message['message_id'] == message_id:
            message.update({'channel_id': -1})
            message.update({'dm_id': -1})
            message.update({'u_id': -1})
            message.update({'message': ''})
    return {}

def message_edit_v1(auth_user_id, message_id, message):
    return {
    }
    
