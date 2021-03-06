''' Helper functions for channel.py '''
from data import data

def is_valid_uid(u_id):

    for user in data['users']:
        if user['u_id'] == u_id:
            return True
            
    return False

def is_valid_channelid(channel_id):
    
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            return True
            
    return False
    
    
def find_permissions(u_id):
    
    for user in data['users']:
        if user['u_id'] == u_id:
            break
            
    if user['perm_id'] == 1:
        return 1
    else:
        return 2
        
    
def is_channel_public(channel_id):
    
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            break
    
    if channel['is_public']:
        return True
    else:
        return False
        
def is_already_in_channel(u_id, channel_id):

    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            break
            
    for members in channel['all_members']:
        if members['u_id'] == u_id:
            return True
    
    return False
    
def get_len_messages(channel_id):
    
    total = 0
    for message in data['messages']:
        if message['channel_id'] == channel_id:
            total += 1
            
    return total  

    
def add_uid_to_channel(u_id, channel_id):
    '''
    This function appends a user to a channel
    '''
    first_name = None
    last_name = None
    for user in data['users']:
        if user['u_id'] == u_id:
            first_name = user['name_first']
            last_name = user['name_last']
            
            new_member = {
                'u_id': u_id,
                'name_first': first_name,
                'name_last': last_name,
            }   
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            channel['all_members'].append(new_member)    
   
   
def add_owner_to_channel(u_id, channel_id):
    '''
    This function appends a user to a channel
    '''
    first_name = None
    last_name = None
    for user in data['users']:
        if user['u_id'] == u_id:
            first_name = user['name_first']
            last_name = user['name_last']
            
            new_member = {
                'u_id': u_id,
                'name_first': first_name,
                'name_last': last_name,
            }   
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            channel['owner_members'].append(new_member) 
            
def list_of_messages(channel_id, start, message_limit):
    # Reverse messages so most recent are at the beginning 
    ordered_messages = list(reversed(data['messages']))
    messages = []
    message_count = 0
    
    for message in ordered_messages:
        if message_count >= message_limit:
            break
        # Appends message if it's in the channel, and is from index 'start'
        if message['channel_id'] == channel_id and message_count >= start:
            message_details = {
                'message_id': message['message_id'],
                'u_id': message['u_id'],
                'message': message['message'],
                'time_created': message['time_created'],  
            }     
            messages.append(message_details)
        # Increments counter to keep track of number of messages appended
        if message['channel_id'] == channel_id: 
            message_count += 1
   
    return messages
   
