import pytest
import requests
import json
from src import config

INVALID_TOKEN = -1
INVALID_CHANNEL_ID = -1
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
        'name': "Phil's Channel",
        'is_public': True
    })
    channel_info = channel.json()
    return channel_info['channel_id']

@pytest.fixture 
def clear_database():
    requests.delete(config.url + 'clear')

################################################################################
# message_send http tests                                                      #
################################################################################

def test_message_send_invalid_token(clear_database, user_1, channel_1):
    
    msg = requests.post(config.url + 'message/send/v2', json={
        'token': INVALID_TOKEN,
        'channel_id': channel_1,
        'message': 'Hello World'
    })
    assert msg.status_code == ACCESSERROR
    
def test_message_send_invalid_channel(clear_database, user_1, channel_1):

    msg = requests.post(config.url + 'message/send/v2', json={
        'token': user_1['token']
        'channel_id': INVALID_CHANNEL_ID,
        'message': 'Hello World'
    })
    assert msg.status_code == INPUTERROR
    
def test_message_send_user_not_in_channel(clear_database, user_1, user_2, channel_1):
    
    msg = requests.post(config.url + 'message/send/v2', json={
        'token': user_2['token']
        'channel_id': channel_1,
        'message': 'Hiya World!'
    })
    assert msg.status_code == INPUTERROR
    
def test_message_send_invalid_length(clear_database, user_1, channel_1):
    i = 0
    message = ''
    while i < 500:
        message += str(i)
        i += 1

    msg = requests.post(config.url + 'message/send/v2', json={
        'token': user_1['token'],
        'channel_id': channel_1,
        'message': message
    })
    assert msg.status_code == INPUTERROR

def test_message_send_empty_message(clear_database, user_1, channel_1):

    msg = requests.post(config.url + 'message/send/v2', json={
        'token': user_1['token'],
        'channel_id': channel_1,
        'message': '        '
    })
    assert msg.status_code == INPUTERROR
    
def test_message_send_single(clear_database, user_1, channel_1):
    
    msg = requests.post(config.url + 'message/send/v2', json={
        'token': user_1['token'],
        'channel_id': channel_1,
        'message': 'Hi Channel'
    })
    channel_msg = requests.get(config.url + 'channel/messages/v2', json={
        'token': user_1['token'],
        'channel_id': channel_1,
        'start': 0
    })
    msg_info = channel_msg.json()['messages']
    assert len(msg_info) == 1
    assert msg_info[0]['message_id'] == 1
    assert msg_info[0]['u_id'] == user_1['auth_user_id']
    assert msg_info[0]['message'] == 'Hi Channel'
    
def test_message_send_joined_user(clear_database, user_1, user_2, channel_1):
    
    requests.post(config.url + 'channel/join/v2', json={
        'token': user_2['token'],
        'channel_id': channel_1
    })
    msg = requests.post(config.url + 'message/send/v2', json={
        'token': user_2['token'],
        'channel_id': channel_1,
        'message': 'I just joined!!'
    })
    channel_msg = requests.get(config.url + 'channel/messages/v2', json={
        'token': user_2['token'],
        'channel_id': channel_1,
        'start': 0
    }) 
    msg_info = channel_msg.json()['messages']
    assert len(msg_info) == 1
    assert msg_info[0]['message_id'] == 1
    assert msg_info[0]['u_id'] == user_2['auth_user_id']
    assert msg_info[0]['message'] == 'I just joined!!'

