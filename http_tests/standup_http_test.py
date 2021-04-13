import pytest
import requests
import json
from src import config

INVALID_CHANNEL_ID = -1
INVALID_TOKEN = -1

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
def public_channel_1(user_1):
    channel = requests.post(config.url + 'channels/create/v2', json={
        'token': user_1['token'],
        'name': 'Channel1',
        'is_public': True
    })
    channel_info = channel.json()
    return channel_info['channel_id']

@pytest.fixture
def create_long_msg():
    msg = ''
    for i in range(0,400):
        msg += str(i)
    return msg

@pytest.fixture 
def clear_data():
    requests.delete(config.url + '/clear/v1')

################################################################################
# standup_start_v1 http tests                                                  #
################################################################################

def test_standup_start_invalid_channel_id(clear_data,user_1,public_channel_1):
    standup = requests.post(config.url + 'standup/start/v1', json={
        'token' : user_1['token']
        'channel_id' : INVALID_CHANNEL_ID
        'length' : 10
    })
    assert standup.status_code == InputError

def test_currently_running_standup(clear_data,user_1,public_channel_1):
    standup = requests.post(config.url + 'standup/start/v1', json={
        'token' :user_1['token']
        'channel_id' : public_channel_1
        'length' :10
    })  
         standup = requests.post(config.url + 'standup/start/v1', json={
        'token' :user_1['token']
        'channel_id' : public_channel_1
        'length' : 19
    })  
    assert standup.status_code == InputError

def test_user_not_in_channel(clear_data,user_1,user_2,public_channel_1):
    standup = requests.post(config.url + 'standup/start/v1', json={
        'token' : user_2['token']
        'channel_id' : public_channel_1
        'length' : 19
    })  
    assert standup.status_code == AccessError

def test_standup_start_invalid_token(clear_data,user_1,public_channel_1):
    standup = requests.post(config.url + 'standup/start/v1', json={  
        'token' : INVALID_TOKEN
        'channel_id' : public_channel_1
        'length': 19
    })  
    assert standup.status_code == AccessError

def test_standup_start(clear_data,user_1,public_channel_1):
    time_end = datetime.now() + timedelta(0, 10)
    time_end = round(time_end.replace(tzinfo=timezone.utc).timestamp())

    standup = requests.post(config.url + 'standup/start/v1', json={  
        'token' : INVALID_TOKEN
        'channel_id' : public_channel_1
        'length' : 19
    })
    time = standup.json()['time_finish']

    is_active = requests.get(f"{config.url}standup/active/v1={user_1['token']}&channel_id={public_channel_1}")  
    is_active = is_active.json()['is_active']
    
    assert time == time_end
    assert is_active == True
