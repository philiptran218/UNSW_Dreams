import pytest
import requests
import json
from src import config

INVALID_TOKEN = -1
INVALID_CHANNEL_ID = -1
INVALID_DM_ID = -1
INVALID_MESSAGE_ID = -1
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
def dm_1(user_1):
    dm = requests.post(config.url + 'dm/create/v1', json={
        'token': user_1['token'],
        'u_ids': []
    })
    dm_info = dm.json()
    return dm_info['dm_id']
    
@pytest.fixture
def dm_2(user_2):
    dm = requests.post(config.url + 'dm/create/v1', json={
        'token': user_2['token'],
        'u_ids': []
    })
    dm_info = dm.json()
    return dm_info['dm_id']
    
@pytest.fixture
def message_1(user_1, channel_1):
    msg = requests.post(config.url + 'message/send/v2', json={
        'token': user_1['token'],
        'channel_id': channel_1,
        'message': 'Hello World'
    })
    msg_info = msg.json()
    return msg_info['message_id']
    
@pytest.fixture
def message_2(user_1, dm_1):
    msg = requests.post(config.url + 'message/senddm/v1', json={
        'token': user_1['token'],
        'dm_id': dm_1,
        'message': 'Hello DM'
    })
    msg_info = msg.json()
    return msg_info['message_id']

@pytest.fixture 
def clear_database():
    requests.delete(config.url + 'clear/v1')

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
        'token': user_1['token'],
        'channel_id': INVALID_CHANNEL_ID,
        'message': 'Hello World'
    })
    assert msg.status_code == INPUTERROR
    
def test_message_send_user_not_in_channel(clear_database, user_1, user_2, channel_1):
    
    msg = requests.post(config.url + 'message/send/v2', json={
        'token': user_2['token'],
        'channel_id': channel_1,
        'message': 'Hiya World!'
    })
    assert msg.status_code == ACCESSERROR
    
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
    
    requests.post(config.url + 'message/send/v2', json={
        'token': user_1['token'],
        'channel_id': channel_1,
        'message': 'Hi Channel'
    })
    channel_msg = requests.get(f"{config.url}channel/messages/v2?token={user_1['token']}&channel_id={channel_1}&start=0")
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
    requests.post(config.url + 'message/send/v2', json={
        'token': user_2['token'],
        'channel_id': channel_1,
        'message': 'I just joined!!'
    })
    channel_msg = requests.get(f"{config.url}channel/messages/v2?token={user_2['token']}&channel_id={channel_1}&start=0")
    msg_info = channel_msg.json()['messages']
    assert len(msg_info) == 1
    assert msg_info[0]['message_id'] == 1
    assert msg_info[0]['u_id'] == user_2['auth_user_id']
    assert msg_info[0]['message'] == 'I just joined!!'

################################################################################
# message_edit http tests                                                      #
################################################################################

def test_message_edit_invalid_token(clear_database, user_1, channel_1, message_1):

    msg = requests.put(config.url + 'message/edit/v2', json={
        'token': INVALID_TOKEN,
        'message_id': message_1,
        'message': 'New message here'
    })
    assert msg.status_code == ACCESSERROR
    
def test_message_edit_invalid_messageid(clear_database, user_1, channel_1, message_1):

    msg = requests.put(config.url + 'message/edit/v2', json={
        'token': user_1['token'],
        'message_id': INVALID_MESSAGE_ID,
        'message': 'New message here'
    })
    assert msg.status_code == INPUTERROR
    
def test_message_edit_removed_message(clear_database, user_1, channel_1, message_1):

    requests.delete(config.url + 'message/remove/v1', json={
        'token': user_1['token'],
        'message_id': message_1
    })
    msg = requests.put(config.url + 'message/edit/v2', json={
        'token': user_1['token'],
        'message_id': message_1,
        'message': 'This is now changed'
    })
    assert msg.status_code == INPUTERROR
    
def test_message_edit_invalid_length(clear_database, user_1, channel_1, message_1):

    i = 0
    message = ''
    while i < 500:
        message += str(i)
        i += 1
        
    msg = requests.put(config.url + 'message/edit/v2', json={
        'token': user_1['token'],
        'message_id': message_1,
        'message': message
    })
    assert msg.status_code == INPUTERROR
    
def test_message_edit_accesserror_channel(clear_database, user_1, user_2, channel_1, message_1):

    msg = requests.put(config.url + 'message/edit/v2', json={
        'token': user_2['token'],
        'message_id': message_1,
        'message': 'I am not in this channel'
    })
    assert msg.status_code == ACCESSERROR
    
def test_message_edit_accesserror_dm(clear_database, user_1, user_2, dm_1, message_2):

    msg = requests.put(config.url + 'message/edit/v2', json={
        'token': user_2['token'],
        'message_id': message_2,
        'message': 'I am not in this DM'
    })
    assert msg.status_code == ACCESSERROR
    
def test_message_edit_empty(clear_database, user_1, dm_1, message_2):

    requests.put(config.url + 'message/edit/v2', json={
        'token': user_1['token'],
        'message_id': message_2,
        'message': '      '
    })
    dm_msg = requests.get(f"{config.url}dm/messages/v1?token={user_1['token']}&dm_id={dm_1}&start=0")
    msg_list = dm_msg.json()
    assert msg_list == {'messages': [], 'start': 0, 'end': -1}

def test_message_edit_valid_global(clear_database, user_1, channel_1, message_1):

    requests.put(config.url + 'message/edit/v2', json={
        'token': user_1['token'],
        'message_id': message_1,
        'message': 'This has been edited'
    })
    chan_msg = requests.get(f"{config.url}channel/messages/v2?token={user_1['token']}&channel_id={channel_1}&start=0")
    msg_info = chan_msg.json()['messages']
    assert len(msg_info) == 1
    assert msg_info[0]['message'] == 'This has been edited'
    assert msg_info[0]['u_id'] == user_1['auth_user_id']
    
def test_message_edit_valid_owner(clear_database, user_1, user_2, channel_2):
    
    requests.post(config.url + 'channel/join/v2', json={
        'token': user_1['token'],
        'channel_id': channel_2
    })
    msg = requests.post(config.url + 'message/send/v2', json={
        'token': user_1['token'],
        'channel_id': channel_2,
        'message': 'Sent by global'
    })
    msg_info = msg.json()
    requests.put(config.url + 'message/edit/v2', json={
        'token': user_2['token'],
        'message_id': msg_info['message_id'],
        'message': 'Edited by owner'
    })
    chan_msg = requests.get(f"{config.url}channel/messages/v2?token={user_1['token']}&channel_id={channel_2}&start=0") 
    chan_msg_info = chan_msg.json()['messages']
    assert len(chan_msg_info) == 1
    assert chan_msg_info[0]['message'] == 'Edited by owner'
    assert chan_msg_info[0]['u_id'] == user_1['auth_user_id']
    
def test_message_edit_valid_author(clear_database, user_1, user_2, dm_1):

    requests.post(config.url + 'dm/invite/v1', json={
        'token': user_1['token'],
        'dm_id': dm_1,
        'u_id': user_2['auth_user_id']
    })
    msg = requests.post(config.url + 'message/senddm/v1', json={
        'token': user_2['token'],
        'dm_id': dm_1,
        'message': 'Sent by new member'
    })
    msg_info = msg.json()
    requests.put(config.url + 'message/edit/v2', json={
        'token': user_2['token'],
        'message_id': msg_info['message_id'],
        'message': 'Edited by author'
    })
    dm_msg = requests.get(f"{config.url}dm/messages/v1?token={user_2['token']}&dm_id={dm_1}&start=0")
    dm_msg_info = dm_msg.json()['messages']
    assert len(dm_msg_info) == 1
    assert dm_msg_info[0]['message'] == 'Edited by author'
    assert dm_msg_info[0]['u_id'] == user_2['auth_user_id']
    
################################################################################
# message_remove http tests                                                    #
################################################################################    

def test_message_remove_invalid_token(clear_database, user_1, channel_1, message_1):

    msg = requests.delete(config.url + 'message/remove/v1', json={
        'token': INVALID_TOKEN,
        'message_id': message_1,
    })
    assert msg.status_code == ACCESSERROR
    
def test_message_remove_invalid_messageid(clear_database, user_1, channel_1, message_1):

    msg = requests.delete(config.url + 'message/remove/v1', json={
        'token': user_1['token'],
        'message_id': INVALID_MESSAGE_ID,
    })
    assert msg.status_code == INPUTERROR
    
def test_message_remove_removed_message(clear_database, user_1, channel_1, message_1):

    requests.delete(config.url + 'message/remove/v1', json={
        'token': user_1['token'],
        'message_id': message_1
    })
    msg = requests.delete(config.url + 'message/remove/v1', json={
        'token': user_1['token'],
        'message_id': message_1,
    })
    assert msg.status_code == INPUTERROR
    
def test_message_remove_accesserror_channel(clear_database, user_1, user_2, channel_1, message_1):

    msg = requests.delete(config.url + 'message/remove/v1', json={
        'token': user_2['token'],
        'message_id': message_1,
    })
    assert msg.status_code == ACCESSERROR
    
def test_message_remove_accesserror_dm(clear_database, user_1, user_2, dm_1, message_2):

    msg = requests.delete(config.url + 'message/remove/v1', json={
        'token': user_2['token'],
        'message_id': message_2,
    })
    assert msg.status_code == ACCESSERROR
    
def test_message_remove_valid_global(clear_database, user_2, user_1, channel_1, message_1):

    requests.delete(config.url + 'message/remove/v1', json={
        'token': user_2['token'],
        'message_id': message_1,
    })
    chan_msg = requests.get(f"{config.url}channel/messages/v2?token={user_1['token']}&channel_id={channel_1}&start=0") 
    msg_info = chan_msg.json()
    assert msg_info == {'messages': [], 'start': 0, 'end': -1}
    
def test_message_remove_valid_owner(clear_database, user_1, user_2, channel_2):
    
    requests.post(config.url + 'channel/join/v2', json={
        'token': user_1['token'],
        'channel_id': channel_2
    })
    msg = requests.post(config.url + 'message/send/v2', json={
        'token': user_1['token'],
        'channel_id': channel_2,
        'message': 'Sent by global'
    })
    msg_info = msg.json()
    requests.delete(config.url + 'message/remove/v1', json={
        'token': user_2['token'],
        'message_id': msg_info['message_id'],
    })
    chan_msg = requests.get(f"{config.url}channel/messages/v2?token={user_1['token']}&channel_id={channel_2}&start=0")
    chan_msg_info = chan_msg.json()
    assert chan_msg_info == {'messages': [], 'start': 0, 'end': -1}
    
def test_message_remove_valid_author(clear_database, user_1, user_2, dm_1):

    requests.post(config.url + 'dm/invite/v1', json={
        'token': user_1['token'],
        'dm_id': dm_1,
        'u_id': user_2['auth_user_id']
    })
    msg = requests.post(config.url + 'message/senddm/v1', json={
        'token': user_2['token'],
        'dm_id': dm_1,
        'message': 'Sent by new member'
    })
    msg_info = msg.json()
    requests.delete(config.url + 'message/remove/v1', json={
        'token': user_2['token'],
        'message_id': msg_info['message_id'],
    })
    dm_msg = requests.get(f"{config.url}dm/messages/v1?token={user_2['token']}&dm_id={dm_1}&start=0")
    dm_msg_info = dm_msg.json()
    assert dm_msg_info == {'messages': [], 'start': 0, 'end': -1}

################################################################################
# message_share http tests                                                     #
################################################################################

def test_message_share_invalid_token(clear_database, user_1, channel_1, message_1):

    msg = requests.post(config.url + 'message/share/v1', json={
        'token': INVALID_TOKEN,
        'og_message_id': message_1,
        'message': '',
        'channel_id': channel_1,
        'dm_id': -1
    })
    assert msg.status_code == ACCESSERROR
    
def test_message_share_invalid_messageid(clear_database, user_1, channel_1, message_1):

    msg = requests.post(config.url + 'message/share/v1', json={
        'token': user_1['token'],
        'og_message_id': INVALID_MESSAGE_ID,
        'message': '',
        'channel_id': channel_1,
        'dm_id': -1
    })
    assert msg.status_code == INPUTERROR
    
def test_message_share_removed_message(clear_database, user_1, channel_1, message_1):

    requests.delete(config.url + 'message/remove/v1', json={
        'token': user_1['token'],
        'message_id': message_1
    })
    msg = requests.post(config.url + 'message/share/v1', json={
        'token': user_1['token'],
        'og_message_id': message_1,
        'message': '',
        'channel_id': channel_1,
        'dm_id': -1
    })
    assert msg.status_code == INPUTERROR
    
def test_message_share_invalid_channel(clear_database, user_1, channel_1, message_1):

    msg = requests.post(config.url + 'message/share/v1', json={
        'token': user_1['token'],
        'og_message_id': message_1,
        'message': '',
        'channel_id': INVALID_CHANNEL_ID,
        'dm_id': -1
    })
    assert msg.status_code == INPUTERROR
    
def test_message_share_invalid_dm(clear_database, user_1, dm_1, message_2):

    msg = requests.post(config.url + 'message/share/v1', json={
        'token': user_1['token'],
        'og_message_id': message_2,
        'message': '',
        'channel_id': -1,
        'dm_id': INVALID_DM_ID
    })
    assert msg.status_code == INPUTERROR

def test_message_share_accesserror_channel(clear_database, user_1, user_2, channel_1, message_1):

    msg = requests.post(config.url + 'message/share/v1', json={
        'token': user_2['token'],
        'og_message_id': message_1,
        'message': '',
        'channel_id': channel_1,
        'dm_id': -1
    })
    assert msg.status_code == ACCESSERROR

def test_message_share_accesserror_dm(clear_database, user_1, user_2, dm_1, message_2):

    msg = requests.post(config.url + 'message/share/v1', json={
        'token': user_2['token'],
        'og_message_id': message_2,
        'message': '',
        'channel_id': -1,
        'dm_id': dm_1
    })
    assert msg.status_code == ACCESSERROR
    
def test_message_share_invalid_length(clear_database, user_1, channel_1, message_1):

    i = 0
    message = ''
    while i < 500:
        message += str(i)
        i += 1
        
    msg = requests.post(config.url + 'message/share/v1', json={
        'token': user_1['token'],
        'og_message_id': message_1,
        'message': message,
        'channel_id': channel_1,
        'dm_id': -1
    })
    assert msg.status_code == INPUTERROR 

def test_message_share_simple_optional(clear_database, user_1, channel_1, dm_1, message_1):
        
    requests.post(config.url + 'message/share/v1', json={
        'token': user_1['token'],
        'og_message_id': message_1,
        'message': 'Hi everyone!!!',
        'channel_id': -1,
        'dm_id': dm_1
    })
    dm_msg = requests.get(f"{config.url}dm/messages/v1?token={user_1['token']}&dm_id={dm_1}&start=0")
    dm_msg_info = dm_msg.json()['messages']
    assert len(dm_msg_info) == 1
    assert dm_msg_info[0]['message'] == 'Hello World Hi everyone!!!'
    assert dm_msg_info[0]['u_id'] == user_1['auth_user_id']

################################################################################
# message_senddm http tests                                                    #
################################################################################

def test_message_senddm_invalid_token(clear_database, user_1, dm_1):
    
    msg = requests.post(config.url + 'message/senddm/v1', json={
        'token': INVALID_TOKEN,
        'dm_id': dm_1,
        'message': 'Hello World'
    })
    assert msg.status_code == ACCESSERROR
    
def test_message_senddm_invalid_dm(clear_database, user_1, dm_1):

    msg = requests.post(config.url + 'message/senddm/v1', json={
        'token': user_1['token'],
        'dm_id': INVALID_DM_ID,
        'message': 'Hello World'
    })
    assert msg.status_code == INPUTERROR
    
def test_message_senddm_user_not_in_dm(clear_database, user_1, user_2, dm_1):
    
    msg = requests.post(config.url + 'message/senddm/v1', json={
        'token': user_2['token'],
        'dm_id': dm_1,
        'message': 'Greetings dm_1'
    })
    assert msg.status_code == ACCESSERROR
    
def test_message_senddm_invalid_length(clear_database, user_1, dm_1):
    i = 0
    message = ''
    while i < 500:
        message += str(i)
        i += 1

    msg = requests.post(config.url + 'message/senddm/v1', json={
        'token': user_1['token'],
        'dm_id': dm_1,
        'message': message
    })
    assert msg.status_code == INPUTERROR

def test_message_senddm_empty_message(clear_database, user_1, dm_1):

    msg = requests.post(config.url + 'message/senddm/v1', json={
        'token': user_1['token'],
        'dm_id': dm_1,
        'message': '  \n \t  '
    })
    assert msg.status_code == INPUTERROR
    
def test_message_senddm_single(clear_database, user_1, dm_1):

    requests.post(config.url + 'message/senddm/v1', json={
        'token': user_1['token'],
        'dm_id': dm_1,
        'message': 'Hi dm!!!'
    })
    dm_msg = requests.get(f"{config.url}dm/messages/v1?token={user_1['token']}&dm_id={dm_1}&start=0")
    msg_info = dm_msg.json()['messages']
    assert len(msg_info) == 1
    assert msg_info[0]['message_id'] == 1
    assert msg_info[0]['u_id'] == user_1['auth_user_id']
    assert msg_info[0]['message'] == 'Hi dm!!!'

def test_message_senddm_invited_user(clear_database, user_1, user_2, dm_1, dm_2):

    requests.post(config.url + 'dm/invite/v1', json={
        'token': user_2['token'],
        'dm_id': dm_2,
        'u_id': user_1['auth_user_id']
    })
    requests.post(config.url + 'message/senddm/v1', json={
        'token': user_1['token'],
        'dm_id': dm_2,
        'message': 'Thanks for the invite!'
    })
    requests.post(config.url + 'message/senddm/v1', json={
        'token': user_2['token'],
        'dm_id': dm_2,
        'message': 'No worries mate!'
    })   
    dm_msg = requests.get(f"{config.url}dm/messages/v1?token={user_1['token']}&dm_id={dm_2}&start=0")
    msg_info = dm_msg.json()['messages']
    assert len(msg_info) == 2
    assert msg_info[0]['message_id'] == 2
    assert msg_info[0]['u_id'] == user_2['auth_user_id']
    assert msg_info[0]['message'] == 'No worries mate!'
    assert msg_info[1]['message_id'] == 1
    assert msg_info[1]['u_id'] == user_1['auth_user_id']
    assert msg_info[1]['message'] == 'Thanks for the invite!'

