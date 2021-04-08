from src.error import InputError, AccessError 
from src.database import data, update_data
import src.helper as helper
from datetime import timezone, datetime

OWNER = 1
MEMBER = 2
REACTS = [1]

# Helper functions for the message.py:
def is_message_empty(message):
    message = message.replace(' ', '')
    message = message.replace('\n', '')
    message = message.replace('\t', '')
    return len(message) == 0
     
def message_details(message_id):
    msg_details = None
    for message in data['messages']:    
        if message['message_id'] == message_id:
            msg_details = message
    return msg_details

def message_exists(message_id):
    for message in data['messages']:
        if message['message_id'] == message_id:
            return True
    return False 
    
def find_permissions(u_id):
    user_perm = None
    for user in data['users']: 
        if user['u_id'] == u_id:
            user_perm = user
            
    if user_perm['perm_id'] == OWNER:
        return OWNER
    else:
        return MEMBER
        
def is_user_authorised(u_id, message_id):
    if find_permissions(u_id) == OWNER:
        return True   
    msg = message_details(message_id)
    if msg['channel_id'] != -1 and msg['dm_id'] == -1:
        owners_list = channel_owners(msg['channel_id'])
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
 
def dm_details(dm_id):
    selected_dm = None
    for dm in data['DM']:  
        if dm['dm_id'] == dm_id:
            selected_dm = dm
    return selected_dm

def channel_owners(channel_id):
    list_of_owners = []
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            list_of_owners = channel['owner_members']
    return list_of_owners
        
def is_valid_channelid(channel_id): 
    if channel_id < 1:
        return False
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            return True       
    return False
    
def is_message_deleted(message):
    if message['channel_id'] == -1 and message['dm_id'] == -1:
        return True
    else:
        return False
 
def retrieve_members(channel_id, dm_id): 
    members = None
    if channel_id == -1:
        for dm in data['DM']:   
            if dm['dm_id'] == dm_id:
                members = dm['dm_members']
    else:
        for channel in data['channels']:      
            if channel['channel_id'] == channel_id:
                members = channel['all_members']
    return members 
                    
def add_tag_notification(auth_user_id, channel_id, dm_id, message):
    members = retrieve_members(channel_id, dm_id)
    
    for member in members:
        handle = '@' + member['handle_str']
        if handle in message:
            notification = {
                'auth_user_id': auth_user_id,
                'u_id': member['u_id'],
                'channel_id': channel_id,
                'dm_id': dm_id,
                'type': 1,
                'message': message,
            }
            data['notifications'].append(notification)


def message_send_v1(token, channel_id, message):
    '''
    Function:
        Send a message from authorised_user to the channel specified by 
        channel_id. Note: Each message has its own unique ID, whether it is in
        a channel or a DM.
        
    Arguments:
        token (str) - this is the token of a registered user during their 
                      session
        channel_id (int) - this is the ID of an existing channel
        message (str) - the message that will be sent to the channel with ID
                        channel_id
                        
    Exceptions:
        InputError - occurs when the channel ID is not a valid ID, when the
                     message being sent is empty and when the message has more
                     than 1000 characters
        AccessError - occurs when the user's token is not a valid token and when 
                      the user is not a member of the channel they are sending 
                      the message to 
        
    Return value:
        Returns a dictionary containing the type {message_id}
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
    # Check if message is empty
    if is_message_empty(message):
        raise InputError(description="Empty messages cannot be posted to channels")
    # Check if message surpasses accepted length
    if len(message) > 1000:
        raise InputError(description="Message is longer than 1000 characters")
    
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
        'reacts': helper.create_reacts(),
        'is_pinned': None
    }
    data['messages'].append(message_info)
    add_tag_notification(auth_user_id, channel_id, -1, message)
    update_data()
    return {
        'message_id': message_id,
    }

def message_remove_v1(token, message_id):
    '''
    Function:
        Given a message_id for a message, this message is removed from the 
        channel/DM.
        
    Arguments:
        token (str) - this is the token of a registered user during their
                      session
        message_id (int) - this is the ID of an existing message 
        
    Exceptions:
        InputError - occurs when the message ID is not a valid ID and when the
                     message has already been deleted
        AccessError - occurs when the user's token is not a valid token and when 
                      the user is not authorised to remove the message
                      
    Return value:
        Returns an empty dictionary {}
    '''
    # Check for valid token
    if not helper.is_valid_token(token):
        raise AccessError(description="Please enter a valid token")
    auth_user_id = helper.detoken(token)
    # Check if message_id is valid
    if not message_exists(message_id):
        raise InputError(description="message_id does not exist")
    # Check if message has already been removed
    msg = message_details(message_id)
    if is_message_deleted(msg):
        raise InputError(description="Message has already been deleted")
    # Check if user has permission to remove the message
    if not is_user_authorised(auth_user_id, message_id):
        raise AccessError(description="User is not authorised to remove the message")
        
    # Edit message details to show that it has been removed
    msg.update({'channel_id': -1})
    msg.update({'dm_id': -1})
    msg.update({'u_id': -1})
    msg.update({'message': ''})
    update_data()
    return {}

def message_edit_v1(token, message_id, message):
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
        AccessError - occurs when the user's token is not a valid token and when 
                      the user is not authorised to edit the message 
                      
    Return value:
        Returns an empty dictionary {}
    '''
    # Check for valid token
    if not helper.is_valid_token(token):
        raise AccessError(description="Please enter a valid token")
    auth_user_id = helper.detoken(token)
    # Check if message_id is valid
    if not message_exists(message_id):
        raise InputError(description="message_id does not exist")
    msg = message_details(message_id)
    # Check if message has already been removed
    if is_message_deleted(msg):
        raise InputError(description="Message has already been deleted")
    # Check if user has permission to remove the message
    if not is_user_authorised(auth_user_id, message_id):
        raise AccessError(description="User is not authorised to remove the message")
    # Check if edited message is longer than 1000 characters
    if len(message) > 1000:
        raise InputError(description="Message is longer than 1000 characters long")
    # If edited message is empty, the current message is removed
    if is_message_empty(message):
        edit_msg = message_details(message_id)
        edit_msg.update({'channel_id': -1})
        edit_msg.update({'dm_id': -1})
        edit_msg.update({'u_id': -1})
        edit_msg.update({'message': ''})
        edit_msg.update({'reacts': ''})
        edit_msg.update({'is_pinned': None})
    else:   
        edit_msg = message_details(message_id)
        edit_msg.update({'message': message})
    update_data()
    return {}

def message_share_v1(token, og_message_id, message, channel_id, dm_id):
    '''
    Function:
        Shares a message from a channel/DM to another channel/DM. An optional
        message can be added in addition to the original message 
        
    Arguments:
        token (str) - this is the token of a registered user during their
                      session
        og_message_id (int) - this is the ID of the original message being
                              shared
        message (str) - is the optional message in addition to the shared 
                        message
        channel_id (int) - is the ID of the channel that the message is being
                           shared to (is -1 if it is shared to a DM)
        dm_id (int) - is the ID of the DM that the message is being shared to 
                      (is -1 if it is shared to a channel)
                      
    Exceptions:
        InputError - occurs when the channel/DM ID is not a valid ID, when the 
                     og_message ID is not a valid ID, when the og_message has 
                     already been deleted and when the shared message is longer
                     than 1000 characters
        AccessError - occurs when the user's token is not a valid token and when 
                      the user is not a member of the channel/DM they are 
                      sharing the message to 
                      
    Return value:
        Returns a dictionary containing the type {shared_message_id}
    '''   
    # Check for valid token
    if not helper.is_valid_token(token):
        raise AccessError(description="Please enter a valid token")
    auth_user_id = helper.detoken(token)
    if channel_id != -1 and dm_id == -1:
        # Check for valid channel_id
        if not is_valid_channelid(channel_id):
            raise InputError(description="Please enter a valid channel_id")
        # Check if user has joined the channel
        if not helper.is_already_in_channel(auth_user_id, channel_id):
            raise AccessError(description="User is not a member in the channel they are sharing the message to")        
    else:
        # Check for valid dm_id
        if not helper.is_valid_dm_id(dm_id):
            raise InputError(description="Please enter a valid dm_id")
        # Check if user has joined the DM
        if not helper.is_already_in_dm(auth_user_id, dm_id):
            raise AccessError(description="User is not a member in the DM they are sharing the message to")
    # Check if og_message_id is valid
    if not message_exists(og_message_id):
        raise InputError(description="og_message_id does not exist")
    og_msg = message_details(og_message_id)
    # Check if og_message_id has been removed
    if is_message_deleted(og_msg):
        raise InputError(description="Message has already been deleted")
    # Check if og_message + optional message > 1000 characters
    if not is_message_empty(message):
        if len(og_msg['message']) + len(message) + 1 > 1000:
            raise InputError(description="Message is longer than 1000 characters")

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
        'reacts': og_msg['reacts'],
        'is_pinned': og_msg['is_pinned'],
    }
    data['messages'].append(msg)
    add_tag_notification(auth_user_id, channel_id, dm_id, msg['message'])
    update_data()
    return {'shared_message_id': message_id}

def message_senddm_v1(token, dm_id, message):
    '''
    Function:
        Send a message from authorised_user to the DM specified by dm_id. Note: 
        Each message has its own unique ID, regardless of whether it is in a 
        channel or a DM.
        
    Arguments:
        token (str) - this is the token of a registered user during their
                      session
        dm_id (int) - this is the ID of an existing DM
        message (str) - the message that will be sent to the DM with ID dm_id
        
    Exceptions:
        InputError - occurs when the dm ID is not a valid ID, when the
                     message being sent is empty and when the message has more
                     than 1000 characters
        AccessError - occurs when the user's token is not a valid token and when 
                      the user is not a member of the DM they are sending the 
                      message to 
                      
    Return value:
        Returns a dictionary containing the type {message_id}
    '''
    # Check for valid token
    if not helper.is_valid_token(token):
        raise AccessError(description="Please enter a valid token") 
    auth_user_id = helper.detoken(token) 
    # Check for valid dm_id
    if not helper.is_valid_dm_id(dm_id):
        raise InputError(description="Please enter a valid dm_id")       
    # Check if user is not in the DM
    if not helper.is_already_in_dm(auth_user_id, dm_id):
        raise AccessError(description="User is not a member in the DM they are sending the message to")
    # Check if message is empty
    if is_message_empty(message):
        raise InputError(description="Empty messages cannot be posted to DMs")
    # Check if message surpasses accepted length
    if len(message) > 1000:
        raise InputError(description="Message is longer than 1000 characters")
    
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
        'reacts': helper.create_reacts(),
        'is_pinned': None
    }
    data['messages'].append(message_info)
    add_tag_notification(auth_user_id, -1, dm_id, message)
    update_data()
    return {
        'message_id': message_id,
    }

def add_react(auth_user_id, reacts, react_id):
    for react in reacts:
        if react['react_id'] == react_id:
            react['u_ids'].append(auth_user_id)
    return reacts

def message_react_v1(token, message_id, react_id):
    '''
    Function:
        Given a message within a channel or DM the authorised user is part of, 
        add a "react" to that particular message
        
    Arguments:
        token (str) - this is the token of a registered user during their
                      session
        message_id (int) - this is the ID of the message the user wants to react to
        react_id (int) - this is the id of the type of react the user is using
        
    Exceptions:
        InputError - message_id is not a valid message within a channel or DM 
                     that the authorised user has joined
                   - react_id is not a valid React ID. The only valid react ID 
                     the frontend has is 1
                   - Message with ID message_id already contains an active React 
                     with ID react_id from the authorised user
        AccessError - The authorised user is not a member of the channel or DM 
                      that the message is within
                      
    Return value:
        Returns a dictionary containing the type {message_id}
    '''
    if not helper.is_valid_token(token):
        raise AccessError(description="Please enter a valid token") 
    auth_user_id = helper.detoken(token) 
    if not message_exists(message_id):
        raise InputError(description="Please select a valid message")
    if react_id not in REACTS:
        raise InputError(description="Please select a valid react")
    message = message_details(message_id)
    reacts = helper.get_reacts(auth_user_id, message['reacts'])
    if reacts[0]['is_this_user_reacted']:
        raise InputError(description="User has already reacted to this message")
    if message['channel_id'] != -1:
        user_found = helper.is_already_in_channel(auth_user_id, message['channel_id'])
    else:
        user_found = helper.is_already_in_dm(auth_user_id, message['dm_id'])
    if not user_found:
        raise AccessError(description="User is not in channel/dm")
    add_react(auth_user_id, reacts, react_id)
    update_data()
    return {}

