from src.auth import auth_login_v1, auth_register_v1
from src.users import users_all_v1, users_stats_v1
from src.dm import dm_create_v1
from src.channels import channels_create_v1
from src.message import message_senddm_v1
from src.error import InputError, AccessError
import pytest
from src.other import clear_v1

INVALID_VALUE = -1

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
                },
                {
                'u_id': 2,
                'name_first': 'Terry',
                'name_last': 'Nguyen',
                'email': 'terrynguyen@gmail.com',
                'handle_str': 'terrynguyen',
                },
                {
                'u_id': 3,
                'name_first': 'Phil',
                'name_last': 'Tran',
                'email': 'philt@gmail.com',
                'handle_str': 'philtran',
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

def test_users_stats_invalid_token(clear_data):
    with pytest.raises(AccessError):
        users_stats_v1(INVALID_VALUE) 

def test_users_stats_valid_empty(clear_data, user_1):
    assert users_stats_v1(user_1['token']) == empty_stats_list()

def test_users_stats_valid(clear_data, user_1, user_2, channel1, dm1, message1):
    assert users_stats_v1(user_1['token']) == stats_list()
