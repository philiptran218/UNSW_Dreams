import pytest
import requests
import json
from src import config
import time
from datetime import datetime, timezone, timedelta

INPUTERROR = 400
ACCESSERROR = 403
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
def clear_data():
    requests.delete(config.url + '/clear/v1')

################################################################################
# standup_start_v1 http tests                                                  #
################################################################################

def test_standup_start_invalid_channel_id(clear_data,user_1,public_channel_1):
    standup = requests.post(config.url + 'standup/start/v1', json={
        'token' : user_1['token'],
        'channel_id' : INVALID_CHANNEL_ID,
        'length' : 10
    })
    assert standup.status_code == INPUTERROR

def test_currently_running_standup(clear_data,user_1,public_channel_1):
    standup = requests.post(config.url + 'standup/start/v1', json={
        'token' :user_1['token'],
        'channel_id' : public_channel_1,
        'length' :10
    })  
    standup = requests.post(config.url + 'standup/start/v1', json={
        'token' :user_1['token'],
        'channel_id' : public_channel_1,
        'length' : 19
    })  
    assert standup.status_code == INPUTERROR

def test_user_not_in_channel(clear_data,user_1,user_2,public_channel_1):
    standup = requests.post(config.url + 'standup/start/v1', json={
        'token' : user_2['token'],
        'channel_id' : public_channel_1,
        'length' : 19
    })  
    assert standup.status_code == ACCESSERROR

def test_standup_start_invalid_token(clear_data,user_1,public_channel_1):
    standup = requests.post(config.url + 'standup/start/v1', json={  
        'token' : INVALID_TOKEN,
        'channel_id' : public_channel_1,
        'length': 19
    })  
    assert standup.status_code == ACCESSERROR

def test_standup_start(clear_data,user_1,public_channel_1):
    time_end = datetime.now() + timedelta(0, 10)
    time_end = round(time_end.replace(tzinfo=timezone.utc).timestamp())

    standup = requests.post(config.url + 'standup/start/v1', json={  
        'token' : INVALID_TOKEN,
        'channel_id' : public_channel_1,
        'length' : 19
    })
    time = standup.json()['time_finish']

    is_active = requests.get(f"{config.url}standup/active/v1={user_1['token']}&channel_id={public_channel_1}")  
    is_active = is_active.json()['is_active']
    
    assert time == time_end
    assert is_active == True


################################################################################
# standup_active_v1 tests                                                      #
################################################################################

def test_standup_active_invalid_channel_id(clear_data,user_1,public_channel_1):
    is_active = requests.get(f"{config.url}standup/active/v1={user_1['token']}&channel_id={INVALID_CHANNEL_ID}")
    assert is_active.status_code == INPUTERROR

def test_standup_active_invalid_token(clear_data,user_1,public_channel_1):
    is_active = requests.get(f"{config.url}standup/active/v1={INVALID_TOKEN}&channel_id={public_channel_1}")   
    assert is_active.status_code == ACCESSERROR

def test_standup_active(clear_data,user_1,public_channel_1):
    time_end = datetime.now() + timedelta(0, 10)
    time_end = round(time_end.replace(tzinfo=timezone.utc).timestamp())
    requests.post(config.url + 'standup/start/v1', json={
        'token' :user_1['token'],
        'channel_id' : public_channel_1,
        'length' :10
    })  
    info = requests.get(f"{config.url}standup/active/v1={user_1['token']}&channel_id={public_channel_1}")  
    info = info.json()
    assert(info['is_active'])
    assert info['time_finish'] == time_end
    time.sleep(15)
    
    new_info = requests.get(f"{config.url}standup/active/v1={user_1['token']}&channel_id={public_channel_1}")  
    new_info = new_info.json()
    assert not info['is_active']
    assert info['time_finish'] == None

def test_standup_inactive(clear_data, user_1, public_channel_1):
    new_info = requests.get(f"{config.url}standup/active/v1={user_1['token']}&channel_id={public_channel_1}")  
    new_info = new_info.json()
    assert not info['is_active']
    assert info['time_finish'] == None

################################################################################
# standup_send_v1 http tests                                                   #
################################################################################

def test_standup_send_invalid_channel_id(clear_data,user_1,public_channel_1):
    standup = requests.post(config.url + 'standup/send/v1', json={  
        'token' : user_1['token'],
        'channel_id' : INVALID_CHANNEL_ID,
        'message': "hibye"
    })  
    assert standup.status_code == INPUTERROR

def test_standup_send_invalid_msg_length(clear_data,user_1,public_channel_1):
    requests.post(config.url + 'standup/start/v1', json={
        'token' :user_1['token'],
        'channel_id' : public_channel_1,
        'length' :20
    })  
    standup = requests.post(config.url + 'standup/send/v1', json={  
        'token' : user_1['token'],
        'channel_id' : public_channel_1,
        'message': "i"*1001
    })  
    assert standup.status_code == INPUTERROR


def test_standup_send_not_active(clear_data,user_1,public_channel_1):
    standup = requests.post(config.url + 'standup/send/v1', json={  
        'token' : user_1['token'],
        'channel_id' : public_channel_1,
        'message': 'bye'
    })  
    assert standup.status_code == INPUTERROR


def test_standup_send_user_not_member(clear_data,user_1,user_2,public_channel_1):
    requests.post(config.url + 'standup/start/v1', json={
        'token' :user_1['token'],
        'channel_id' : public_channel_1,
        'length' :20
    }) 
    standup = requests.post(config.url + 'standup/send/v1', json={  
        'token' : user_2['token'],
        'channel_id' : public_channel_1,
        'message': 'bye'
    })  
    assert standup.status_code == ACCESSERROR

def test_standup_send_invalid_token(clear_data, user_1, public_channel_1):
    standup = requests.post(config.url + 'standup/send/v1', json={  
        'token' : INVALID_TOKEN,
        'channel_id' : public_channel_1,
        'message': 'bye'
    })  
    assert standup.status_code == ACCESSERROR


def test_standup_send_successful_message(clear_data, user_1, user_2, public_channel_1):
    requests.post(config.url + 'channel/join/v2', json={
        'token': user_2['token'],
        'channel_id': public_channel_1
    })
    time_end = datetime.now() + timedelta(0, 5)
    time_end = round(time_end.replace(tzinfo=timezone.utc).timestamp())
    requests.post(config.url + 'standup/start/v1', json={
        'token' :user_1['token'],
        'channel_id' : public_channel_1,
        'length' : 5
    }) 
    standup = requests.post(config.url + 'standup/send/v1', json={  
        'token' : user_1['token'],
        'channel_id' : public_channel_1,
        'message': 'Welcome to the standup!'
    }) 
    standup = requests.post(config.url + 'standup/send/v1', json={  
        'token' : user_2['token'],
        'channel_id' : public_channel_1,
        'message': 'Hi there!'
    }) 
    time.sleep(6)
    chan = requests.get(f"{config.url}channel/messages/v2?token={user_1['token']}&channel_id={public_channel_1}&start={0}")
    chan_msg = chan.json()['messages']
    assert len(chan_msg) == 1
    assert chan_msg[0]['message'] == 'johnsmith: Welcome to the standup!\nterrynguyen: Hi there!'
    assert chan_msg[0]['u_id'] == user_1['auth_user_id']
    assert chan_msg[0]['message_id'] == 1
    assert chan_msg[0]['time_created'] == time_end





    
    

    
    
    
    
    
    
    
