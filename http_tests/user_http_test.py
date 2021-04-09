import pytest
import requests
import json
from src import config

INVALID_TOKEN = -1
INVALID_UID = -1
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
def test_create_dm(user_1,user_2):
    dm = requests.post(config.url + 'dm/create/v1', json={
        'token': user_1['token'],
        'u_ids': [user_2['auth_user_id']]
    })
    dm_info = dm.json()
    return dm_info

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
def message_1(user_1, test_create_dm):
    msg = requests.post(config.url + 'message/senddm/v1', json={
        'token': user_1['token'],
        'dm_id': test_create_dm['dm_id'],
        'message': 'Hello DM'
    })
    msg_info = msg.json()
    return msg_info['message_id']

@pytest.fixture 
def clear_database():
    requests.delete(config.url + 'clear/v1')

################################################################################
# user_profile http tests                                                      #
################################################################################

def expected_output_user1_profile():
    return {
        'user': 
            {
                'u_id': 1,
                'email': 'johnsmith@gmail.com',
                'name_first': 'John',
                'name_last': 'Smith',
                'handle_str': 'johnsmith'
            }
        
    }

def expected_output_user1_profilev2():
    return {
        'user':
            {
                'u_id': 1,
                'email': 'mynewemail@gmail.com',
                'name_first': 'Daniel',
                'name_last': 'Nguyen',
                'handle_str': 'totallyoriginalhandl'
            }
    }

def test_simple_profile(clear_database, user_1):
    profile_json = requests.get(f"{config.url}user/profile/v2?token={user_1['token']}&u_id={user_1['auth_user_id']}")  
    profile = profile_json.json()
    assert profile == expected_output_user1_profile()

def test_profile_invalid_token(clear_database, user_1):
    profile = requests.get(f"{config.url}user/profile/v2?token={INVALID_TOKEN}&u_id={user_1['auth_user_id']}")
    assert profile.status_code == ACCESSERROR

def test_profile_invalid_u_id(clear_database, user_1):
    profile = requests.get(f"{config.url}user/profile/v2?token={user_1['token']}&u_id={INVALID_UID}")
    assert profile.status_code == INPUTERROR

################################################################################
# user_set_email http tests                                                    #
################################################################################

def test_set_email(clear_database, user_1):
    requests.put(config.url + 'user/profile/setemail/v2', json={
        'token': user_1['token'],
        'email': "newemail@gmail.com",
    })
    profile = requests.get(f"{config.url}user/profile/v2?token={user_1['token']}&u_id={user_1['auth_user_id']}")
    user_1_profile = profile.json() 

    assert user_1_profile['user']['email'] == "newemail@gmail.com"

def test_invalid_email(clear_database, user_1):
    profile = requests.put(config.url + 'user/profile/setemail/v2', json={
        'token': user_1['token'],
        'email': 'bademail',
    })

    assert profile.status_code == INPUTERROR

def test_invalid_token(clear_database, user_1):
    profile = requests.put(config.url + 'user/profile/setemail/v2', json={
        'token': INVALID_TOKEN,
        'email': 'newemail@gmail.com',
    })

    assert profile.status_code == ACCESSERROR

################################################################################
# user_set_handle http tests                                                   #
################################################################################
def test_empty_handle(clear_database, user_1):
    profile = requests.put(config.url + 'user/profile/sethandle/v1', json={
        'token': user_1['token'],
        'handle_str': '',
    })
    assert profile.status_code == INPUTERROR

def test_invalid_handle(clear_database, user_1):
    profile = requests.put(config.url + 'user/profile/sethandle/v1', json={
        'token': user_1['token'],
        'handle_str': 'thiscontainsmorelettersthanisallowed',
    })
    assert profile.status_code == INPUTERROR

def test_handle_invalid_token(clear_database, user_1):
    profile = requests.put(config.url + 'user/profile/sethandle/v1', json={
        'token': INVALID_TOKEN,
        'handle_str': 'perfect',
    })
    assert profile.status_code == ACCESSERROR

################################################################################
# test_set_name http tests                                                     #
################################################################################
def test_setname_invalid_token(clear_database, user_1):
    profile = requests.put(config.url + 'user/profile/setname/v2', json={
        'token': INVALID_TOKEN,
        'name_first': 'Evan',
        'name_last': 'Baxter',
    })
    assert profile.status_code == ACCESSERROR

def test_setname_empty_first(clear_database, user_1):
    profile = requests.put(config.url + 'user/profile/setname/v2', json={
        'token': user_1['token'],
        'name_first': '',
        'name_last': 'Baxter',
    })
    assert profile.status_code == INPUTERROR
    
def test_setname_empty_last(clear_database, user_1):
    profile = requests.put(config.url + 'user/profile/setname/v2', json={
        'token': user_1['token'],
        'name_first': 'Evan',
        'name_last': '',
    })
    assert profile.status_code == INPUTERROR

def test_setname_long_first(clear_database, user_1):
    profile = requests.put(config.url + 'user/profile/setname/v2', json={
        'token': user_1['token'],
        'name_first': 'Thisismynamebutitmaybetoolongfortheapplicationtoaccept',
        'name_last': 'Baxter',
    })
    assert profile.status_code == INPUTERROR
    
def test_setname_long_last(clear_database, user_1):
    profile = requests.put(config.url + 'user/profile/setname/v2', json={
        'token': user_1['token'],
        'name_first': 'Evan',
        'name_last': 'Thisismysurnameanditisveryveryverylongandtakesalongtimetowrite',
    })
    assert profile.status_code == INPUTERROR

################################################################################
# test_all_user_func http tests                                                #
################################################################################

def set_email(token, email):
    requests.put(config.url + 'user/profile/setemail/v2', json={
        'token': token,
        'email': email,
    })

def set_name(token, name_first, name_last):
    requests.put(config.url + 'user/profile/setname/v2', json={
        'token': token,
        'name_first': name_first,
        'name_last': name_last,
    })

def set_handle(token, handle_str):
    requests.put(config.url + 'user/profile/sethandle/v1', json={
        'token': token,
        'handle_str': handle_str,
    })

def test_user_func(clear_database, user_1):
    set_email(user_1['token'], "mynewemail@gmail.com")
    set_name(user_1['token'], "Daniel", "Nguyen")
    set_handle(user_1['token'], "totallyoriginalhandl")
    
    profile_json = requests.get(f"{config.url}user/profile/v2?token={user_1['token']}&u_id={user_1['auth_user_id']}")
    profile = profile_json.json()
    assert profile == expected_output_user1_profilev2()

def test_multi_user(clear_database, user_1, user_2, user_3):
    set_email(user_2['token'], "potato@gmail.com")
    set_email(user_3['token'], "compgod@gmail.com")
    set_handle(user_1['token'], "dropout")
    set_name(user_2['token'], "Dark", "Soul")
    set_handle(user_3['token'], "gamer")

    profile_1 = requests.get(f"{config.url}user/profile/v2?token={user_1['token']}&u_id={user_1['auth_user_id']}")
    user_1_profile = profile_1.json() 

    profile_2 = requests.get(f"{config.url}user/profile/v2?token={user_2['token']}&u_id={user_2['auth_user_id']}")
    user_2_profile = profile_2.json()

    profile_3 = requests.get(f"{config.url}user/profile/v2?token={user_3['token']}&u_id={user_3['auth_user_id']}")
    user_3_profile = profile_3.json()  

    assert user_1_profile['user']['handle_str'] == "dropout"
    assert user_2_profile['user']['name_first'] == "Dark"
    assert user_2_profile['user']['name_last'] == "Soul"
    assert user_2_profile['user']['email'] == "potato@gmail.com"
    assert user_3_profile['user']['email'] == "compgod@gmail.com"
    assert user_3_profile['user']['handle_str'] == "gamer"

################################################################################
# test_user_stats http tests                                                   #
################################################################################

def empty_stats_list():
    return {
        'channels_joined': 0,
        'dms_joined': 0,
        'messages_sent': 0,
        'involvement_rate': 0,
    }

def stats_list():
    return {
        'channels_joined': 1,
        'dms_joined': 1,
        'messages_sent': 1,
        'involvement_rate': 1,
    }

def test_user_stats_invalid_token(clear_database, user_1):
    stats = requests.get(f"{config.url}user/stats/v1?{INVALID_TOKEN}")
    assert stats.status_code == ACCESSERROR

def test_user_stats_valid_empty(clear_database, user_1):
    stats = requests.get(f"{config.url}user/stats/v1?{user_1['token']}")
    stats_info = stats.json()
    assert stats_info == empty_stats_list()

def test_user_stats_valid_full(clear_database, user_1, user_2, test_create_dm, channel_1, message_1):
    stats = requests.get(f"{config.url}user/stats/v1?{user_1['token']}")
    stats_info = stats.json()
    assert stats_info == stats_list()
    


