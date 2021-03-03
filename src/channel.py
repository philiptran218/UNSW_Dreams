from channels import channels_listall_v1, channels_list_v1
import data

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
    valid_channels = channels_listall_v1(auth_user_id)
        if channel_id not in valid_channels
            raise Exception(InputError)
    authorised_channels = channels_list_v1(auth_user_id)
        if channel_id not in authorised_channels
            raise Exception(AccessError)
    valid_uids = data.uid_listall_v1()
        if u_id not in valid_uids
            raise Exception(InputError)
    channel_details = channel_details_v1(auth_user_id, channel_id)
    if u_id in channel_details['owner_memebers'] or u_id in channel_details['owner_memebers']:
        return {}
    else:
        data.add_uid_to_channel(u_id, channel_id)
    return {}

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

'''
Function:
    Given a Channel with ID channel_id that the authorised user is part of, 
    return up to 50 messages between index "start" and "start + 50". Message 
    with index 0 is the most recent message in the channel. This function 
    returns a new index "end" which is the value of "start + 50", or, if this 
    function has returned the least recent messages in the channel, returns -1 
    in "end" to indicate there are no more messages to load after this return.

Return Type:
    { messages, start, end }

Exceptions:
    InputError when any of:
        - Channel ID is not a valid channel.
        - Start is greater than the total number of messages in the channel.
    AccessError when any of:
        - Authorised user is not a member of channel with channel_id.
'''
def channel_messages_v1(auth_user_id, channel_id, start):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
        'start': 0,
        'end': 50,
    }

def channel_leave_v1(auth_user_id, channel_id):
    return {
    }

'''
Function:
    Given a channel_id of a channel that the authorised user can join, adds them 
    to that channel

Return Type:
    {}

Exceptions:
    InputError when any of:
        - Channel ID is not a valid channel.
    AccessError when any of:
        - channel_id refers to a channel that is private (when the authorised 
          user is not a global owner).
'''
def channel_join_v1(auth_user_id, channel_id):
    return {
    }

def channel_addowner_v1(auth_user_id, channel_id, u_id):
    return {
    }

def channel_removeowner_v1(auth_user_id, channel_id, u_id):
    return {
    }