import src.helper as helper
from src.error import AccessError, InputError
from src.database import data
from src.helper import get_email, get_first_name, get_last_name, get_handle, is_valid_uid, is_valid_token, detoken 

#helper fucntion that checks if given dm_id is valid
def is_valid_dm_id(dm_id):
    for dm in data['DM']:
        if dm['dm_id'] == dm_id:
            return True
    return False

#helper fucntion that checks if a user in a given dm is the creator of it
def is_dm_creator(u_id,dm_id):
    for dm in data['DM']:
        if dm['dm_id'] ==dm_id:
            if dm['dm_owner'] == u_id:
                return True
    return False

#helper fucntion that checks if a user is part of the given dm
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

#helper fucntion that returns the number of messages in a given dm
def get_len_messages(dm_id):
    total = 0
    for message in data['messages']:
        if message['dm_id'] == dm_id:
            total += 1
    return total  

#helper fucntion that returns the number of messages to the limit, in a given dm
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

# Helper funciton to get the name of the dm.
def dm_name_generator(u_id):
    handles = []
    dm_name = ''

    for u in u_id:
        for user in data['users']:
            if user['u_id'] == u:
                handles.append(user['handle_str'])

    handles.sort()

    for handle in handles:
        if i == len(handles):
            dm_name = dm_name + handle
        else:
            dm_name = dm_name + handle + ", "

    return dm_name

def dm_details(token, dm_id):
    '''
    Function:
        Displays basic information about the dm.

    Arguments:
        token (str) - token of a registered user during their session
        dm_id (int) - this is the ID of the dm that the user is in

    Exceptions:
        InputError  - dm_id does not refer to a existing / valid dm.
        
        AccessError - when the user who calls the fucntion is not a valid user.
                    - the user who calls the fucntion is not a member of the dm

    Return Type:
        A dictionary is returned with the name and list of members inside dm.
    ''' 
    pass

def dm_list(token):
    '''
    Function:
       returns a list of DM's the user is a part of. 

    Arguments:
        token (str) - token of a registered user during their session

    Exceptions:     
        AccessError - the user who calls the fucntion is not a valid user.

    Return Type:
        This function returns the dms data type; a dictionary with dm_id and dm_name.
    ''' 
    pass

def dm_create(token, u_id):
    '''
    Function:
        creates a dm. Geenrates name based on handle strings of members.

    Arguments:
        token (str) - token of a registered user during their session
        u_id (list) - this is the ID of the user the dm is directed to. 

    Exceptions:
        InputError  - u_id does not refer to a existing / valid.

    Return Type:
        A dictionary is returned with the name and list of members inside dm.
    ''' 
    validator = is_valid_token(token)

    if validator == True:
    
        token_u_id = detoken(token)

        for id in u_id:
            if not is_valid_uid(u_id):
                raise AccessError('user_id is invalid')

        #This section grabs the handle of the person and appends it to the inputted list of u_id's
        #It assumes token works, as testing occurs after this point. Code places owners u_id first
        #in the list. This makes it easier when creating the dm later in the function.

        for member in data['users']:
            if member['u_id'] == token_u_id:
                [u_id].insert(0,token_u_id)
    
        dm_name = dm_name_generator([u_id])

        dm_id = len(data['DM'])+1
        new_dm = {
            'dm_id': dm_id,
            'dm_owner': token_u_id,
            'name':dm_name,
            'dm_members':[],
        }

        for id in [u_id]:
            new_dm['dm_members'].append(
                {
                    'u_id':id,
                    'name_first':get_first_name(id),
                    'name_last' :get_last_name(id),
                    'email': get_email(id),
                    'handle_str': get_handle(id),
                }
            )

        data['DM'].append(new_dm)

        return {
            'dm_id': dm_id,
            'dm_name': dm_name
        }
    else:
        raise AccessError('Invalid Token')


def dm_invite_v1(token, dm_id, u_id):
    '''
    Function:
        Invites a user to an existing dm

    Arguments:
        token (str) - token of a registered user during their session
        dm_id (int) - this is the ID of the dm that the user is invited to
        u_id (int) - this is the ID of a user to be invited

    Exceptions:
        InputError  - dm_id does not refer to a existing dm.
                    - u_id does not refer to a valid user.
        AccessError when any of: 
                    - the authorised user is not already a member of the DM.

    Return Type:
        This function doesn't return any data.
    ''' 
    token_u_id = detoken(token)
    #checking if the dm  has a valid dm_id
    if not is_valid_dm_id(dm_id) :
        raise InputError("dm_id does not refer to an existing dm")
    #checking if the user is a member of the dm
    if not is_already_in_dm(token_u_id, dm_id):
        raise AccessError("Authorised user is not a member of the dm")
    #checking if user who called fucntion has a valid u_id
    if not helper.is_valid_uid(u_id) :
        raise InputError("Please enter a valid u_id")
    #checking if the user is in the dm, if they are , nothing is done.
    if is_already_in_dm(u_id, dm_id):
        return {}
    
    invited_member = {
                    'u_id': u_id,
                    'name_first': helper.get_first_name(u_id),
                    'name_last': helper.get_last_name(u_id),
                    'email': helper.get_email(u_id),
                    'handle_str': helper.get_handle(u_id),
                     }
    for dm in data['DM']:
        if dm['dm_id'] == dm_id:
            dm['dm_members'].append(invited_member)
            return{}


def dm_remove_v1(token,dm_id):
    '''
    Function:
        removes a dm from list of dm

    Arguments:
        token (str) - token of a registered user during their session
        dm_id (int) - this is the ID of the dm that the user is invited to

    Exceptions:
        InputError  - dm_id does not refer to a existing dm.
        
        AccessError when any of: 
                    - the user who calls the fucntion is not a valid user.
                    - the user who calls the fucntion is not the original dm creator

    Return Type:
        This function doesn't return any data.
    ''' 
    u_id = detoken(token)# yet to be completed

    #checking if user who called fucntion has a valid u_id
    if not helper.is_valid_uid(u_id):
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
