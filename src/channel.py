from src.channels import channels_listall_v1, channels_list_v1, channels_create_v1
from src.auth import auth_register_v1
from src.error import InputError, AccessError
import src.helper as helper
from src.database import data

def channel_invite_v1(auth_user_id, channel_id, u_id):
    '''
    Function:
        Invites a user (with user id u_id) to join a channel with ID channel_id. 
        Once invited the user is added to the channel immediately.

    Return Type:
        {}

    Exceptions:
        InputError when any of:
            - channel_id does not refer to a valid channel.
            - u_id does not refer to a valid user.
        AccessError when any of:
            - the authorised user is not already a member of the channel.
    ''' 
    if helper.is_valid_channelid(channel_id) == False:
        raise InputError("Please enter a valid channel_id")
    if helper.is_already_in_channel(auth_user_id, channel_id) == False:
        raise AccessError("Authorised user is not a member of the channel")
    if helper.is_valid_uid(u_id) == False:
        raise InputError("Please enter a valid u_id")
    if helper.is_already_in_channel(u_id, channel_id) == True:
        # If u_id is already in channel, u_id is not appended again.
        return {}
    else:
        # If inputs are valid and u_id is not in channel, append u_id to channel.
        helper.add_uid_to_channel(u_id, channel_id)
    return {}

def channel_details_v1(auth_user_id, channel_id):
    '''
    Function:
        Given a Channel with ID channel_id that the authorised user is part of, 
        provide basic details about the channel.

    Return Type:
        { name, owner_members, all_members }

    Exceptions:
        InputError when any of:
            - Channel ID is not a valid channel.
        AccessError when any of:
            - Authorised user is not a member of channel with channel_id.
    '''
    if helper.is_valid_channelid(channel_id) == False:
        raise InputError("Please enter a valid channel_id")
    if helper.is_already_in_channel(auth_user_id, channel_id) == False:
        raise AccessError("Please enter a valid u_id")
    channel_details = {}
    channel_details['name'] = helper.channel_name(channel_id)
    channel_details['owner_members'] = helper.channel_owners(channel_id)
    channel_details['all_members'] = helper.channel_members(channel_id)
    return channel_details

def channel_messages_v1(auth_user_id, channel_id, start):
    return {
    }
def channel_leave_v1(auth_user_id, channel_id):
    return {
    }

def channel_join_v1(auth_user_id, channel_id):
    return {
    }

def channel_addowner_v1(auth_user_id, channel_id, u_id):
    return {
    }

def channel_removeowner_v1(auth_user_id, channel_id, u_id):
    return {
    }