from src.user import user_profile_v1, user_profile_setname_v1, user_profile_setemail_v1, user_profile_sethandle_v1, user_profile_uploadphoto_v1, user_stats_v1
from src.auth import auth_login_v1, auth_register_v1
from src.error import InputError, AccessError
from src.dm import dm_create_v1
from src.channels import channels_create_v1
from src.message import message_senddm_v1
from src.other import clear_v1
from datetime import timezone, datetime

from src import config

import pytest

INVALID_VALUE = -1
INVALID_TOKEN = -1
INVALID_COORDINATE = -1
LARGE_COORDINATE = 10000000000000000000

DEFAULT_IMG_URL = "https://www.usbji.org/sites/default/files/person.jpg"
NEW_IMG_URL = "https://img1.looper.com/img/gallery/things-only-adults-notice-in-shrek/intro-1573597941.jpg"
INVALID_IMG_URL = "https://i.insider.com/5c59e77ceb3ce80d46564023?width=700"

#################################################################################
#   Fixtures                                                                    #
#################################################################################

@pytest.fixture
def user_1():
    user = auth_register_v1("johnsmith@gmail.com", "password", "John", "Smith")
    return user

@pytest.fixture
def user_2():
    user = auth_register_v1("terrynguyen@gmail.com", "password", "Terry", "Nguyen")
    return user

@pytest.fixture
def channel1(user_1):
    channel = channels_create_v1(user_1['token'], "channel1", True)
    return channel

@pytest.fixture
def dm1(user_1, user_2):
    dm = dm_create_v1(user_1['token'], [user_2['auth_user_id']])
    return dm

@pytest.fixture
def message1(user_1, user_2, dm1):
    message = message_senddm_v1(user_1['token'], dm1['dm_id'], 'Hello DM')
    return message

@pytest.fixture
def get_time():
    time = datetime.today()
    time = time.replace(tzinfo=timezone.utc).timestamp()
    time_issued = round(time)
    return time_issued

@pytest.fixture
def clear_data():
    clear_v1()

#################################################################################
#   user_profile_v1 testing functions                                           #
#################################################################################

def test_valid_user_profile_v1(clear_data): 
    new_user = auth_register_v1("validemail@gmail.com", "Thisisagoodpassword123", "John", "Smith")
    user = user_profile_v1(new_user.get('token'), new_user.get('auth_user_id'))
    assert user['user']['u_id'] == new_user.get('auth_user_id')
    assert user['user']['email'] == "validemail@gmail.com"
    assert user['user']['name_first'] == "John"
    assert user['user']['name_last'] == "Smith"
    assert user['user']['handle_str'] == "johnsmith"
    assert user['user']['profile_img_url'] == config.url + "static/1.jpg"

def test_profile_unregistered_user(clear_data):
    with pytest.raises(AccessError):
        user_profile_v1('invalid_token', 'invalid_u_id')
    
def test_profile_invalid_u_id(clear_data):
    new_user = auth_register_v1("validemail@gmail.com", "Thisisagoodpassword123", "John", "Smith")
    with pytest.raises(InputError):
        user_profile_v1(new_user.get('token'), INVALID_VALUE)

def test_user_profile_invalid_token(clear_data):
    new_user = auth_register_v1("validemail@gmail.com", "Thisisagoodpassword123", "John", "Smith")
    with pytest.raises(AccessError):
        user_profile_v1(INVALID_VALUE, new_user['auth_user_id'])

#################################################################################
#   user_profile_setname_v1 testing functions                                   #
#################################################################################

def test_setname_first_pass(clear_data):
    new_user = auth_register_v1("validemail@gmail.com", "GoodPassword23", "Jason", "Bourne")
    user_token = new_user.get("token")
    user_profile_setname_v1(user_token, "Jake", "Bourne")
    new_first_name_check = user_profile_v1(new_user.get('token'), new_user.get('auth_user_id'))
    assert new_first_name_check['user']['name_first'] == "Jake"

def test_setname_last_pass(clear_data):
    new_user = auth_register_v1("validemail@gmail.com", "GoodPassword23", "Jason", "Bourne")
    user_token = new_user.get("token")
    user_profile_setname_v1(user_token, "Jason", "Smith")
    new_last_name_check = user_profile_v1(new_user.get('token'), new_user.get('auth_user_id'))
    assert new_last_name_check['user']['name_last'] == "Smith"

def test_setname_first_too_long(clear_data):
    new_user = auth_register_v1("validemail@gmail.com", "GoodPassword23", "Jason", "Bourne")
    user_token = new_user.get("token")
    
    with pytest.raises(InputError):
        user_profile_setname_v1(user_token, "Thiscantpossiblybesomeonesnameasitistoolongandhardtoread", "Bourne")

def test_setname_first_too_short(clear_data):
    new_user = auth_register_v1("validemail@gmail.com", "GoodPassword23", "Jason", "Bourne")    
    user_token = new_user.get("token")
    
    with pytest.raises(InputError):
        user_profile_setname_v1(user_token, "", "Bourne")

def test_setname_last_too_long(clear_data):
    new_user = auth_register_v1("validemail@gmail.com", "GoodPassword23", "Jason", "Bourne")    
    user_token = new_user.get("token")
    
    with pytest.raises(InputError):
        user_profile_setname_v1(user_token, "Jason", "Thisisaverylonglonglonglonglonglonglonglonglastname")

def test_setname_last_too_short(clear_data):
    new_user = auth_register_v1("validemail@gmail.com", "GoodPassword23", "Jason", "Bourne")    
    user_token = new_user.get("token")
    
    with pytest.raises(InputError):
        user_profile_setname_v1(user_token, "Jason", "")

def test_setname_invalid_token(clear_data):
    auth_register_v1("validemail@gmail.com", "GoodPassword23", "Jason", "Bourne")

    with pytest.raises(AccessError):
        user_profile_setname_v1("invalid", "Not", "JasonBourne")

#################################################################################
#   user_profile_setemail_v1 testing functions                                  #
#################################################################################

def test_setemail_pass(clear_data):
    new_user = auth_register_v1("validemail@gmail.com", "GoodPassword10", "Kevin", "Tran")
    user_token = new_user.get("token")
    user_profile_setemail_v1(user_token, "newemail@gmail.com")
    email = user_profile_v1(user_token, new_user.get("auth_user_id")).get("user").get("email")
    assert email == "newemail@gmail.com"

def test_invalid_token(clear_data):
    with pytest.raises(AccessError):
        user_profile_setemail_v1(INVALID_VALUE, 'bademail')

def test_invalid_email(clear_data):
    new_user = auth_register_v1("thisismyemail@gmail.com", "Thisisagoodpass12", "Alex", "Knight")
    with pytest.raises(InputError):
        user_profile_setemail_v1(new_user.get('token'), 'bademail')
    
def test_sameemail(clear_data):
    new_user = auth_register_v1("thisismyemail@gmail.com", "Thisisagoodpass12", "Alex", "Knight")
    with pytest.raises(InputError):
        user_profile_setemail_v1(new_user.get('token'), 'thisismyemail@gmail.com')

def test_email_taken(clear_data):
    auth_register_v1("thisismyemail@gmail.com", "Thisisagoodpass12", "Alex", "Knight")
    new_user2 = auth_register_v1("somethingcompletelyrandom@gmail.com", "Thisismyaccount24", "John", "Stone")

    with pytest.raises(InputError):
        user_profile_setemail_v1(new_user2.get('token'), 'thisismyemail@gmail.com')
    
def test_unregistered_user(clear_data):
    with pytest.raises(AccessError):
        user_profile_v1('invalid_token', 'invalid_u_id')

#################################################################################
#   user_profile_sethandle_v1 testing functions                                 #
#################################################################################

def test_handle_simple_pass(clear_data):
    new_user = auth_register_v1("myemail@gmail.com", "my12password", "Brad", "Lee")
    new_user_token = new_user.get("token")

    user_profile_sethandle_v1(new_user_token, "MyHandle")
    user = user_profile_v1(new_user.get("token"), new_user.get('auth_user_id'))

    assert user['user']['handle_str'] == "MyHandle"


def test_invalid_handle(clear_data):
    new_user = auth_register_v1("validemail@gmail.com", "PaSsWoRd321My", "Ash", "Ketchum")
    new_user_token = new_user.get("token")

    with pytest.raises(InputError):
        user_profile_sethandle_v1(new_user_token, '')

def test_invalid_long_handle(clear_data):
    new_user = auth_register_v1("validemail@gmail.com", "PaSsWoRd321My", "Ash", "Ketchum")
    new_user_token = new_user.get("token")

    with pytest.raises(InputError):
        user_profile_sethandle_v1(new_user_token, 'thisisaverylonghandlethatcantbeused')

def test_handle_taken(clear_data):
    new_user1 = auth_register_v1("validemail@gmail.com", "PaSsWoRd321My", "Ash", "Ketchum")
    new_user1_token = new_user1.get("token")
    user_profile_sethandle_v1(new_user1_token, "PokemonMaster")

    new_user2 = auth_register_v1("thisemail@gmail.com", "DifferentPassword", "Gary", "Oak")
    new_user2_token = new_user2.get("token")
    with pytest.raises(InputError):
        user_profile_sethandle_v1(new_user2_token, "PokemonMaster")

def test_sethandle_invalid_token(clear_data):
    auth_register_v1("thismyemail@gmail.com", "whatisapassword1", "Bill", "Gates")

    with pytest.raises(AccessError):
        user_profile_sethandle_v1("invalid", 'mycrosoft')

################################################################################
# user_profile_uploadphoto_v1 tests                                            #
################################################################################

def expected_output_uploadphoto():
    return { 'user': {
        'u_id': 1,
        'email': 'johnsmith@gmail.com',
        'name_first': 'John',
        'name_last': 'Smith', 
        'handle_str': "johnsmith",
        'profile_img_url': config.url + "static/1.jpg", 
    }
    }

def test_user_photo_invalid_token(clear_data, user_1):
    with pytest.raises(AccessError):
        user_profile_uploadphoto_v1(INVALID_TOKEN, NEW_IMG_URL, 0, 0, 200, 200)

def test_user_photo_invalid_not_jpg(clear_data, user_1):
    with pytest.raises(InputError):
        user_profile_uploadphoto_v1(user_1['token'], INVALID_IMG_URL, 0, 0, 200, 200)

def test_user_photo_negative_x_start(clear_data, user_1):
    with pytest.raises(InputError):
        user_profile_uploadphoto_v1(user_1['token'], NEW_IMG_URL, INVALID_COORDINATE, 0, 200, 200)

def test_user_photo_too_large_x_start(clear_data, user_1):
    with pytest.raises(InputError):
        user_profile_uploadphoto_v1(user_1['token'], NEW_IMG_URL, LARGE_COORDINATE, 0, 200, 200)

def test_user_photo_negative_y_start(clear_data, user_1):
    with pytest.raises(InputError):
        user_profile_uploadphoto_v1(user_1['token'], NEW_IMG_URL, 0, INVALID_COORDINATE, 200, 200)

def test_user_photo_too_large_y_start(clear_data, user_1):
    with pytest.raises(InputError):
        user_profile_uploadphoto_v1(user_1['token'], NEW_IMG_URL, 0, LARGE_COORDINATE, 200, 200)

def test_user_photo_neagtive_x_end(clear_data, user_1):
    with pytest.raises(InputError):
        user_profile_uploadphoto_v1(user_1['token'], NEW_IMG_URL, 0, 0, INVALID_COORDINATE, 200)
    
def test_user_photo_too_large_x_end(clear_data, user_1):
    with pytest.raises(InputError):
        user_profile_uploadphoto_v1(user_1['token'], NEW_IMG_URL, 0, 0, LARGE_COORDINATE, 200)

def test_user_photo_negative_y_end(clear_data, user_1):
    with pytest.raises(InputError):
        user_profile_uploadphoto_v1(user_1['token'], NEW_IMG_URL, 0, 0, 200, INVALID_COORDINATE)
    
def test_user_photo_too_large_y_end(clear_data, user_1):
    with pytest.raises(InputError):
        user_profile_uploadphoto_v1(user_1['token'], NEW_IMG_URL, 0, 0, 200, LARGE_COORDINATE)

def test_user_photo_valid(clear_data, user_1, user_2):
    user_profile_uploadphoto_v1(user_1['token'], NEW_IMG_URL, 0, 0, 600, 500)
    assert user_profile_v1(user_2['token'], user_1['auth_user_id']) == expected_output_uploadphoto()

################################################################################
# user_stats_v1 tests                                                          #
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
            'channels_joined': [{'num_channels_joined': 1, 'time_stamp': get_time}],
            'dms_joined': [{'num_dms_joined': 1, 'time_stamp': get_time}],
            'messages_sent': [{'num_messages_sent': 1, 'time_stamp': get_time}],
            'involvement_rate': 1.0
        }
    }

def test_user_stats_invalid_token(clear_data):
    with pytest.raises(AccessError):
        user_stats_v1(INVALID_TOKEN) 

def test_user_stats_valid_empty(clear_data, user_1, get_time):
    assert user_stats_v1(user_1['token']) == empty_stats_list(get_time)

def test_user_stats_valid(clear_data, user_1, user_2, channel1, dm1, message1, get_time):
    assert user_stats_v1(user_1['token']) == stats_list(get_time)