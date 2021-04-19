import pytest
import requests
import json
from src import config

INVALID_TOKEN = -1
INVALID_UID = -1
INVALID_RESET_CODE = -1
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
def clear_database():
    requests.delete(config.url + 'clear/v1')

################################################################################
# auth_register http tests                                                     #
################################################################################

def test_register_invalid_email(clear_database):
    user = requests.post(config.url + 'auth/register/v2', json={
        'email': 'johns@',
        'password': 'goodpass',
        'name_first': 'John',
        'name_last': 'Smith'
    })
    assert user.status_code == INPUTERROR

def test_register_invalid_first_name_1(clear_database):
    user = requests.post(config.url + 'auth/register/v2', json={
        'email': 'johnsmith@gmail.com',
        'password': 'goodpass',
        'name_first': 'Thisisaveryveryveryverylongfirstnameitrunsinthefamily',
        'name_last': 'Smith'
    })
    assert user.status_code == INPUTERROR
    
def test_register_invalid_first_name_2(clear_database):
    user = requests.post(config.url + 'auth/register/v2', json={
        'email': 'johnsmith@gmail.com',
        'password': 'goodpass',
        'name_first': '',
        'name_last': 'Smith'
    })
    assert user.status_code == INPUTERROR

def test_register_invalid_last_name_1(clear_database):
    user = requests.post(config.url + 'auth/register/v2', json={
        'email': 'johnsmith@gmail.com',
        'password': 'goodpass',
        'name_first': 'John',
        'name_last': 'Thisisaveryveryveryverylongfirstnameitrunsinthefamily'
    })
    assert user.status_code == INPUTERROR

def test_register_invalid_last_name_2(clear_database):
    user = requests.post(config.url + 'auth/register/v2', json={
        'email': 'johnsmith@gmail.com',
        'password': 'goodpass',
        'name_first': 'John',
        'name_last': ''
    })
    assert user.status_code == INPUTERROR

def test_register_invalid_password(clear_database):
    user = requests.post(config.url + 'auth/register/v2', json={
        'email': 'johnsmith@gmail.com',
        'password': '',
        'name_first': 'John',
        'name_last': 'Smith'
    })
    assert user.status_code == INPUTERROR
    
def test_register_duplicate_email(clear_database, user_1):
    user = requests.post(config.url + 'auth/register/v2', json={
        'email': 'johnsmith@gmail.com',
        'password': 'agreatpassword',
        'name_first': 'Smith',
        'name_last': 'John'
    })
    assert user.status_code == INPUTERROR
    
def test_register_multiple_users(clear_database):
    user_json = requests.post(config.url + 'auth/register/v2', json={
        'email': 'el_barto@gmail.com',
        'password': 'agreatpassword',
        'name_first': 'Bartholomew',
        'name_last': 'Simpson-Cartwright'
    })
    requests.post(config.url + 'auth/register/v2', json={
        'email': 'elbarto@gmail.com',
        'password': 'agreatpassword',
        'name_first': 'Bartholomew',
        'name_last': 'Simpson-Cartwright'
    })
    user = user_json.json()
    
    users_info_json = requests.get(f"{config.url}users/all/v1?token={user['token']}")
    users_info = users_info_json.json()['users']
    assert len(users_info) == 2
    assert users_info[0]['handle_str'] == 'bartholomewsimpson-c'
    assert users_info[1]['handle_str'] == 'bartholomewsimpson-0'

################################################################################
# auth_login http tests                                                        #
################################################################################

def test_login_valid(clear_database, user_1):
    user = requests.post(config.url + 'auth/login/v2', json={
        'email': 'johnsmith@gmail.com',
        'password': 'goodpass',
    })

    user1 = user.json()
    assert user1['auth_user_id'] == 1

def test_login_incorrect_password(clear_database, user_1):
    user = requests.post(config.url + 'auth/login/v2', json={
        'email': 'johnsmith@gmail.com',
        'password': 'badpass',
    })

    assert user.status_code == INPUTERROR

def test_login_unregistered_email(clear_database, user_1):
    user = requests.post(config.url + 'auth/login/v2', json={
        'email': 'unregisteredemail@gmail.com',
        'password': 'goodpass',
    })

    assert user.status_code == INPUTERROR
    
def test_login_invalid_email(clear_database, user_1):
    user = requests.post(config.url + 'auth/login/v2', json={
        'email': 'johns@',
        'password': 'goodpass',
        'name_first': 'John',
        'name_last': 'Smith'
    })
    assert user.status_code == INPUTERROR

def test_mix(clear_database, user_1, user_2):
    user1_login = requests.post(config.url + 'auth/login/v2', json={
        'email': 'johnsmith@gmail.com',
        'password': 'goodpass',
    })
    user1 = user1_login.json()
   
    user2_login = requests.post(config.url + 'auth/login/v2', json={
        'email': 'philtran@gmail.com',
        'password': 'goodpass',
    })
    user2 = user2_login.json()

    # These users should be able to logout if login worked
    user_1_json = requests.post(config.url + 'auth/logout/v1', json={
        'token': user_1['token']
    })
    user_1_logout = user_1_json.json()
    assert user_1_logout['is_success'] == True
    
    user_2_json = requests.post(config.url + 'auth/logout/v1', json={
        'token': user_2['token']
    })
    user_2_logout = user_2_json.json()
    assert user_2_logout['is_success'] == True
    
    user1_json = requests.post(config.url + 'auth/logout/v1', json={
        'token': user1['token']
    })
    user1_logout = user1_json.json()
    assert user1_logout['is_success'] == True
    
    user2_json = requests.post(config.url + 'auth/logout/v1', json={
        'token': user2['token']
    })
    user2_logout = user2_json.json()
    assert user2_logout['is_success'] == True
    
################################################################################
# auth_logout http tests                                                       #
################################################################################

def test_auth_logout_invalid_token(clear_database, user_1):
    user = requests.post(config.url + 'auth/logout/v1', json={
        'token': INVALID_TOKEN
    })
    assert user.status_code == ACCESSERROR
 
def test_auth_logout_again(clear_database, user_1):
    requests.post(config.url + 'auth/logout/v1', json={
        'token': user_1['token']
    })
    user = requests.post(config.url + 'auth/logout/v1', json={
        'token': user_1['token']
    })
    assert user.status_code == ACCESSERROR
  
def test_auth_logout_valid_simple(clear_database, user_1):
    logout_json = requests.post(config.url + 'auth/logout/v1', json={
        'token': user_1['token']
    })
    logout = logout_json.json()
    assert logout['is_success'] == True  
  
def test_auth_logout_multi_sessions(clear_database, user_1):
    session_json = requests.post(config.url + 'auth/login/v2', json={
        'email': 'johnsmith@gmail.com',
        'password': 'goodpass'
    })
    session = session_json.json()
    logout_1_json = requests.post(config.url + 'auth/logout/v1', json={
        'token': user_1['token']
    })
    logout_1 = logout_1_json.json()
    assert logout_1['is_success'] == True
    
    logout_2_json = requests.post(config.url + 'auth/logout/v1', json={
        'token': session['token']
    })
    logout_2 = logout_2_json.json()
    assert logout_2['is_success'] == True
    
def test_auth_logout_request(clear_database, user_1):
    logout_json = requests.post(config.url + 'auth/logout/v1', json={
        'token': user_1['token']
    })
    logout = logout_json.json()
    assert logout['is_success'] == True
    
    request = requests.post(config.url + 'channels/create/v2', json={
        'token': user_1['token'],
        'name': 'Channel 1',
        'is_public': True
    })
    assert request.status_code == ACCESSERROR

    
################################################################################
# auth_passwordreset_request http tests                                        #
################################################################################

def test_passwordreset_request_invalid_email_format(clear_database, user_1):
    reset = requests.post(config.url + 'auth/passwordreset/request/v1', json={
        'email': 'bademail',
    })

    assert reset.status_code == INPUTERROR

def test_passwordreset_request_unregistered_email(clear_database, user_1):
    reset = requests.post(config.url + 'auth/passwordreset/request/v1', json={
        'email': 'noemail@gmail.com',
    })

    assert reset.status_code == INPUTERROR

################################################################################
# auth_passwordreset_reset http tests                                          #
################################################################################

def test_passwordreset_reset_invalid_code(clear_database, user_1):
    reset = requests.post(config.url + 'auth/passwordreset/reset/v1', json={
        'reset_code': INVALID_RESET_CODE,
        'new_password': 'newpassword'
    })

    assert reset.status_code == INPUTERROR

