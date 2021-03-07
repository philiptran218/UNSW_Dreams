
from src.database import data
#from src.channels import channels_list_v1


def is_valid_uid(u_id):
    for user in data['users']:
        if user['u_id'] == u_id:
            return True
    return False


'''def is_valid_channelid(channel_id):
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
    selected_channel = None
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            selected_channel = channel
            break
            
    for members in selected_channel['all_members']:
        if members['u_id'] == u_id:
            return True
    return False

def is_owner_in_channel(u_id, channel_id):
    authorised_channels = channels_list_v1(u_id)
    for channel in authorised_channels['channels']:
        if channel['channel_id'] == channel_id:
            return True
    return False


def add_uid_to_channel(u_id, channel_id):
    first_name = None
    last_name = None
    for user in data.users:
        if user['u_id'] == u_id:
            first_name = user['name_first']
            last_name = user['name_last']
    new_member = {
                'u_id': u_id,
                'name_first': first_name,
                'name_last': last_name,
                }   
    for channel in data.channels:
        if channel['channel_id'] == channel_id:
            channel['all_members'].append(new_member)

def channel_name(channel_id):
    name = None
    for channel in data.channels:
        if channel['channel_id'] == channel_id:
            name = channel['name']
    return name

def channel_members(channel_id):
    list_of_members = []
    for channel in data.channels:
        if channel['channel_id'] == channel_id:
            list_of_members = channel['all_members']
    return list_of_members

def channel_owners(channel_id):
    list_of_owners = []
    for channel in data.channels:
        if channel['channel_id'] == channel_id:
            list_of_owners = channel['all_owners']
    return list_of_owners

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
   
    return message
'''
