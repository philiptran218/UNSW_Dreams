import pytest
import requests
import json
from src import config
from datetime import datetime, timezone, timedelta
import threading

INVALID_TOKEN = -1
INVALID_CHANNEL_ID = -1
INVALID_DM_ID = -1
INVALID_MESSAGE_ID = -1
INVALID_REACT_ID = -1
REACT_ID = 1
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
def message_time():
    time = datetime.now() + timedelta(0, 3)
    send_time = round(time.replace(tzinfo=timezone.utc).timestamp())
    return send_time

@pytest.fixture 
def clear_database():
    requests.delete(config.url + 'clear/v1')

def message_react(token, message_id, react_id):
    return requests.post(config.url + 'message/react/v1', json={
        'token': token,
        'message_id': message_id,
        'react_id': react_id
    })

def message_unreact(token, message_id, react_id):
    return requests.post(config.url + 'message/unreact/v1', json={
        'token': token,
        'message_id': message_id,
        'react_id': react_id
    })

def message_pin(token, message_id):
    return requests.post(config.url + 'message/pin/v1', json={
        'token': token,
        'message_id': message_id
    })

def message_unpin(token, message_id):
    return requests.post(config.url + 'message/unpin/v1', json={
        'token': token,
        'message_id': message_id
    })

def channel_messages(token, channel_id, start):
    return requests.get(f"{config.url}channel/messages/v2?token={token}&channel_id={channel_id}&start={start}")

def dm_messages(token, channel_id, start):
    return requests.get(f"{config.url}dm/messages/v1?token={token}&dm_id={channel_id}&start={start}")

def channel_invite(token, channel_id, u_id):
    return requests.post(config.url + 'channel/invite/v2', json={
        'token': token,
        'channel_id': channel_id,
        'u_id': u_id
    })

def channel_leave(token, channel_id):
    return requests.post(config.url + 'channel/leave/v1', json={
        'token': token,
        'channel_id': channel_id,
    })

def channel_addowner(token, channel_id, u_id):
    return requests.post(config.url + 'channel/addowner/v1', json={
        'token': token,
        'channel_id': channel_id,
        'u_id': u_id
    })

def dm_invite(token, dm_id, u_id):
    return requests.post(config.url + 'dm/invite/v1', json={
        'token': token,
        'dm_id': dm_id,
        'u_id': u_id
    })

def dm_leave(token, dm_id):
    return requests.post(config.url + 'dm/leave/v1', json={
        'token': token,
        'dm_id': dm_id,
    })


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

################################################################################
# message_react http tests                                                     #
################################################################################

def test_message_react_invalid_token(clear_database, user_1, channel_1, message_1):
    react = message_react(INVALID_TOKEN, message_1, REACT_ID)
    assert react.status_code == ACCESSERROR

def test_message_react_invalid_message_id(clear_database, user_1, channel_1, message_1):
    react = message_react(user_1['token'], INVALID_MESSAGE_ID, REACT_ID)
    assert react.status_code == INPUTERROR

def test_message_react_invalid_react_id(clear_database, user_1, channel_1, message_1):
    react = message_react(user_1['token'], message_1, INVALID_REACT_ID)
    assert react.status_code == INPUTERROR

def test_message_has_already_reacted(clear_database, user_1, channel_1, message_1):
    message_react(user_1['token'], channel_1, REACT_ID)
    react = message_react(user_1['token'], message_1, REACT_ID)
    assert react.status_code == INPUTERROR

def test_message_react_user_not_in_channel(clear_database, user_1, user_2, channel_1, message_1):
    react = message_react(user_2['token'], message_1, REACT_ID)
    assert react.status_code == ACCESSERROR   

def test_message_react_user_not_in_dm(clear_database, user_1, user_2, dm_1, message_2):
    react = message_react(user_2['token'], message_2, REACT_ID)
    assert react.status_code == ACCESSERROR  

def test_message_react_valid_inputs_in_channel(clear_database, user_1, channel_1, message_1):
    message_react(user_1['token'], channel_1, REACT_ID)
    messages_json = channel_messages(user_1['token'], channel_1, 0)
    messages = messages_json.json()
    message = messages['messages'][0]
    assert message['message_id'] == 1
    assert message['u_id'] == 1
    assert message['message'] == 'Hello World'
    assert message['reacts'][0]['react_id'] == 1
    assert message['reacts'][0]['u_ids'] == [1]
    assert message['reacts'][0]['is_this_user_reacted'] == True

def test_message_react_valid_inputs_in_dm(clear_database, user_1, channel_1, dm_1, message_1, message_2):
    message_react(user_1['token'], message_2, REACT_ID)
    messages_json = dm_messages(user_1['token'], dm_1, 0)
    messages = messages_json.json()
    message = messages['messages'][0]
    assert message['message_id'] == 2
    assert message['u_id'] == 1
    assert message['message'] == 'Hello DM'
    assert message['reacts'][0]['react_id'] == 1
    assert message['reacts'][0]['u_ids'] == [1]
    assert message['reacts'][0]['is_this_user_reacted'] == True

def test_message_react_multiple_reacts_in_channel(clear_database, user_1, user_2, user_3, channel_1, message_1):
    channel_invite(user_1['token'], channel_1, user_2['auth_user_id'])
    channel_invite(user_1['token'], channel_1, user_3['auth_user_id'])
    message_react(user_1['token'], message_1, REACT_ID)
    message_react(user_2['token'], message_1, REACT_ID)
    messages_json = channel_messages(user_3['token'], channel_1, 0)
    messages = messages_json.json()
    message = messages['messages'][0]
    assert message['message_id'] == 1
    assert message['u_id'] == 1
    assert message['message'] == 'Hello World'
    assert message['reacts'][0]['react_id'] == 1
    assert message['reacts'][0]['u_ids'] == [1,2]
    assert message['reacts'][0]['is_this_user_reacted'] == False

def test_message_react_multiple_reacts_in_dm(clear_database, user_1, user_2, user_3, dm_1, message_2):
    dm_invite(user_1['token'], dm_1, user_2['auth_user_id'])
    dm_invite(user_1['token'], dm_1, user_3['auth_user_id'])
    message_react(user_1['token'], message_2, REACT_ID)
    message_react(user_2['token'], message_2, REACT_ID)
    messages_json = dm_messages(user_3['token'], dm_1, 0)
    messages = messages_json.json()
    message = messages['messages'][0]
    assert message['message_id'] == 1
    assert message['u_id'] == 1
    assert message['message'] == 'Hello DM'
    assert message['reacts'][0]['react_id'] == 1
    assert message['reacts'][0]['u_ids'] == [1,2]
    assert message['reacts'][0]['is_this_user_reacted'] == False

################################################################################
# message_unreact http tests                                                   #
################################################################################

def test_message_unreact_invalid_token(clear_database, user_1, channel_1, message_1):
    react = message_unreact(INVALID_TOKEN, message_1, REACT_ID)
    assert react.status_code == ACCESSERROR

def test_message_unreact_invalid_message_id(clear_database, user_1, channel_1, message_1):
    react = message_unreact(user_1['token'], INVALID_MESSAGE_ID, REACT_ID)
    assert react.status_code == INPUTERROR

def test_message_unreact_invalid_react_id(clear_database, user_1, channel_1, message_1):
    react = message_unreact(user_1['token'], message_1, INVALID_REACT_ID)
    assert react.status_code == INPUTERROR

def test_message_unreact_no_reacts(clear_database, user_1, channel_1, message_1):
    react = message_unreact(user_1['token'], message_1, REACT_ID)
    assert react.status_code == INPUTERROR

def test_message_has_already_unreacted(clear_database, user_1, channel_1, message_1):
    message_react(user_1['token'], message_1, REACT_ID)
    message_unreact(user_1['token'], message_1, REACT_ID)
    react = message_unreact(user_1['token'], message_1, REACT_ID)
    assert react.status_code == INPUTERROR

def test_message_unreact_user_not_in_channel(clear_database, user_1, user_2, channel_1, message_1):
    message_react(user_1['token'], message_1, REACT_ID)
    channel_leave(user_1['token'], channel_1)
    react = message_unreact(user_1['token'], message_1, REACT_ID)
    assert react.status_code == ACCESSERROR   

def test_message_unreact_user_not_in_dm(clear_database, user_1, user_2, dm_1, message_2):
    message_react(user_1['token'], message_2, REACT_ID)
    dm_leave(user_1['token'], dm_1)
    react = message_unreact(user_1['token'], message_2, REACT_ID)
    assert react.status_code == ACCESSERROR  

def test_message_unreact_valid_inputs_in_channel(clear_database, user_1, channel_1, message_1):
    message_react(user_1['token'], message_1, REACT_ID)
    message_unreact(user_1['token'], message_1, REACT_ID)
    messages_json = channel_messages(user_1['token'], channel_1, 0)
    messages = messages_json.json()
    message = messages['messages'][0]
    assert message['message_id'] == 1
    assert message['u_id'] == 1
    assert message['message'] == 'Hello World'
    assert message['reacts'][0]['react_id'] == 1
    assert message['reacts'][0]['u_ids'] == []
    assert message['reacts'][0]['is_this_user_reacted'] == False

def test_message_unreact_valid_inputs_in_dm(clear_database, user_1, channel_1, dm_1, message_1, message_2):
    message_react(user_1['token'], message_2, REACT_ID)
    message_unreact(user_1['token'], message_2, REACT_ID)
    messages_json = dm_messages(user_1['token'], dm_1, 0)
    messages = messages_json.json()
    message = messages['messages'][0]
    assert message['message_id'] == 2
    assert message['u_id'] == 1
    assert message['message'] == 'Hello DM'
    assert message['reacts'][0]['react_id'] == 1
    assert message['reacts'][0]['u_ids'] == []
    assert message['reacts'][0]['is_this_user_reacted'] == False

def test_message_unreact_multiple_reacts_in_channel(clear_database, user_1, user_2, user_3, channel_1, message_1):
    channel_invite(user_1['token'], channel_1, user_2['auth_user_id'])
    channel_invite(user_1['token'], channel_1, user_3['auth_user_id'])
    message_react(user_1['token'], message_1, REACT_ID)
    message_react(user_2['token'], message_1, REACT_ID)
    message_react(user_3['token'], message_1, REACT_ID)
    message_unreact(user_1['token'], message_1, REACT_ID)
    message_unreact(user_2['token'], message_1, REACT_ID)
    messages_json = channel_messages(user_3['token'], channel_1, 0)
    messages = messages_json.json()
    message = messages['messages'][0]
    assert message['message_id'] == 1
    assert message['u_id'] == 1
    assert message['message'] == 'Hello World'
    assert message['reacts'][0]['react_id'] == 1
    assert message['reacts'][0]['u_ids'] == [3]
    assert message['reacts'][0]['is_this_user_reacted'] == True

def test_message_unreact_multiple_reacts_in_dm(clear_database, user_1, user_2, user_3, dm_1, message_2):
    dm_invite(user_1['token'], dm_1, user_2['auth_user_id'])
    dm_invite(user_1['token'], dm_1, user_3['auth_user_id'])
    message_react(user_1['token'], message_2, REACT_ID)
    message_react(user_2['token'], message_2, REACT_ID)
    message_react(user_3['token'], message_2, REACT_ID)
    message_unreact(user_1['token'], message_2, REACT_ID)
    message_unreact(user_2['token'], message_2, REACT_ID)
    messages_json = dm_messages(user_3['token'], dm_1, 0)
    messages = messages_json.json()
    message = messages['messages'][0]
    assert message['message_id'] == 1
    assert message['u_id'] == 1
    assert message['message'] == 'Hello DM'
    assert message['reacts'][0]['react_id'] == 1
    assert message['reacts'][0]['u_ids'] == [3]
    assert message['reacts'][0]['is_this_user_reacted'] == True

################################################################################
# message_pin http tests                                                       #
################################################################################

def test_message_pin_invalid_token(clear_database, user_1, channel_1, message_1):
    pin = message_pin(INVALID_TOKEN, message_1)
    assert pin.status_code == ACCESSERROR

def test_message_pin_invalid_message_id(clear_database, user_1, channel_1, message_1):
    pin = message_pin(user_1['token'], INVALID_MESSAGE_ID)
    assert pin.status_code == INPUTERROR

def test_message_same_user_pin_again(clear_database, user_1, channel_1, message_1):
    message_pin(user_1['token'], message_1)
    pin = message_pin(user_1['token'], message_1)
    assert pin.status_code == INPUTERROR

def test_message_diff_user_pin_again(clear_database, user_1, user_2, channel_1, message_1):
    message_pin(user_1['token'], message_1)
    channel_invite(user_1['token'], channel_1, user_2['auth_user_id'])
    channel_addowner(user_1['token'], channel_1, user_2['auth_user_id'])
    pin = message_pin(user_2['token'], message_1)
    assert pin.status_code == INPUTERROR

def test_message_pin_user_not_in_channel(clear_database, user_1, user_2, channel_1, message_1):
    pin = message_pin(user_2['token'], message_1)
    assert pin.status_code == ACCESSERROR  

def test_message_pin_member_in_channel(clear_database, user_1, user_2, channel_1, message_1):
    channel_invite(user_1['token'], channel_1, user_2['auth_user_id'])
    pin = message_pin(user_2['token'], message_1)
    assert pin.status_code == ACCESSERROR  

def test_message_pin_user_not_in_dm(clear_database, user_1, user_2, dm_1, message_2):
    pin = message_pin(user_2['token'], message_2)
    assert pin.status_code == ACCESSERROR

def test_message_pin_valid_inputs_in_channel(clear_database, user_1, channel_1, message_1):
    message_pin(user_1['token'], message_1)
    messages_json = channel_messages(user_1['token'], channel_1, 0)
    messages = messages_json.json()
    message = messages['messages'][0]
    assert message['message_id'] == 1
    assert message['u_id'] == 1
    assert message['message'] == 'Hello World'
    assert message['is_pinned'] == True

def test_message_pin_valid_inputs_in_dm(clear_database, user_1, channel_1, dm_1, message_1, message_2):
    message_pin(user_1['token'], message_2)
    messages_json = dm_messages(user_1['token'], dm_1, 0)
    messages = messages_json.json()
    message = messages['messages'][0]
    assert message['message_id'] == 2
    assert message['u_id'] == 1
    assert message['message'] == 'Hello DM'
    assert message['is_pinned'] == True

def test_message_pin_another_user_in_channel(clear_database, user_1, user_2, channel_1, message_1):
    channel_invite(user_1['token'], channel_1, user_2['auth_user_id'])
    channel_addowner(user_1['token'], channel_1, user_2['auth_user_id'])
    message_pin(user_2['token'], message_1)
    messages_json = channel_messages(user_1['token'], channel_1, 0)
    messages = messages_json.json()
    message = messages['messages'][0]
    assert message['message_id'] == 1
    assert message['u_id'] == 1
    assert message['message'] == 'Hello World'
    assert message['is_pinned'] == True

################################################################################
# message_unpin http tests                                                       #
################################################################################

def test_message_unpin_invalid_token(clear_database, user_1, channel_1, message_1):
    message_pin(user_1['token'], message_1)
    pin = message_unpin(INVALID_TOKEN, message_1)
    assert pin.status_code == ACCESSERROR

def test_message_unpin_invalid_message_id(clear_database, user_1, channel_1, message_1):
    message_pin(user_1['token'], message_1)
    pin = message_unpin(user_1['token'], INVALID_MESSAGE_ID)
    assert pin.status_code == INPUTERROR

def test_message_same_user_unpin_again(clear_database, user_1, channel_1, message_1):
    message_pin(user_1['token'], message_1)
    message_unpin(user_1['token'], message_1)
    pin = message_unpin(user_1['token'], message_1)
    assert pin.status_code == INPUTERROR

def test_message_diff_user_unpin_again(clear_database, user_1, user_2, channel_1, message_1):
    message_pin(user_1['token'], message_1)
    channel_invite(user_1['token'], channel_1, user_2['auth_user_id'])
    channel_addowner(user_1['token'], channel_1, user_2['auth_user_id'])
    message_unpin(user_1['token'], message_1)
    pin = message_unpin(user_2['token'], message_1)
    assert pin.status_code == INPUTERROR

def test_message_unpin_user_not_in_channel(clear_database, user_1, user_2, channel_1, message_1):
    message_pin(user_1['token'], message_1)
    pin = message_unpin(user_2['token'], message_1)
    assert pin.status_code == ACCESSERROR 

def test_message_unpin_member_in_channel(clear_database, user_1, user_2, channel_1, message_1):
    channel_invite(user_1['token'], channel_1, user_2['auth_user_id'])
    message_pin(user_1['token'], message_1)
    pin = message_unpin(user_2['token'], message_1)
    assert pin.status_code == ACCESSERROR  

def test_message_unpin_user_not_in_dm(clear_database, user_1, user_2, dm_1, message_2):
    message_pin(user_1['token'], message_2)
    pin = message_unpin(user_2['token'], message_2)
    assert pin.status_code == ACCESSERROR

def test_message_unpin_valid_inputs_in_channel(clear_database, user_1, channel_1, message_1):
    message_pin(user_1['token'], message_1)
    message_unpin(user_1['token'], message_1)
    messages_json = channel_messages(user_1['token'], channel_1, 0)
    messages = messages_json.json()
    message = messages['messages'][0]
    assert message['message_id'] == 1
    assert message['u_id'] == 1
    assert message['message'] == 'Hello World'
    assert message['is_pinned'] == False

def test_message_unpin_valid_inputs_in_dm(clear_database, user_1, channel_1, dm_1, message_1, message_2):
    message_pin(user_1['token'], message_2)
    message_unpin(user_1['token'], message_2)
    messages_json = dm_messages(user_1['token'], dm_1, 0)
    messages = messages_json.json()
    message = messages['messages'][0]
    assert message['message_id'] == 2
    assert message['u_id'] == 1
    assert message['message'] == 'Hello DM'
    assert message['is_pinned'] == False

def test_message_unpin_another_user_in_channel(clear_database, user_1, user_2, channel_1, message_1):
    channel_invite(user_1['token'], channel_1, user_2['auth_user_id'])
    channel_addowner(user_1['token'], channel_1, user_2['auth_user_id'])
    message_pin(user_1['token'], message_1)
    message_unpin(user_2['token'], message_1)
    messages_json = channel_messages(user_1['token'], channel_1, 0)
    messages = messages_json.json()
    message = messages['messages'][0]
    assert message['message_id'] == 1
    assert message['u_id'] == 1
    assert message['message'] == 'Hello World'
    assert message['is_pinned'] == False

################################################################################
# message_sendlater http tests                                                 #
################################################################################

def test_message_sendlater_invalid_token(clear_database, user_1, channel_1, message_time):
    
    msg = requests.post(config.url + 'message/sendlater/v1', json={
        'token': INVALID_TOKEN,
        'channel_id': channel_1,
        'message': 'Hello World',
        'time_sent': message_time
    })
    assert msg.status_code == ACCESSERROR
    
def test_message_sendlater_invalid_channel(clear_database, user_1, channel_1, message_time):

    msg = requests.post(config.url + 'message/sendlater/v1', json={
        'token': user_1['token'],
        'channel_id': INVALID_CHANNEL_ID,
        'message': 'Hello World',
        'time_sent': message_time
    })
    assert msg.status_code == INPUTERROR
    
def test_message_sendlater_user_not_in_channel(clear_database, user_1, user_2, channel_1, channel_2, message_time):
    
    msg = requests.post(config.url + 'message/sendlater/v1', json={
        'token': user_2['token'],
        'channel_id': channel_1,
        'message': 'Hiya World!',
        'time_sent': message_time
    })
    assert msg.status_code == ACCESSERROR
    
def test_message_sendlater_invalid_length(clear_database, user_1, channel_1, message_time):
    i = 0
    message = ''
    while i < 500:
        message += str(i)
        i += 1

    msg = requests.post(config.url + 'message/sendlater/v1', json={
        'token': user_1['token'],
        'channel_id': channel_1,
        'message': message,
        'time_sent': message_time
    })
    assert msg.status_code == INPUTERROR

def test_message_sendlater_empty_message(clear_database, user_1, channel_1, message_time):

    msg = requests.post(config.url + 'message/sendlater/v1', json={
        'token': user_1['token'],
        'channel_id': channel_1,
        'message': '   ',
        'time_sent': message_time
    })
    assert msg.status_code == INPUTERROR

def test_message_sendlater_past_time(clear_database, user_1, channel_1):
    time = datetime.now() - timedelta(0, 5)
    send_time = round(time.replace(tzinfo=timezone.utc).timestamp())
    msg = requests.post(config.url + 'message/sendlater/v1', json={
        'token': user_1['token'],
        'channel_id': channel_1,
        'message': 'This will not be sent',
        'time_sent': send_time
    })
    assert msg.status_code == INPUTERROR

def check_before_send_time(token, channel_id, dm_id):
    if dm_id == -1:
        chan_msg = requests.get(f"{config.url}channel/messages/v2?token={token}&channel_id={channel_id}&start=0")
        chan_msg = chan_msg.json()
        assert chan_msg == {'messages': [], 'start': 0, 'end': -1}
    elif channel_id == -1:
        dm_msg = requests.get(f"{config.url}dm/messages/v1?token={token}&dm_id={dm_id}&start=0")
        dm_msg = dm_msg.json()
        assert dm_msg == {'messages': [], 'start': 0, 'end': -1}

def test_message_sendlater_valid_message(clear_database, user_1, channel_1):
    send_time = datetime.now() + timedelta(0, 5)
    send_time = round(send_time.replace(tzinfo=timezone.utc).timestamp())

    check_send = threading.Timer(4, check_before_send_time, args=(user_1['token'], channel_1, -1))
    check_send.start()
    message = requests.post(config.url + 'message/sendlater/v1', json={
        'token': user_1['token'],
        'channel_id': channel_1,
        'message': 'This is successful!',
        'time_sent': send_time
    })
    message = message.json()
    chan_msg = requests.get(f"{config.url}channel/messages/v2?token={user_1['token']}&channel_id={channel_1}&start=0")
    chan_msg = chan_msg.json()['messages']
    assert chan_msg[0]['message'] == 'This is successful!'
    assert chan_msg[0]['message_id'] == message['message_id']
    assert chan_msg[0]['u_id'] == user_1['auth_user_id']
    assert chan_msg[0]['time_created'] == send_time

################################################################################
# message_sendlaterdm http tests                                               #
################################################################################

def test_message_sendlaterdm_invalid_token(clear_database, user_1, dm_1, message_time):
    
    msg = requests.post(config.url + 'message/sendlaterdm/v1', json={
        'token': INVALID_TOKEN,
        'dm_id': dm_1,
        'message': 'Sending to DM...',
        'time_sent': message_time
    })
    assert msg.status_code == ACCESSERROR
    
def test_message_sendlaterdm_invalid_dm(clear_database, user_1, dm_1, message_time):

    msg = requests.post(config.url + 'message/sendlaterdm/v1', json={
        'token': user_1['token'],
        'dm_id': INVALID_DM_ID,
        'message': 'Hello World',
        'time_sent': message_time
    })
    assert msg.status_code == INPUTERROR
    
def test_message_sendlaterdm_user_not_in_channel(clear_database, user_1, user_2, dm_1, dm_2, message_time):
    
    msg = requests.post(config.url + 'message/sendlaterdm/v1', json={
        'token': user_2['token'],
        'dm_id': dm_1,
        'message': 'Hiya World!',
        'time_sent': message_time
    })
    assert msg.status_code == ACCESSERROR
    
def test_message_sendlaterdm_invalid_length(clear_database, user_1, dm_1, message_time):
    i = 0
    message = ''
    while i < 500:
        message += str(i)
        i += 1

    msg = requests.post(config.url + 'message/sendlaterdm/v1', json={
        'token': user_1['token'],
        'dm_id': dm_1,
        'message': message,
        'time_sent': message_time
    })
    assert msg.status_code == INPUTERROR

def test_message_sendlaterdm_empty_message(clear_database, user_1, dm_1, message_time):

    msg = requests.post(config.url + 'message/sendlaterdm/v1', json={
        'token': user_1['token'],
        'dm_id': dm_1,
        'message': '  \n  \t  ',
        'time_sent': message_time
    })
    assert msg.status_code == INPUTERROR

def test_message_sendlaterdm_past_time(clear_database, user_1, dm_1):
    time = datetime.now() - timedelta(0, 5)
    send_time = round(time.replace(tzinfo=timezone.utc).timestamp())
    msg = requests.post(config.url + 'message/sendlaterdm/v1', json={
        'token': user_1['token'],
        'dm_id': dm_1,
        'message': 'This is me from the past!!!',
        'time_sent': send_time
    })
    assert msg.status_code == INPUTERROR

def test_message_sendlaterdm_valid_message(clear_database, user_1, dm_1):
    send_time = datetime.now() + timedelta(0, 5)
    send_time = round(send_time.replace(tzinfo=timezone.utc).timestamp())

    check_send = threading.Timer(4, check_before_send_time, args=(user_1['token'], -1, dm_1))
    check_send.start()
    message = requests.post(config.url + 'message/sendlaterdm/v1', json={
        'token': user_1['token'],
        'dm_id': dm_1,
        'message': 'Delayed message for dm_1.',
        'time_sent': send_time
    })
    message = message.json()
    dm_msg = requests.get(f"{config.url}dm/messages/v1?token={user_1['token']}&dm_id={dm_1}&start=0")
    dm_msg = dm_msg.json()['messages']
    assert dm_msg[0]['message'] == 'Delayed message for dm_1.'
    assert dm_msg[0]['message_id'] == message['message_id']
    assert dm_msg[0]['u_id'] == user_1['auth_user_id']
    assert dm_msg[0]['time_created'] == send_time
