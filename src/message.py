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
        
def is_user_authorised(u_id, message_id):
    if helper.find_permissions(u_id) == 1:
        return True
        
    msg = message_details(message_id)
    owners_list = helper.channel_owners(msg['channel_id'])
    for owners in owners_list:
        if owners['u_id'] == u_id:
            return True

    if msg['u_id'] == u_id:
        return True
    
    return False


def message_send_v1(auth_user_id, channel_id, message):
    return {
        'message_id': 1,
    }

def message_remove_v1(auth_user_id, message_id):
    return {
    }

def message_edit_v1(auth_user_id, message_id, message):
    # Check for valid u_id
    if helper.is_valid_uid(auth_user_id) == False:
        raise AccessError("Please enter a valid u_id")
    # Check if message_id is valid
    if message_exists(message_id) == False:
        raise InputError("message_id does not exist")
    # Check if user has permission to remove the message
    if is_user_authorised(auth_user_id, message_id) == False:
        raise AccessError("User is not authorised to remove the message")
    # Check if message has already been removed
    msg = message_details(message_id)
    if msg['message'] == '' and msg['channel_id'] == -1 and msg['dm_id'] == -1:
        raise InputError("Message has already been deleted")
    # Check if edited message is longer than 1000 characters
    if len(message) > 1000:
        raise InputError("Message is longer than 1000 characters long")
    # If edited message is empty, the current message is removed
    if message == '':
        edit_msg = message_details(message_id)
        edit_msg.update({'channel_id': -1})
        edit_msg.update({'dm_id': -1})
        edit_msg.update({'u_id': -1})
        edit_msg.update({'message': message})
       
    edit_msg = message_details(message_id)
    edit_msg.update({'u_id': auth_user_id})
    edit_msg.update({'message': message})
    
    return {}
    
