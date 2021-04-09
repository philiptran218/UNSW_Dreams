import pytest
import requests
import json
from src import config

INVALID_TOKEN = -1
INVALID_UID = -1
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
def user_3():
    user = requests.post(config.url + 'auth/register/v2', json={
        'email': 'terrynguyen@gmail.com',
        'password': 'goodpass',
        'name_first': 'Terrance',
        'name_last': 'Nguyen'
    })
    return user.json()

@pytest.fixture
def test_create_dm(user_1,user_2):
    dm = requests.post(config.url + 'dm/create/v1', json={
        'token': user_1['token'],
        'u_ids': [user_2['auth_user_id']]
    })
    dm_info = dm.json()
    return dm_info

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
def message_1(user_1, test_create_dm):
    msg = requests.post(config.url + 'message/senddm/v1', json={
        'token': user_1['token'],
        'dm_id': test_create_dm['dm_id'],
        'message': 'Hello DM'
    })
    msg_info = msg.json()
    return msg_info['message_id']

@pytest.fixture 
def clear_database():
    requests.delete(config.url + 'clear/v1')

################################################################################
# users_all http tests                                                         #
################################################################################

def expected_output_all_users():
    return {
        'users': [
            {
                'u_id': 1,
                'email': 'johnsmith@gmail.com',
                'name_first': 'John',
                'name_last': 'Smith',
                'handle_str': 'johnsmith',
            },
            {
                'u_id': 2,
                'email': 'philtran@gmail.com',
                'name_first': 'Philip',
                'name_last': 'Tran',
                'handle_str': 'philiptran',
            },
            {
                'u_id': 3,
                'email': 'terrynguyen@gmail.com',
                'name_first': 'Terrance',
                'name_last': 'Nguyen',
                'handle_str': 'terrancenguyen', 
            }
        ]   
    }

def test_all_invalid_token(clear_database, user_1, user_2, user_3):

    all_profiles = requests.get(f"{config.url}users/all/v1?token={INVALID_TOKEN}")
    assert all_profiles.status_code == ACCESSERROR

def test_all_valid(clear_database, user_1, user_2, user_3):
    all_profiles_json = requests.get(f"{config.url}users/all/v1?token={user_1['token']}")
    all_profiles = all_profiles_json.json()
    assert all_profiles == expected_output_all_users()
    # This is the last http tests, so run clear here to reset database to its
    # original state.
    requests.delete(config.url + 'clear/v1')

################################################################################
# users_stats http tests                                                       #
################################################################################

def empty_stats_list():
    return {
        'channels_joined': 0,
        'dms_joined': 0,
        'messages_sent': 0,
        'utilisation_rate': 0,
    }

def stats_list():
    return {
        'channels_joined': 1,
        'dms_joined': 1,
        'messages_sent': 1,
        'involvement_rate': 1,
    }

def test_users_stats_invalid_token(clear_database, user_1):
    stats = requests.get(f"{config.url}users/stats/v1?{INVALID_TOKEN}")
    assert stats.status_code == ACCESSERROR

def test_users_stats_valid_empty(clear_database, user_1):
    stats = requests.get(f"{config.url}user/stats/v1?{user_1['token']}")
    stats_info = stats.json()
    assert stats_info == empty_stats_list()

def test_users_stats_valid(clear_database, user_1, user_2, test_create_dm, channel_1, message_1):
    stats = requests.get(f"{config.url}user/stats/v1?{user_1['token']}")
    stats_info = stats.json()
    assert stats_info == stats_list()
