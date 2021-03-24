from src.helper import is_valid_uid
from src.error import AccessError, InputError
from src.database import data

def is_valid_dm_id(dm_id):
    for dm in data['DM']:
        if dm['dm_id'] == dm_id:
            return True
    return False

def is_dm_creator(u_id,dm_id):
    for dm in data['DM']:
        if dm['dm_id'] ==dm_id:
            if dm['dm_owner'] == u_id:
                return True
    return False

def dm_remove_v1(token,dm_id):
    u_id = detoken(token)# yet to be completed

    #checking if user who called fucntion has a valid u_id
    if not is_valid_uid(u_id):
        raise AccessError('user_id is invalid')
    #checking if the dm to be removed has a valid dm_id
    if not is_valid_dm_id(dm_id):
        raise InputError('dm_id is invalid')
    #checking if the user who called the fucntion is the original dm creator
    if not is_dm_creator(u_id,dm_id):
        raise AccessError('user is not original dm creator')
    
    for dm in data['DM']:
        if dm['dm_id'] == dm_id:
            dm.update({'dm_id' : -1})
            dm.update({'dm_name':''})
            dm.update({'dm_members':[]})
    return {}
    

'''an input error is raaised when the dm id is invalid

access error when the user is not the orgeinal creatoe



is Dm id valid ->>>> create based on u id
is the  token of the user calling the fuicntion similar to
             the token of the user who created
             it?
try to match u id from the token given to the owner firld inside dm'''

def is_already_in_dm(u_id, dm_id):
    selected_dm = None
    for dm in data['DM']:
        if dm['dm_id'] == dm_id:
            selected_dm = dm
            break
            
    for members in selected_dm['dm_members']:
        if members['u_id'] == u_id:
            return True
    return False

def get_len_messages(dm_id):
    total = 0
    for message in data['messages']:
        if message['dm_id'] == dm_id:
            total += 1
    return total  

def list_of_messages(dm_id, start, message_limit):
    # Reverse messages so most recent are at the beginning 
    ordered_messages = list(reversed(data['messages']))
    messages = []
    message_count = 0
    
    # Appending messages from the given dm_id
    for message in ordered_messages:
        if message_count >= message_limit:
            break
            
        if message['dm_id'] == dm_id and message_count >= start:
            message_details = {
                'message_id': message['message_id'],
                'u_id': message['u_id'],
                'message': message['message'],
                'time_created': message['time_created'],  
            }     
            messages.append(message_details)
        
        if message['dm_id'] == dm_id: 
            message_count += 1
   
    return messages

def dm_messages_v1(token, dm_id, start):
    '''
    Function:
        Given a DM with ID dm_id that the authorised user is part of, 
        return up to 50 messages between index "start" and "start + 50".
        Message with index 0 is the most recent message in the channel. 
        This function returns a new index "end" which is the value of "
        start + 50", or, if this function has returned the least recent 
        messages in the channel, returns -1 in "end" to indicate there 
        are no more messages to load after this return.
    
    Arguments:
        token (str) - this is the token of a registered user during their session
        dm_id (int) - this is the ID of a created dm
        start (int) - the beginning index for messages in a given dm
        
    Exceptions:
        InputError - occurs when the dm ID is not for valid dm and when
                     start is greater than the number of messages in the dm
        AccessError - occurs when the token is not a valid token and when the
                      user is not a member in the given dm
        
    Return Value:
        Returns a dictionary, where each dictionary contains types {message_id,
        u_id, message, time_created, start, end}
    '''
    u_id = detoken(token)
     # Check for valid u_id
    if not helper.is_valid_uid(u_id):
        raise AccessError("invalid user_id")  
   
   
    # Check for valid dm id 
    if not is_valid_dm_id(dm_id): 
        raise InputError("Please enter a valid channel_id")
  
   
    # Check if user is a member of the dm
    if not is_already_in_dm(u_id, dm_id): 
        raise AccessError("User is not a member of this dm")
   
   
    # Check if start is greater than number of messages
    if start > get_len_messages(dm_id):  
        raise InputError("Start is greater than the number of messages in the dm")    
   
   
    # If start is equal to number of messages
    if start == get_len_messages(dm_id) :
        return {'messages': [], 'start': start, 'end': -1}
    
    

    # Setting the message limits and 'end' values
    if get_len_messages(dm_id) - start <= 50:
        end = -1
        message_limit = get_len_messages(dm_id)
    else:
        end = start + 50
        message_limit = end

    return {
        'messages': list_of_messages(dm_id, start, message_limit),
        'start': start,
        'end': end,
    }      

