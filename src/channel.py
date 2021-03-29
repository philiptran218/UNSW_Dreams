from src.channels import channels_listall_v1, channels_list_v1, channels_create_v1
from src.auth import auth_register_v1
from src.error import InputError, AccessError
import src.helper as helper
from src.database import data

OWNER = 1
MEMBER = 2

def is_valid_channelid(channel_id): 
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            return True       
    return False     

def is_channel_public(channel_id):
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            break
    
    if channel['is_public']:
        return True
    else:
        return False

def is_already_in_channel(u_id, channel_id):
    selected_channel = None
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            selected_channel = channel
            break
            
    for members in selected_channel['all_members']:
        if members['u_id'] == u_id:
            return True
    return False

def channel_name(channel_id):
    name = None
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            name = channel['name']
    return name

def channel_members(channel_id):
    list_of_members = []
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            list_of_members = channel['all_members']
    return list_of_members

def channel_owners(channel_id):
    list_of_owners = []
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            list_of_owners = channel['owner_members']
    return list_of_owners

def channel_invite_v1(token, channel_id, u_id):
    '''
    Function:
        Invites a user (with user id u_id) to join a channel with ID channel_id. 
        Once invited the user is added to the channel immediately.

    Arguments:
        auth_user_id (int) - this is the ID of a registered user
        channel_id (int) - this is the ID of a created channel
        u_id (int) - this is the ID of a user

    Exceptions:
        InputError when any of:
            - channel_id does not refer to a valid channel.
            - u_id does not refer to a valid user.
        AccessError when any of:
            - the authorised user is not already a member of the channel.

    Return Type:
        This function doesn't return any value.
    ''' 
    if helper.is_valid_token(token) == False:
        raise InputError("Please enter a valid token")
    auth_user_id = helper.detoken(token)
    if is_valid_channelid(channel_id) == False:
        raise InputError("Please enter a valid channel_id")
    if is_already_in_channel(auth_user_id, channel_id) == False:
        raise AccessError("Authorised user is not a member of the channel")
    if is_already_in_channel(u_id, channel_id) == True:
        # If u_id is already in channel, u_id is not appended again.
        return {}
    else:
        # If inputs are valid and u_id is not in channel, append u_id to channel.
        helper.add_uid_to_channel(u_id, channel_id)
        helper.add_to_notifications(auth_user_id, u_id, channel_id, -1)
    return {}

def channel_details_v1(token, channel_id):
    '''
    Function:
        Given a Channel with ID channel_id that the authorised user is part of, 
        provide basic details about the channel.

    Arguments:
        auth_user_id (int) - this is the ID of a registered user
        channel_id (int) - this is the ID of a created channel

    Exceptions:
        InputError when any of:
            - Channel ID is not a valid channel.
        AccessError when any of:
            - Authorised user is not a member of channel with channel_id.

    Return Type:
        { name, owner_members, all_members }
    '''
    if helper.is_valid_token(token) == False:
        raise AccessError("Please enter a valid token")
    auth_user_id = helper.detoken(token)
    if is_valid_channelid(channel_id) == False:
        raise InputError("Please enter a valid channel_id")
    if is_already_in_channel(auth_user_id, channel_id) == False:
        raise AccessError("Please enter a valid u_id")
    channel_details = {}
    channel_details['name'] = channel_name(channel_id)
    channel_details['owner_members'] = channel_owners(channel_id)
    channel_details['all_members'] = channel_members(channel_id)
    return channel_details

def get_len_messages(channel_id):
    total = 0
    for message in data['messages']:
        if message['channel_id'] == channel_id:
            total += 1
            
    return total  

def list_of_messages(channel_id, start, message_limit):
    # Reverse messages so most recent are at the beginning 
    ordered_messages = list(reversed(data['messages']))
    messages = []
    message_count = 0
    
    # Appending messages from the given channel_id
    for message in ordered_messages:
        if message_count >= message_limit:
            break
            
        if message['channel_id'] == channel_id and message_count >= start:
            message_details = {
                'message_id': message['message_id'],
                'u_id': message['u_id'],
                'message': message['message'],
                'time_created': message['time_created'],  
            }     
            messages.append(message_details)
        
        if message['channel_id'] == channel_id: 
            message_count += 1
   
    return messages

def channel_messages_v1(token, channel_id, start):
    '''
    Function:
        Given a Channel with ID channel_id that the authorised user is part of, 
        return up to 50 messages between index  "start" and "start + 50". The
        function returns the newest messages first, followed by older messages.
        Also returns an "end" value, which is either "start + 50", or -1 if 
        there are no more messages in the channel to load.
       
    Arguments:
        token (str) - this is the token of a registered user during their 
                      session
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
    
    # Check for valid token
    if not helper.is_valid_token(token):
        raise AccessError("Please enter a valid token") 
    auth_user_id = helper.detoken(token) 
    # Check for valid channel_id
    if not is_valid_channelid(channel_id):
        raise InputError("Please enter a valid channel_id")
    # Check if user is not in the channel
    if not is_already_in_channel(auth_user_id, channel_id):
        raise AccessError("User is not a member of the channel")
    # Check if start is greater than number of messages
    if start > get_len_messages(channel_id):
        raise InputError("Start is greater than the number of messages in the channel")    
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

def find_permissions(u_id):
    for user in data['users']:
        if user['u_id'] == u_id:
            break
            
    if user['perm_id'] == 1:
        return 1
    else:
        return 2

def channel_join_v1(token, channel_id):
    '''
    Function:
        Given a channel_id of a channel that the authorised user can join, adds 
        them to that channel.
        
    Arguments:
        token (str) - this is the token of a registered user during their 
                      session
        channel_id (int) - this is the ID of a created channel
    
    Exceptions:
        InputError when any of:
            - channel_id does not refer to a valid channel.
        AccessError when any of:
            - the authorised user is not already a member of the channel.
        
    Return Value:
        Returns {} if successful or if the user is already in the channel
    '''
    
    # Check for valid token
    if not helper.is_valid_token(token):
        raise AccessError("Please enter a valid token")
    auth_user_id = helper.detoken(token)
    # Check for valid channel_id
    if not is_valid_channelid(channel_id):
        raise InputError("Please enter a valid channel_id") 
    # Check if auth_user_id cannot join a private channel
    if find_permissions(auth_user_id) == MEMBER and not is_channel_public(channel_id):
        raise AccessError("Members cannot join a private channel")
    # If auth_user_id is already in the channel     
    if is_already_in_channel(auth_user_id, channel_id):
        return {}
        
    helper.add_uid_to_channel(auth_user_id, channel_id)
    # Adding user into the owners list if they have global permissions
    if find_permissions(auth_user_id) == OWNER:
        helper.add_owner_to_channel(auth_user_id, channel_id) 
  
    return {}
    
def channel_addowner_v1(auth_user_id, channel_id, u_id):
    return {
    }

def channel_removeowner_v1(auth_user_id, channel_id, u_id):
    return {
    }
