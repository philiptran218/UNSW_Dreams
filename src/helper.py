from src.database import data
import jwt

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

def get_first_name(auth_user_id):
    first_name = None
    for user in data['users']:
        if user['u_id'] == auth_user_id:
            first_name = user['name_first']
    return first_name

def get_last_name(auth_user_id):
    last_name = None
    for user in data['users']:
        if user['u_id'] == auth_user_id:
            last_name = user['name_last']
    return last_name

def get_email(auth_user_id):
    email = None
    for user in data['users']:
        if user['u_id'] == auth_user_id:
            email = user['email']
    return email

def get_handle(auth_user_id):
    handle = None
    for user in data['users']:
        if user['u_id'] == auth_user_id:
            handle = user['handle_str']
    return handle

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

def add_owner_to_channel(u_id, channel_id):
    '''
    This function appends a user to a channel
    '''
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
            
def add_to_notifications(auth_user_id, u_id, channel_id, dm_id):
    notification = {
                    'auth_user_id': auth_user_id,
                    'u_id': u_id,
                    'channel_id': channel_id,
                    'dm_id': dm_id,
                    'type': 2,
                    'message': None,     
                }
    data['notifications'].append(notification)

