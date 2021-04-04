import pytest
import requests
import json
import string
import random

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
    requests.delete(config.url + 'clear/v1')

################################################################################
# clear_v1 http tests                                                          # 
################################################################################

def test_clear_users(clear_database,user_1):
    email = 'johnsmith@gmail.com'
    password = 'goodpass'
    requests.delete(config.url + 'clear/v1')

    login = requests.post(config.url + 'auth/login/v2', json={
        'email': email,
        'password': password
    })
    assert login.status_code == INPUTERROR

def test_clear_channels(clear_database, user_1,channel_1):
    requests.delete(config.url + 'clear/v1')

    user_info = requests.post(config.url + 'auth/register/v2', json={
        'email': "terrynguyen@gmail.com",
        'password': "password",
        'name_first': "Terry",
        'name_last': "Nguyen"
    })
    user_token= user_info.json()['token']

    chan = requests.get(f"{config.url}channels/listall/v2?token={user_token}")
    chan_list = chan.json()['channels']
    assert(not bool(chan_list))

################################################################################
# search_v1() tests                                                            #
################################################################################

def create_invalid_string():
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for counter in range(INVALID_STRING_LENGTH))

def send_channel_message(token, channel_id, message):
    requests.post(config.url + 'message/send/v2', json={
        'token': token,
        'channel_id': channel_id,
        'message': message
    })

def send_dm_message(token, dm_id, message):
    requests.post(config.url + 'message/senddm/v1', json={
        'token': token,
        'dm_id': dm_id,
        'message': message
    })

def test_other_search_invalid_token(clear_database, user_1):
    search = requests.get(f"{config.url}search/v2?token={INVALID_TOKEN}&query_str={MIXED_QUERY_STR}")
    assert search.status_code == ACCESSERROR

def test_other_search_invalid_query_str(clear_database, user_1):
    string = create_invalid_string()
    print(len(string))
    search = requests.get(f"{config.url}search/v2?token={user_1['token']}&query_str={string}")
    assert search.status_code == INPUTERROR

def test_other_search_valid_inputs(clear_database, user_1, user_2, user_3, channel_1, channel_2, dm_1, dm_2):
    send_channel_message(user_1['token'], channel_1, MIXED_QUERY_STR)
    send_dm_message(user_1['token'], dm_1, MIXED_QUERY_STR)
    send_channel_message(user_1['token'], channel_1, UPPER_CASE_STR)
    send_channel_message(user_2['token'], channel_2, SUB_STR)
    send_dm_message(user_2['token'], dm_2, UPPER_CASE_STR)
    send_dm_message(user_2['token'], dm_2, MIXED_QUERY_STR)
    send_dm_message(user_3['token'], dm_2, MIXED_QUERY_STR)
    search_json = requests.get(f"{config.url}search/v2?token={user_2['token']}&query_str={SUB_STR}")
    search = search_json.json()
    messages = search['messages']
    assert messages[0]['message_id'] == 2
    assert messages[0]['u_id'] == 1
    assert messages[0]['message'] == MIXED_QUERY_STR

    assert messages[1]['message_id'] == 4
    assert messages[1]['u_id'] == 2
    assert messages[1]['message'] == SUB_STR

    assert messages[2]['message_id'] == 6
    assert messages[2]['u_id'] == 2
    assert messages[2]['message'] == MIXED_QUERY_STR

    assert messages[3]['message_id'] == 7
    assert messages[3]['u_id'] == 3
    assert messages[3]['message'] == MIXED_QUERY_STR
    
################################################################################
# notifications_get_v1() tests                                                 #
################################################################################

def test_notifications_get_invalid_token(clear_database, user_1):

    notif = requests.get(f"{config.url}notifications/get/v1?token={INVALID_TOKEN}")
    assert notif.status_code == ACCESSERROR
    
def test_notifications_get_empty(clear_database, user_1):

    notif = requests.get(f"{config.url}notifications/get/v1?token={user_1['token']}")
    notif_info = notif.json()
    assert notif_info == {'notifications': []}

def test_notifications_get_share_dm_invite(clear_database, user_1, user_2, user_3, dm_2):

    requests.post(config.url + 'dm/invite/v1', json={
        'token': user_3['token'],
        'dm_id': dm_2,
        'u_id': user_1['auth_user_id']
    })
    msg = requests.post(config.url + 'message/senddm/v1', json={
        'token': user_2['token'],
        'dm_id': dm_2,
        'message': 'Hello @johnsmith and @terrancenguyen'
    })
    msg_info = msg.json()
    requests.post(config.url + 'message/share/v1', json={
        'token': user_2['token'],
        'og_message_id': msg_info['message_id'],
        'message': "And I'll tag myself too @philiptran",
        'channel_id': -1,
        'dm_id': dm_2
    })
    notif_1 = requests.get(f"{config.url}notifications/get/v1?token={user_1['token']}")
    notif_1_info = notif_1.json()['notifications']
    assert len(notif_1_info) == 3
    assert notif_1_info[0]['notification_message'] == 'philiptran tagged you in philiptran, terrancenguyen: Hello @johnsmith and'
    assert notif_1_info[1]['notification_message'] == 'philiptran tagged you in philiptran, terrancenguyen: Hello @johnsmith and'
    assert notif_1_info[2]['notification_message'] == 'terrancenguyen added you to philiptran, terrancenguyen'
    
    notif_2 = requests.get(f"{config.url}notifications/get/v1?token={user_2['token']}")
    notif_2_info = notif_2.json()['notifications']
    assert len(notif_2_info) == 1
    assert notif_2_info[0]['notification_message'] == 'philiptran tagged you in philiptran, terrancenguyen: Hello @johnsmith and'
    
    notif_3 = requests.get(f"{config.url}notifications/get/v1?token={user_3['token']}")
    notif_3_info = notif_3.json()['notifications']
    assert len(notif_3_info) == 3
    assert notif_3_info[0]['notification_message'] == 'philiptran tagged you in philiptran, terrancenguyen: Hello @johnsmith and'
    assert notif_3_info[1]['notification_message'] == 'philiptran tagged you in philiptran, terrancenguyen: Hello @johnsmith and'
    assert notif_3_info[2]['notification_message'] == 'philiptran added you to philiptran, terrancenguyen'


