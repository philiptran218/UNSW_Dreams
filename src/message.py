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
    else:
        dm = dm_details(msg['dm_id'])
        if dm['dm_owner'] == u_id:
            return True

    if msg['u_id'] == u_id:
        return True
    
    return False

def is_message_empty(message):
    message = message.replace(' ', '')
    message = message.replace('\n', '')
    message = message.replace('\t', '')
    return len(message) == 0


def message_send_v1(auth_user_id, channel_id, message):
    return {
        'message_id': 1,
    }

def message_remove_v1(auth_user_id, message_id):
    return {
    }

def message_edit_v1(auth_user_id, message_id, message):
    '''
    Function:
        Given a message, update its text with new text. If the new message is an 
        empty string, the message is deleted.
        
    Arguments:
        token (str) - this is the token of a registered user during their 
                      session
        message_id (int) - this is the ID of an existing message 
        message (str) - the new edited message 
        
    Exceptions:
        InputError - occurs when the message ID is not a valid ID, when the 
                     message has already been deleted and when the edited 
                     message is longer than 1000 characters
        AccessError - occurs when the user ID is not a valid ID and when the
                      user is not authorised to edit the message 
                      
    Return value:
        Returns an empty dictionary {}
    '''
    # Check for valid u_id
    if not helper.is_valid_uid(auth_user_id):
        raise AccessError("Please enter a valid u_id")
    # Check if message_id is valid
    if not message_exists(message_id):
        raise InputError("message_id does not exist")
    msg = message_details(message_id)
    # Check if message has already been removed
    if msg['message'] == '' and msg['channel_id'] == -1 and msg['dm_id'] == -1:
        raise InputError("Message has already been deleted")
    # Check if user has permission to remove the message
    if not is_user_authorised(auth_user_id, message_id):
        raise AccessError("User is not authorised to remove the message")
    # Check if edited message is longer than 1000 characters
    if len(message) > 1000:
        raise InputError("Message is longer than 1000 characters long")
    # If edited message is empty, the current message is removed
    if is_message_empty(message):
        edit_msg = message_details(message_id)
        edit_msg.update({'channel_id': -1})
        edit_msg.update({'dm_id': -1})
        edit_msg.update({'u_id': -1})
        edit_msg.update({'message': ''})
    else:   
        edit_msg = message_details(message_id)
        edit_msg.update({'u_id': auth_user_id})
        edit_msg.update({'message': message})
    return {}
    
