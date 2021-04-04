import pytest
import requests
import json
from src import config

INVALID_TOKEN = -1
INVALID_CHANNEL_ID = -1
INVALID_DM_ID = -1
INVALID_U_ID = -1

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
def channel_2(user_2):
    channel = requests.post(config.url + 'channels/create/v2', json={
        'token': user_2['token'],
        'name': 'Channel2',
        'is_public': True
    })
    channel_info = channel.json()
    return channel_info['channel_id']

@pytest.fixture 
def clear_database():
    requests.delete(config.url + 'clear/v1')

def expected_empty_output():
    return {'channels': []}

################################################################################
# channels_listall http tests                                                  #
################################################################################

def expected_output_listall_v2():
    return {
        'channels': [
            {
                "channel_id": 1,
                "name":"Channel1"
            },
            {
                "channel_id": 2,
                "name":"Channel2"
            }
        ]
    }

def test_channels_listall_invalid_token(clear_database, user_1, channel_1):
    chan = requests.get(config.url + 'channels/listall/v2', json={
        'token': INVALID_TOKEN,
    })
    assert chan.status_code == ACCESSERROR

def test_channel_listall_valid_empty(clear_database, user_1):
    chan = requests.get(config.url + 'channels/listall/v2', json={
        'token': user_1['token'],
    })
    chan_list = chan.json()
    assert chan_list == expected_empty_output()

def test_channel_listall_valid(clear_database, user_1, user_2, channel_1, channel_2):
    chan = requests.get(config.url + 'channels/listall/v2', json={
        'token': user_1['token'],
    })
    chan_list = chan.json()
    assert chan_list == expected_output_listall_v2()

################################################################################
# channels_list http tests                                                     #
################################################################################
 
def expected_output_list_v2():
    return {
        'channels':
        [
            {
                "channel_id": 1,
                "name": "Channel1"
            }
        ]
    }

def test_channels_list_invalid_token(clear_database, user_1, channel_1):
    chan = requests.get(config.url + 'channels/list/v2', json={
        'token': INVALID_TOKEN,
    })
    assert chan.status_code == ACCESSERROR

def test_channel_list_valid_empty(clear_database, user_1):
    chan = requests.get(config.url + 'channels/list/v2', json={
        'token': user_1['token'],
    })
    chan_list = chan.json()
    assert chan_list == expected_empty_output()

def test_channel_list_valid(clear_database, user_1, user_2, channel_1, channel_2):
    chan = requests.get(config.url + 'channels/list/v2', json={
        'token': user_1['token'],
    })
    chan_list = chan.json()
    assert chan_list == expected_output_list_v2()

################################################################################
# channel_create_v1 http tests                                                 #
################################################################################

def test_valid_channels_create_v1_u_id(clear_database,user_1):
    chan = requests.post(config.url + 'channels/create/v2', json={
       'token': user_1['token'],
       'name': "ValidChannelName",
       'is_public': True
    })
    
    chan_id = chan.json()
    assert(chan_id == {'channel_id': 1})

def test_valid_channels_create_v1(clear_database,user_1):
    requests.post(config.url + 'channels/create/v2', json={
       'token': user_1['token'],
       'name': "ValidChannelName",
       'is_public': True
    })

    chans = requests.get(config.url + 'channels/listall/v2', json={
        'token': user_1['token']
    })
    chans = chans.json()
    assert(bool(chans['channels']))

def test_valid_channels_create_v1_multiple(clear_database,user_1,user_2):
    requests.post(config.url + 'channels/create/v2', json={
       'token': user_1['token'],
       'name': "ValidChannelName",
       'is_public': True
    })
    requests.post(config.url + 'channels/create/v2', json={
       'token': user_2['token'],
       'name': "ValidChannelName1",
       'is_public': True
    })
    
    chans = requests.get(config.url + 'channels/listall/v2', json={
        'token': user_1['token']
    })
    chans = chans.json()
    assert(len(chans['channels']) > 1)

def test_invalidName_channels_create_v1(clear_database,user_1):
    invalid_name = 'nameismorethantwentycharacters'

    chan = requests.post(config.url + 'channels/create/v2', json={
       'token': user_1['token'],
       'name': invalid_name,
       'is_public': True
    })
    assert chan.status_code == INPUTERROR

def test_invalid_user(clear_database):
    chan = requests.post(config.url + 'channels/create/v2', json={
       'token': INVALID_TOKEN,
       'name': 'channelname',
       'is_public': True
    })
    assert chan.status_code == ACCESSERROR
