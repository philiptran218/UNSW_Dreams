OWNER = 1
MEMBER = 2

def channel_invite_v1(auth_user_id, channel_id, u_id):
    return {}

def channel_details_v1(auth_user_id, channel_id):
    return {}

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
    if helper.is_valid_uid(auth_user_id) == False:
        raise AccessError("Please enter a valid u_id")  
    # Check for valid channel_id
    if helper.is_valid_channelid(channel_id) == False:
        raise InputError("Please enter a valid channel_id")
    # Check if user is not in the channel
    if helper.is_already_in_channel(auth_user_id, channel_id) == False:
        raise AccessError("User is not a member of the channel")
    # Check if start is greater than number of messages
    if start > helper.get_len_messages(channel_id):
        raise InputError("Start is greater than the number of messages in the channel")    
    # If start is equal to number of messages
    if start == helper.get_len_messages(channel_id) :
        return {'messages': [], 'start': start, 'end': -1}
    
    # Setting the message limits and 'end' values
    if helper.get_len_messages(channel_id) - start <= 50:
        end = -1
        message_limit = helper.get_len_messages(channel_id)
    else:
        end = start + 50
        message_limit = end

    return {
        'messages': helper.list_of_messages(channel_id, start, message_limit),
        'start': start,
        'end': end,
    }        


def channel_leave_v1(auth_user_id, channel_id):
    return {
    }

def channel_join_v1(auth_user_id, channel_id):
    return {}
    

def channel_addowner_v1(auth_user_id, channel_id, u_id):
    return {
    }

def channel_removeowner_v1(auth_user_id, channel_id, u_id):
    return {
    }
    
