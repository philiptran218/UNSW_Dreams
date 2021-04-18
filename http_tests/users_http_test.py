import pytest
import requests
import json
from src import config
from datetime import timezone, datetime

INVALID_TOKEN = -1
INVALID_UID = -1
INPUTERROR = 400
ACCESSERROR = 403

DEFAULT_IMG_URL = "https://www.usbji.org/sites/default/files/person.jpg"

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
def get_time():
    time = datetime.today()
    time = time.replace(tzinfo=timezone.utc).timestamp()
    time_issued = round(time)
    return time_issued

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
                'profile_img_url': config.url + "static/1.jpg",
            },
            {
                'u_id': 2,
                'email': 'philtran@gmail.com',
                'name_first': 'Philip',
                'name_last': 'Tran',
                'handle_str': 'philiptran',
                'profile_img_url': config.url + "static/2.jpg",
            },
            {
                'u_id': 3,
                'email': 'terrynguyen@gmail.com',
                'name_first': 'Terrance',
                'name_last': 'Nguyen',
                'handle_str': 'terrancenguyen', 
                'profile_img_url': config.url + "static/3.jpg",
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

################################################################################
# users_stats http tests                                                       #
################################################################################

def empty_stats_list(get_time):
    return {
        'dreams_stats': {
        'channels_exist': [{'num_channels_exist': 0, 'time_stamp': get_time}],
        'dms_exist': [{'num_dms_exist': 0, 'time_stamp': get_time}],
        'messages_exist': [{'num_messages_exist': 0, 'time_stamp': get_time}],
        'utilization_rate': 0.0,
        }
    }


def stats_list(get_time):
    return {
        'dreams_stats': {
        'channels_exist': [{'num_channels_exist': 1, 'time_stamp': get_time}],
        'dms_exist': [{'num_dms_exist': 1, 'time_stamp': get_time}],
        'messages_exist': [{'num_messages_exist': 1, 'time_stamp': get_time}],
        'utilization_rate': 1.0,
        }
    }

def test_users_stats_invalid_token(clear_database, user_1):
    stats = requests.get(f"{config.url}users/stats/v1?token={INVALID_TOKEN}")
    assert stats.status_code == ACCESSERROR

def test_users_stats_valid_empty(clear_database, user_1, get_time):
    stats = requests.get(f"{config.url}users/stats/v1?token={user_1['token']}")
    stats_info = stats.json()
    assert stats_info == empty_stats_list(get_time)

def test_users_stats_valid(clear_database, user_1, user_2, test_create_dm, channel_1, message_1, get_time):
    stats = requests.get(f"{config.url}users/stats/v1?token={user_1['token']}")
    stats_info = stats.json()
    assert stats_info == stats_list(get_time)
