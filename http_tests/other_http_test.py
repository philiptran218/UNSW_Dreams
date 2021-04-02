import pytest
import requests
import json
from src import config

INVALID_TOKEN = -1
INVALID_CHANNEL_ID = -1
INVALID_STRING_LENGTH = 1001
INPUTERROR = 400
ACCESSERROR = 403

UPPER_CASE_STR = "HOWS IT GOING"
MIXED_QUERY_STR = "1. How's it going?"
SUB_STR = "it"
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
def channel_1(user_1):
    channel = requests.post(config.url + 'channels/create/v2', json={
        'token': user_1['token'],
        'name': "John's Channel",
        'is_public': True
    })
    channel_info = channel.json()
    return channel_info['channel_id']

@pytest.fixture
def channel_2(user_2):
    channel = requests.post(config.url + 'channels/create/v2', json={
        'token': user_2['token'],
        'name': "Phil's Channel",
        'is_public': True
    })
    channel_info = channel.json()
    return channel_info['channel_id']

@pytest.fixture
def dm_1(user_1, user_2):
    dm = requests.post(config.url + 'dm/create/v1', json={
        'token': user_1['token'],
        'u_ids': [user_2['auth_user_id']],
    })
    dm_info = dm.json()
    return dm_info['dm_id']

@pytest.fixture
def dm_2(user_2, user_3):
    dm = requests.post(config.url + 'dm/create/v1', json={
        'token': user_2['token'],
        'u_ids': [user_3['auth_user_id']],
    })
    dm_info = dm.json()
    return dm_info['dm_id']

@pytest.fixture 
def clear_database():
    requests.delete(config.url + 'clear')


################################################################################
# clear_v1 http tests                                                          # 
################################################################################

def test_clear_users(clear_database,user_1):
    email = 'johnsmith@gmail.com'
    password = 'goodpass'
    requests.delete(config.url + 'clear')

    login = requests.post(config.url + 'auth/login/v2', json={
        'email': email,
        'password': password
    })
    assert login.status_code == INPUTERROR

def test_clear_channels(clear_data, user_1, public_channel_1):
    requests.delete(config.url + 'clear')

    user_info = requests.post(config.url + 'auth/register/v2', json={
        'email': "terrynguyen@gmail.com",
        'password': "password",
        'name_first': "Terry",
        'name_last': "Nguyen"
    })
    user_token= user_info.json()['token']

    chan = requests.get(config.url + 'channel/listall/v2', json={
        'token': user_token
    })
    chan_list = chan.json()['channels']
    assert(not bool(chan_list))

