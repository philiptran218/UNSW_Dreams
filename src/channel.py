from src.channels import channels_listall_v1, channels_list_v1, channels_create_v1
from src.auth import auth_register_v1
from src.error import InputError, AccessError
import src.helper as helper
from src.database import data
from datetime import timezone, datetime

OWNER = 1
MEMBER = 2
CHANNEL = 2   

def is_channel_public(channel_id):
    channel_found = None
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            channel_found = channel
    
    if channel_found['is_public']:
        return True
    else:
        return False

def is_already_channel_owner(u_id, channel_id):
    selected_channel = None
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            selected_channel = channel
            
    for member in selected_channel['owner_members']:
        if member['u_id'] == u_id:
            return True
    return False

def is_already_in_channel(u_id, channel_id):
    selected_channel = None
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            selected_channel = channel
            
    for member in selected_channel['all_members']:
        if member['u_id'] == u_id:
            return True
    return False

def is_only_owner_in_channel(u_id, channel_id):
    selected_channel = None
    owner_found = False
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            selected_channel = channel
            
    for member in selected_channel['owner_members']:
        if member['u_id'] == u_id:
            owner_found = True
    if owner_found == True and len(selected_channel['owner_members']) == 1:
        return True
    return False

def remove_channel_owner(u_id, channel_id):
    selected_channel = None
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            selected_channel = channel
 
    for member in selected_channel['owner_members']:
        if member['u_id'] == u_id:
            selected_channel['owner_members'].remove(member)

def channel_name(channel_id):
    name = None
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            name = channel['name']
    return name

def channel_is_public(channel_id):
    is_public = None
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            is_public = channel['is_public']
    return is_public

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

def remove_user(u_id, channel_id):
    selected_channel = None
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            selected_channel = channel
 
    for member in selected_channel['owner_members']:
        if member['u_id'] == u_id:
            selected_channel['owner_members'].remove(member)
            
    for member in selected_channel['all_members']:
        if member['u_id'] == u_id:
            selected_channel['all_members'].remove(member)

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
    if not helper.is_valid_token(token):
        raise AccessError(description="Please enter a valid token")
    auth_user_id = helper.detoken(token)
    if not helper.is_valid_channelid(channel_id):
        raise InputError(description="Please enter a valid channel")
    if helper.find_permissions(auth_user_id) == OWNER:
        # If auth_user_id is the global owner, they can invite the u_id.
        pass
    elif not is_already_in_channel(auth_user_id, channel_id):
        raise AccessError(description="User is not authorised")
    if not helper.is_valid_uid(u_id):
        raise InputError(description="Please enter a valid user")
    if is_already_in_channel(u_id, channel_id):
        # If u_id is already in channel, u_id is not appended again.
        return {}
    else:
        # If inputs are valid and u_id is not in channel, append u_id to channel.
        helper.add_uid_to_channel(u_id, channel_id)
    if helper.find_permissions(u_id) == OWNER:
        helper.add_owner_to_channel(u_id, channel_id)
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
        { name, is_public, owner_members, all_members }
    '''
    if not helper.is_valid_token(token):
        raise AccessError(description="Please enter a valid token")
    auth_user_id = helper.detoken(token)
    if not helper.is_valid_channelid(channel_id):
        raise InputError(description="Please enter a valid channel")
    if helper.find_permissions(auth_user_id) == OWNER:
     # If auth_user_id is the global owner, they can access channel details.
        pass
    elif not is_already_in_channel(auth_user_id, channel_id):
        raise AccessError(description="User is not authorised")
    channel_details = {}
    channel_details['name'] = channel_name(channel_id)
    channel_details['is_public'] = channel_is_public(channel_id)
    channel_details['owner_members'] = channel_owners(channel_id)
    channel_details['all_members'] = channel_members(channel_id)
    return channel_details

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
    if not helper.is_valid_token(token):
        raise AccessError(description="Please enter a valid token")
    auth_user_id = helper.detoken(token)  
    # Check for valid channel_id
    if not helper.is_valid_channelid(channel_id):
        raise InputError(description="Please enter a valid channel_id")
    # Check if user is not in the channel
    if not is_already_in_channel(auth_user_id, channel_id):
        raise AccessError(description="User is not a member of the channel")
    # Check if start is greater than number of messages
    if start > get_len_messages(channel_id):
        raise InputError(description="Start is greater than the number of messages in the channel")    
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

def channel_leave_v1(token, channel_id):
    '''
    Function:
        Given a channel ID, the user removed as a member of this channel. Their 
        messages should remain in the channel.
        
    Arguments:
        auth_user_id (int) - this is the ID of a registered user
        channel_id (int) - this is the ID of a created channel
    
    Exceptions:
        InputError when any of:
            - Channel_id does not refer to a valid channel.
        AccessError when any of:
            - Authorised user is not a member of channel with channel_id.
        
    Return Value:
        Returns {} if successful
    '''
    if not helper.is_valid_token(token):
        raise AccessError(description="Please enter a valid token")
    auth_user_id = helper.detoken(token)
    if not helper.is_valid_channelid(channel_id):
        raise InputError(description="Please enter a valid channel")
    if not is_already_in_channel(auth_user_id, channel_id):
        raise AccessError(description="Please enter a valid user")
    remove_user(auth_user_id, channel_id)
    return {
    }

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
    if not helper.is_valid_token(token):
        raise AccessError(description="Please enter a valid token")
    auth_user_id = helper.detoken(token)
    # Check for valid channel_id
    if not helper.is_valid_channelid(channel_id):
        raise InputError(description="Please enter a valid channel_id") 
    # Check if auth_user_id cannot join a private channel
    if helper.find_permissions(auth_user_id) == MEMBER and not is_channel_public(channel_id):
        raise AccessError(description="Members cannot join a private channel")
    # If auth_user_id is already in the channel     
    if is_already_in_channel(auth_user_id, channel_id):
        return {}
        
    helper.add_uid_to_channel(auth_user_id, channel_id)
    # Adding user into the owners list if they have global permissions
    if helper.find_permissions(auth_user_id) == OWNER:
        helper.add_owner_to_channel(auth_user_id, channel_id) 
  
    return {}
    
def channel_addowner_v1(token, channel_id, u_id):
    '''
    Function:
        Given a Channel with ID channel_id that the authorised user is an owner 
        of, make user with id "u_id" an owner of the channel.

    Arguments:
        auth_user_id (int) - this is the ID of a registered user
        channel_id (int) - this is the ID of a created channel
        u_id (int) - this is the ID of the member of the channel becoming an owner.

    Exceptions:
        InputError when any of:
            - Channel ID is not a valid channel.
            - User with user id u_id is already an owner of the channel
        AccessError when any of:
            - Authorised user is not an owner of the **Dreams**, or an owner of 
              this channel

    Return Type:
        {}
    '''
    if not helper.is_valid_token(token):
        raise AccessError(description="Please enter a valid token")
    auth_user_id = helper.detoken(token)
    if not helper.is_valid_channelid(channel_id):
        raise InputError(description="Please enter a valid channel")
    if is_already_channel_owner(u_id, channel_id):
        raise InputError(description="User is already an owner of the channel")
    if helper.find_permissions(auth_user_id) == OWNER:
        # If auth_user_id is the global owner, they can add owner.
        pass
    elif not is_already_channel_owner(auth_user_id, channel_id):
        raise AccessError(description="User is not authorised")
    if not is_already_in_channel(u_id, channel_id):
        raise AccessError(description="Please enter a valid user")
    helper.add_owner_to_channel(u_id, channel_id)
    return {
    }

def channel_removeowner_v1(token, channel_id, u_id):
    '''
    Function:
        Given a Channel with ID channel_id that the authorised user is an owner 
        of, remove owner status of user with id "u_id" in the channel.

    Arguments:
        auth_user_id (int) - this is the ID of a registered user
        channel_id (int) - this is the ID of a created channel
        u_id (int) - this is the ID of the member of the channel becoming an owner.

    Exceptions:
        InputError when any of:
            - Channel ID is not a valid channel.
            - User with user id u_id is not an owner of the channel
            - User with user id auth_user_id is the only owner in the channel
        AccessError when any of:
            - Authorised user is not an owner of the **Dreams**, or an owner of 
              this channel

    Return Type:
        {}
    '''
    if not helper.is_valid_token(token):
        raise AccessError(description="Please enter a valid token")
    auth_user_id = helper.detoken(token) 
    if not helper.is_valid_uid(u_id):
        raise AccessError(description="Please enter a valid user") 
    if not helper.is_valid_channelid(channel_id):
        raise InputError(description="Please enter a valid channel")
    if not is_already_channel_owner(u_id, channel_id):
        raise InputError(description="User is not an owner of the channel")
    if is_only_owner_in_channel(auth_user_id, channel_id):
        raise InputError(description="User is currently the only owner")
    if helper.find_permissions(auth_user_id) == OWNER:
        # If auth_user_id is the global owner, they can add owner.
        pass
    elif not is_already_in_channel(auth_user_id, channel_id):
        raise AccessError(description="User is not an owner of the channel")
    elif not is_already_channel_owner(auth_user_id, channel_id):
        raise InputError(description="User is not authorised")
    remove_channel_owner(u_id, channel_id)
    return {
    }
