from src.auth import auth_login_v1, auth_register_v1
from src.users import users_all_v1, users_stats_v1
from src.dm import dm_create_v1
from src.channels import channels_create_v1
from src.message import message_senddm_v1
from src.error import InputError, AccessError
from src.other import clear_v1
from datetime import timezone, datetime
from src import config

import pytest

INVALID_VALUE = -1
INVALID_TOKEN = -1

################################################################################
# Fixtures                                                                     #
################################################################################

@pytest.fixture
def user_1():
    user = auth_register_v1("johnsmith@gmail.com", "password", "John", "Smith")
    return user

@pytest.fixture
def user_2():
    user = auth_register_v1("terrynguyen@gmail.com", "password", "Terry", "Nguyen")
    return user

@pytest.fixture
def user_3():
    user = auth_register_v1('philt@gmail.com', 'badpass', 'Phil', 'Tran')
    return user

@pytest.fixture
def channel1(user_1):
    channel = channels_create_v1(user_1['token'], "channel1", True)
    return channel

@pytest.fixture
def dm1(user_1, user_2):
    dm = dm_create_v1(user_1['token'], [user_2['auth_user_id']])
    return dm

@pytest.fixture
def message1(user_1, user_2, dm1):
    message = message_senddm_v1(user_1['token'], dm1['dm_id'], 'Hello DM')
    return message

@pytest.fixture
def get_time():
    time = datetime.today()
    time = time.replace(tzinfo=timezone.utc).timestamp()
    time_issued = round(time)
    return time_issued

@pytest.fixture
def clear_data():
    clear_v1()

################################################################################
# users_all_v1 tests                                                           #
################################################################################

def expected_output_1():
    return  { 'users':
                [{
                'u_id': 1,
                'email': 'johnsmith@gmail.com',
                'name_first': 'John',
                'name_last': 'Smith',
                'handle_str': 'johnsmith',
                'profile_img_url': config.url + "static/1.jpg", 
                }]
            }

def expected_output_2():
    return  { 'users':
                [{
                'u_id': 1,
                'email': 'johnsmith@gmail.com',
                'name_first': 'John',
                'name_last': 'Smith',
                'handle_str': 'johnsmith',
                'profile_img_url': config.url + "static/1.jpg", 
                },
                {
                'u_id': 2,
                'name_first': 'Terry',
                'name_last': 'Nguyen',
                'email': 'terrynguyen@gmail.com',
                'handle_str': 'terrynguyen',
                'profile_img_url': config.url + "static/2.jpg", 
                },
                {
                'u_id': 3,
                'name_first': 'Phil',
                'name_last': 'Tran',
                'email': 'philt@gmail.com',
                'handle_str': 'philtran',
                'profile_img_url': config.url + "static/3.jpg", 
                }]
            }

def test_users_all_invalid_token(clear_data):
    with pytest.raises(AccessError):
        users_all_v1(INVALID_VALUE)

def test_users_all_valid_token(clear_data, user_1):
    assert users_all_v1(user_1['token']) == expected_output_1()

def test_users_all_multiple_users(clear_data, user_1, user_2, user_3):
    assert users_all_v1(user_1['token']) == expected_output_2()

################################################################################
# users_stats_v1 tests                                                         #
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

def test_users_stats_invalid_token(clear_data):
    with pytest.raises(AccessError):
        users_stats_v1(INVALID_TOKEN) 

def test_users_stats_valid_empty(clear_data, user_1, get_time):
    assert users_stats_v1(user_1['token']) == empty_stats_list(get_time)

def test_users_stats_valid(clear_data, user_1, user_2, channel1, dm1, message1, get_time):
    assert users_stats_v1(user_1['token']) == stats_list(get_time)
