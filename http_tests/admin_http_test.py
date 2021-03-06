import pytest
import requests
import json
from src import config

INVALID_TOKEN = -1
INVALID_CHANNEL_ID = -1
INVALID_DM_ID = -1
INVALID_U_ID = -1
INVALID_PERM_ID = -1

OWNER = 1
MEMBER = 2

INPUTERROR = 400
ACCESSERROR = 403


@pytest.fixture
def user_1():
    user = requests.post(config.url + 'auth/register/v2', json={
        'email': 'johnsmith@gmail.com',
        'password': 'goodpass',
        'name_first': 'John',
        'name_last': 'Smith'
    })
    return user.json()
    
@pytest.fixture
def user_2():
    user = requests.post(config.url + 'auth/register/v2', json={
        'email': 'philtran@gmail.com',
        'password': 'goodpass',
        'name_first': 'Philip',
        'name_last': 'Tran'
    })
    return user.json()
    
@pytest.fixture
def channel_1(user_1):
    channel = requests.post(config.url + 'channels/create/v2', json={
        'token': user_1['token'],
        'name': 'Channel1',
        'is_public': True
    })
    channel_info = channel.json()
    return channel_info['channel_id']

@pytest.fixture
def priv_channel_1(user_1):
    channel = requests.post(config.url + 'channels/create/v2', json={
        'token': user_1['token'],
        'name': 'Channel1',
        'is_public': False
    })
    channel_info = channel.json()
    return channel_info['channel_id']

@pytest.fixture 
def clear_database():
    requests.delete(config.url + 'clear/v1')

################################################################################
# admin_user_remove http tests                                                 #
################################################################################

def test_admin_user_remove_invalid_token(clear_database, user_1):
    msg = requests.delete(config.url + 'admin/user/remove/v1', json={
        'token': INVALID_TOKEN,
        'u_id': user_1['auth_user_id'],
    })
    assert msg.status_code == ACCESSERROR

def test_admin_user_remove_invalid_u_id(clear_database, user_1):
    msg = requests.delete(config.url + 'admin/user/remove/v1', json={
        'token': user_1['token'],
        'u_id': INVALID_U_ID,
    })
    assert msg.status_code == INPUTERROR

def test_admin_user_remove_invalid_only_owner(clear_database, user_1):
    msg = requests.delete(config.url + 'admin/user/remove/v1', json={
        'token': user_1['token'],
        'u_id': user_1['auth_user_id'],
    })
    assert msg.status_code == INPUTERROR

def test_admin_user_remove_invalid_not_owner(clear_database, user_1, user_2):
    msg = requests.delete(config.url + 'admin/user/remove/v1', json={
        'token': user_2['token'],
        'u_id': user_1['auth_user_id'],
    })
    assert msg.status_code == ACCESSERROR

def test_admin_user_remove_valid(clear_database, user_1, user_2, channel_1):
    
    #To test this funciton. User 2 needs to first join a channel and send a message.
    #After funciton is performed: two things must occur:
    #   1: User's name must be changed to "Removed User" - tested through user/profile
    #   2: User's messages must be changed to "Removed User"

    requests.post(config.url + 'channel/join/v2', json={
        'token': user_2['token'],
        'channel_id': channel_1
    })

    channel_msg = requests.post(config.url + 'message/send/v2', json={
        'token': user_2['token'],
        'channel_id': channel_1,
        'message': 'I just joined!!'
    })
    
    requests.delete(config.url + 'admin/user/remove/v1', json={
        'token': user_1['token'],
        'u_id': user_2['auth_user_id'],
    })

    users = requests.get(f"{config.url}user/profile/v2?token={user_1['token']}&u_id={user_2['auth_user_id']}")
    users_info = users.json()
    assert users_info['user']['name_first'] == 'Removed'
    assert users_info['user']['name_last'] == 'user'

    channel_msg = requests.get(f"{config.url}channel/messages/v2?token={user_2['token']}&channel_id={channel_1}&start=0") 
    msg_info = channel_msg.json()
    assert msg_info['messages'][0]['message'] == 'Removed user'
 
################################################################################
# admin_userpermission_change http tests                                       #
################################################################################

def test_admin_userpermission_change_invalid_token(clear_database, user_1):
    msg = requests.post(config.url + 'admin/userpermission/change/v1', json={
        'token': INVALID_TOKEN,
        'u_id': user_1['auth_user_id'],
        'permission_id': OWNER
    })
    assert msg.status_code == ACCESSERROR

def test_admin_userpermission_change_invalid_u_id(clear_database, user_1):
    msg = requests.post(config.url + 'admin/userpermission/change/v1', json={
        'token': user_1['token'],
        'u_id': INVALID_U_ID,
        'permission_id': OWNER
    })
    assert msg.status_code == INPUTERROR

def test_admin_userpermission_change_invalid_perm_id(clear_database, user_1):
    msg = requests.post(config.url + 'admin/userpermission/change/v1', json={
        'token': user_1['token'],
        'u_id': user_1['auth_user_id'],
        'permission_id': INVALID_PERM_ID
    })
    assert msg.status_code == INPUTERROR

def test_admin_userpermission_change_invalid_not_owner(clear_database, user_1, user_2):
    msg = requests.post(config.url + 'admin/userpermission/change/v1', json={
        'token': user_2['token'],
        'u_id': user_1['auth_user_id'],
        'permission_id': OWNER
    })
    assert msg.status_code == ACCESSERROR

def test_admin_userpermission_change_valid(clear_database, user_1, user_2, priv_channel_1):
    
    #To test this funciton. User 2 (a member) must try to enter a private channel.
    #The first time they fail, but after the function is performed, they should succeed.

    msg = requests.post(config.url + 'channel/join/v2', json={
        'token': user_2['token'],
        'channel_id': priv_channel_1
    })
    assert msg.status_code == ACCESSERROR
    
    requests.post(config.url + 'admin/userpermission/change/v1', json={
        'token': user_1['token'],
        'u_id': user_2['auth_user_id'],
        'permission_id': OWNER
    })

    requests.post(config.url + 'channel/join/v2', json={
        'token': user_2['token'],
        'channel_id': priv_channel_1
    })

    channel = requests.get(f"{config.url}channel/details/v2?token={user_2['token']}&channel_id={priv_channel_1}")
    channel_details = channel.json()
    user_2_id = channel_details['all_members'][1]['u_id']
    user_2_profile_json = requests.get(f"{config.url}user/profile/v2?token={user_2['token']}&u_id={user_2_id}")
    user_2_profile_info = user_2_profile_json.json()
    user_2_profile = user_2_profile_info['user']
    assert channel_details['all_members'][1]['u_id'] == user_2_profile['u_id']
    assert channel_details['all_members'][1]['email'] == user_2_profile['email']
    assert channel_details['all_members'][1]['name_first'] == user_2_profile['name_first']
    assert channel_details['all_members'][1]['name_last'] == user_2_profile['name_last']
    
