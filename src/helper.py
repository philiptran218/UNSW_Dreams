from src.database import data, update_data
import jwt
import urllib.request
import sys

SECRET = 'COMP1531PROJECT'

def detoken(token):
    payload = jwt.decode(token, SECRET, algorithms=['HS256'])
    return payload['u_id']
    
def is_valid_token(token):
    for session in data['sessions']:
        if session['token'] == token:
            return True
    return False

def is_valid_uid(u_id): 
    for user in data['users']:
        if user['u_id'] == u_id:
            return True           
    return False

def is_valid_channelid(channel_id): 
    channel_found = False
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            channel_found = True       
    return channel_found  

# u_id and channel_id must be validated before running this function.
# (Functions that validate u_id and channel_id must be run before this function)
def is_already_in_channel(u_id, channel_id):
    selected_channel = None
    for channel in data['channels']:   
        if channel['channel_id'] == channel_id:
            selected_channel = channel
            
    for members in selected_channel['all_members']:
        if members['u_id'] == u_id:
            return True
    return False

# u_id and dm_id must be validated before running this function.
# (Functions that validate u_id and dm_id must be run before this function)
def is_already_in_dm(u_id, dm_id):
    selected_dm = None
    for dm in data['DM']:
        if dm['dm_id'] == dm_id:
            selected_dm = dm
    for members in selected_dm['dm_members']:
        if members['u_id'] == u_id:
            return True
    return False

def is_valid_dm_id(dm_id):
    if dm_id < 1:
        return False
    for dm in data['DM']:
        if dm['dm_id'] == dm_id:
            return True
    return False

# u_id and channel_id must be validated before running this function.
# (Functions that validate u_id and channel_id must be run before this function)
def is_already_channel_owner(u_id, channel_id):
    selected_channel = None
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            selected_channel = channel
            
    for member in selected_channel['owner_members']:
        if member['u_id'] == u_id:
            return True
    return False

# u_id and dm_id must be validated before running this function.
# (Functions that validate u_id and dm_id must be run before this function)
def is_dm_creator(u_id,dm_id):
    for dm in data['DM']:
        if dm['dm_id'] ==dm_id:
            if dm['dm_owner'] == u_id:
                return True
    return False

# u_id must be validated before running this function.
# (Functions that validate u_id must be run before this function)
def get_first_name(auth_user_id):
    first_name = None
    for user in data['users']:
        if user['u_id'] == auth_user_id:
            first_name = user['name_first']
    return first_name

# u_id must be validated before running this function.
# (Functions that validate u_id must be run before this function)
def get_last_name(auth_user_id):
    last_name = None
    for user in data['users']:
        if user['u_id'] == auth_user_id:
            last_name = user['name_last']
    return last_name

# u_id must be validated before running this function.
# (Functions that validate u_id must be run before this function)
def get_email(auth_user_id):
    email = None
    for user in data['users']:
        if user['u_id'] == auth_user_id:
            email = user['email']
    return email

# u_id must be validated before running this function.
# (Functions that validate u_id must be run before this function)
def get_handle(auth_user_id):
    handle = None
    for user in data['users']:
        if user['u_id'] == auth_user_id:
            handle = user['handle_str']
    return handle

# u_id must be validated before running this function.
# (Functions that validate u_id must be run before this function)
def get_reacts(auth_user_id, reacts):
    if auth_user_id in reacts[0]['u_ids']:
        reacts[0]['is_this_user_reacted'] = True
    else:
        reacts[0]['is_this_user_reacted'] = False
    return reacts

def create_reacts():
    return [{
        'react_id': 1,
        'u_ids': [],
        'is_this_user_reacted': None
    }]

# u_id must be validated before running this function.
# (Functions that validate u_id must be run before this function)
def find_permissions(u_id):
    user_found = None
    for user in data['users']:
        if user['u_id'] == u_id:
            user_found = user
            
    if user_found['perm_id'] == 1:
        return 1
    else:
        return 2

# u_id and channel_id must be validated before running this function.
# (Functions that validate u_id and channel_id must be run before this function)
def add_uid_to_channel(u_id, channel_id):
    new_member = {
                'u_id': u_id,
                'name_first': get_first_name(u_id),
                'name_last': get_last_name(u_id),
                'email': get_email(u_id),
                'handle_str': get_handle(u_id),
                }   
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            channel['all_members'].append(new_member)

# u_id and channel_id must be validated before running this function.
# (Functions that validate u_id and channel_id must be run before this function)
def add_owner_to_channel(u_id, channel_id):
    new_member = {
                'u_id': u_id,
                'name_first': get_first_name(u_id),
                'name_last': get_last_name(u_id),
                'email': get_email(u_id),
                'handle_str': get_handle(u_id),
                } 
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            channel['owner_members'].append(new_member)

# auth_user_id, u_id, channel_id and dm_id must be validated before running this function.
# (Functions that validate auth_user_id, u_id, channel_id and dm_id must be run before this function)            
def add_to_notifications(auth_user_id, u_id, channel_id, dm_id):
    notification = {
                    'auth_user_id': auth_user_id,
                    'u_id': u_id,
                    'channel_id': channel_id,
                    'dm_id': dm_id,
                    'type': 2,
                    'message': "",     
                }
    data['notifications'].append(notification)

