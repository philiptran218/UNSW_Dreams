import pytest
import requests
import json
from src import config
from datetime import timezone, datetime

INVALID_TOKEN = -1
INVALID_UID = -1
INVALID_COORDINATE = -1
LARGE_COORDINATE = 10000000000000000000
INPUTERROR = 400
ACCESSERROR = 403

DEFAULT_IMG_URL = "https://www.usbji.org/sites/default/files/person.jpg"
NEW_IMG_URL = "https://img1.looper.com/img/gallery/things-only-adults-notice-in-shrek/intro-1573597941.jpg"
INVALID_IMG_URL = "https://i.insider.com/5c59e77ceb3ce80d46564023?width=700"

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
def get_time():
    time = datetime.now()
    time = time.timestamp()
    time_issued = int(time)
    return time_issued

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
                'handle_str': 'johnsmith',
                'profile_img_url': config.url + "static/1.jpg",
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
                'handle_str': 'totallyoriginalhandl',
                'profile_img_url': config.url + "static/1.jpg",
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

def empty_stats_list(get_time):
    return {
        'user_stats': {
            'channels_joined': [{'num_channels_joined': 0, 'time_stamp': get_time}],
            'dms_joined': [{'num_dms_joined': 0, 'time_stamp': get_time}],
            'messages_sent': [{'num_messages_sent': 0, 'time_stamp': get_time}],
            'involvement_rate': 0.0
        }
    }

def stats_list(get_time):
   return {
        'user_stats': {
            'channels_joined': {'num_channels_joined': 1, 'time_stamp': get_time},
            'dms_joined': {'num_dms_joined': 1, 'time_stamp': get_time},
            'messages_sent': {'num_messages_sent': 1, 'time_stamp': get_time},
            'involvement_rate': 1.0
        }
    }

def test_user_stats_invalid_token(clear_database, user_1):
    stats = requests.get(f"{config.url}user/stats/v1?token={INVALID_TOKEN}")
    assert stats.status_code == ACCESSERROR

def test_user_stats_valid_empty(clear_database, user_1, get_time):
    stats = requests.get(f"{config.url}user/stats/v1?token={user_1['token']}")
    stats_info = stats.json()
    assert stats_info == empty_stats_list(get_time)

def test_user_stats_valid_full(clear_database, user_1, user_2, test_create_dm, channel_1, message_1, get_time):
    stats = requests.get(f"{config.url}user/stats/v1?token={user_1['token']}")
    output_stats = stats.json()
    expected_stats = stats_list(get_time)
    assert output_stats['user_stats']['channels_joined'][1] == expected_stats['user_stats']['channels_joined']
    assert output_stats['user_stats']['dms_joined'][1] == expected_stats['user_stats']['dms_joined']
    assert output_stats['user_stats']['messages_sent'][1] == expected_stats['user_stats']['messages_sent']
    assert output_stats['user_stats']['involvement_rate'] == expected_stats['user_stats']['involvement_rate']


################################################################################
# test_user_profile_uploadphoto http tests                                     #
################################################################################

def test_user_profile_uploadphoto_invalid_token(clear_database, user_1):
    photo = requests.post(config.url + "/user/profile/uploadphoto/v1", json={
        'token': INVALID_TOKEN,
        'img_url': NEW_IMG_URL,
        'x_start': 0,
        'y_start': 0,
        'x_end': 200,
        'y_end': 200,
    })
    assert photo.status_code == ACCESSERROR

def test_user_profile_uploadphoto_invalid_img_url(clear_database, user_1):
    photo = requests.post(config.url + "/user/profile/uploadphoto/v1", json={
        'token': user_1['token'],
        'img_url': INVALID_IMG_URL,
        'x_start': 0,
        'y_start': 0,
        'x_end': 200,
        'y_end': 200,
    })
    assert photo.status_code == INPUTERROR

def test_user_profile_uploadphoto_invalid_x_start_1(clear_database, user_1):
    photo = requests.post(config.url + "/user/profile/uploadphoto/v1", json={
        'token': user_1['token'],
        'img_url': NEW_IMG_URL,
        'x_start': INVALID_COORDINATE,
        'y_start': 0,
        'x_end': 200,
        'y_end': 200,
    })
    assert photo.status_code == INPUTERROR

def test_user_profile_uploadphoto_invalid_x_start_2(clear_database, user_1):
    photo = requests.post(config.url + "/user/profile/uploadphoto/v1", json={
        'token': user_1['token'],
        'img_url': NEW_IMG_URL,
        'x_start': LARGE_COORDINATE,
        'y_start': 0,
        'x_end': 200,
        'y_end': 200,
    })
    assert photo.status_code == INPUTERROR

def test_user_profile_uploadphoto_invalid_x_start_3(clear_database, user_1):
    photo = requests.post(config.url + "/user/profile/uploadphoto/v1", json={
        'token': user_1['token'],
        'img_url': NEW_IMG_URL,
        'x_start': 200,
        'y_start': 0,
        'x_end': 0,
        'y_end': 200,
    })
    assert photo.status_code == INPUTERROR

def test_user_profile_uploadphoto_invalid_y_start_1(clear_database, user_1):
    photo = requests.post(config.url + "/user/profile/uploadphoto/v1", json={
        'token': user_1['token'],
        'img_url': NEW_IMG_URL,
        'x_start': 0,
        'y_start': INVALID_COORDINATE,
        'x_end': 200,
        'y_end': 200,
    })
    assert photo.status_code == INPUTERROR

def test_user_profile_uploadphoto_invalid_y_start_2(clear_database, user_1):
    photo = requests.post(config.url + "/user/profile/uploadphoto/v1", json={
        'token': user_1['token'],
        'img_url': NEW_IMG_URL,
        'x_start': 0,
        'y_start': LARGE_COORDINATE,
        'x_end': 200,
        'y_end': 200,
    })
    assert photo.status_code == INPUTERROR

def test_user_profile_uploadphoto_invalid_y_start_3(clear_database, user_1):
    photo = requests.post(config.url + "/user/profile/uploadphoto/v1", json={
        'token': user_1['token'],
        'img_url': NEW_IMG_URL,
        'x_start': 0,
        'y_start':  INVALID_COORDINATE,
        'x_end': 200,
        'y_end': 0,
    })
    assert photo.status_code == INPUTERROR

def test_user_profile_uploadphoto_invalid_x_end_1(clear_database, user_1):
    photo = requests.post(config.url + "/user/profile/uploadphoto/v1", json={
        'token': user_1['token'],
        'img_url': NEW_IMG_URL,
        'x_start': 0,
        'y_start': 0,
        'x_end': INVALID_COORDINATE,
        'y_end': 200,
    })
    assert photo.status_code == INPUTERROR

def test_user_profile_uploadphoto_invalid_x_end_2(clear_database, user_1):
    photo = requests.post(config.url + "/user/profile/uploadphoto/v1", json={
        'token': user_1['token'],
        'img_url': NEW_IMG_URL,
        'x_start': 0,
        'y_start': 0,
        'x_end': LARGE_COORDINATE,
        'y_end': 200,
    })
    assert photo.status_code == INPUTERROR

def test_user_profile_uploadphoto_invalid_y_end_1(clear_database, user_1):
    photo = requests.post(config.url + "/user/profile/uploadphoto/v1", json={
        'token': user_1['token'],
        'img_url': NEW_IMG_URL,
        'x_start': 0,
        'y_start': 0,
        'x_end': 200,
        'y_end': INVALID_COORDINATE,
    })
    assert photo.status_code == INPUTERROR

def test_user_profile_uploadphoto_invalid_y_end_2(clear_database, user_1):
    photo = requests.post(config.url + "/user/profile/uploadphoto/v1", json={
        'token': user_1['token'],
        'img_url': NEW_IMG_URL,
        'x_start': 0,
        'y_start': 0,
        'x_end': 200,
        'y_end': LARGE_COORDINATE,
    })
    assert photo.status_code == INPUTERROR

def test_user_profile_uploadphoto_valid(clear_database, user_1):
    photo = requests.post(config.url + "/user/profile/uploadphoto/v1", json={
        'token': user_1['token'],
        'img_url': NEW_IMG_URL,
        'x_start': 0,
        'y_start': 0,
        'x_end': 200,
        'y_end': 200,
    })
    assert photo.status_code == 200
    profile = requests.get(f"{config.url}user/profile/v2?token={user_1['token']}&u_id={user_1['auth_user_id']}")
    user_1_profile = profile.json() 

    assert user_1_profile['user']['profile_img_url'] == config.url + "static/1.jpg"

