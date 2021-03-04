from error import InputError, AccessError
from data import data
from helper import is_valid_uid, is_valid_channelid, is_already_in_channel, get_len_messages, find_permissions, is_channel_public, add_uid_to_channel, add_uid_to_private_channel, list_of_messages

def channel_invite_v1(auth_user_id, channel_id, u_id):
    return {
    }

def channel_details_v1(auth_user_id, channel_id):
   
    return {
        'name': 'Hayden',
        'owner_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
    }

def channel_messages_v1(auth_user_id, channel_id, start):
    '''
    Function:
        Given a Channel with ID channel_id that the authorised user is part of, 
        return up to 50 messages between index  "start" and "start + 50". The
        function returns the newest messages first, followed by older messages.
        Also returns an "end" value, which is either "start + 50", or -1 if 
        there are no more messages in the channel to load.
       
    Arguments:
        auth_user_id (int) - this is the ID of a registered user
        channel_id (int) - this is the ID of a created channel
        start (int) - the beginning index for messages in a given channel
        
    Exceptions:
        InputError - occurs when the channel ID is not a valid channel and when
                     start is greater than the number of messages in the channel
        AccessError - occurs when the user ID is not a valid ID and when the
                      user is not a member in the given channel 
        
    Return Value:
        Returns a dictionary, where each dictionary contains types {message_id,
        u_id, message, time_created, start, end}
    '''
    
     # Check for valid u_id
    if is_valid_uid(auth_user_id) == False:
        raise AccessError()  
    # Check for valid channel_id
    if is_valid_channelid(channel_id) == False:
        raise InputError()
    # Check if user is not in the channel
    if is_already_in_channel(auth_user_id, channel_id) == False:
        raise AccessError()
    # Check if start is greater than number of messages
    if start > get_len_messages(channel_id):
        raise InputError()    
    # If start is equal to number of messages
    if start == get_len_messages(channel_id) :
        return {'messages': [], 'start': start, 'end': -1}
    
    # Setting the message limits and 'end' values
    if get_len_messages(channel_id) - start <= 50:
        end = -1
        message_limit = get_len_messages(channel_id)
    else:
        end = start + 50
        message_limit = end

    return {
        'messages': list_of_messages(channel_id, start, message_limit),
        'start': start,
        'end': end,
    }        


def channel_leave_v1(auth_user_id, channel_id):
    return {
    }

def channel_join_v1(auth_user_id, channel_id):
    '''
    Function:
        Given a channel_id of a channel that the authorised user can join, adds 
        them to that channel.
        
    Arguments:
        auth_user_id (int) - this is the ID of a registered user
        channel_id (int) - this is the ID of a created channel
    
    Exceptions:
        InputError - occurs when the channel ID is not a valid channel
        AccessError - occurs when the user ID is not a valid ID and when a non-
                      global user is attempting to join a private channel
        
    Return Value:
        Returns {} if successful or if the user is already in the channel
    '''
    
    # Check for valid u_id
    if is_valid_uid(auth_user_id) == False:
        raise AccessError("Please enter a valid u_id")
    # Check for valid channel_id
    if is_valid_channelid(channel_id) == False:
        raise InputError("Please enter a valid channel_id") 
    # Check if auth_user_id cannot join a private channel
    if find_permissions(auth_user_id) == 2 and is_channel_public(channel_id) == False:
        raise AccessError("Members cannot join a private channel")
    # If auth_user_id is already in the channel     
    if is_already_in_channel(auth_user_id, channel_id):
        return {}
        
    add_uid_to_channel(auth_user_id, channel_id)
    # Adding user into the owners list if they have global permissions
    if is_channel_public(channel_id) == False:
        add_uid_to_private_channel(auth_user_id, channel_id) 
    
    return {}
    

def channel_addowner_v1(auth_user_id, channel_id, u_id):
    return {
    }

def channel_removeowner_v1(auth_user_id, channel_id, u_id):
    return {
    }
        
