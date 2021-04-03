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

def test_register_invalid_first_name(clear_database):
    user = requests.post(config.url + 'auth/register/v2', json={
        'email': 'johnsmith@gmail.com',
        'password': 'goodpass',
        'name_first': 'Thisisaveryveryveryverylongfirstnameitrunsinthefamily',
        'name_last': 'Smith'
    })
    assert user.status_code == INPUTERROR

def test_register_invalid_last_name(clear_database):
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

def test_mix(clear_database, user_1, user_2):
    user1 = requests.post(config.url + 'auth/login/v2', json={
        'email': 'johnsmith@gmail.com',
        'password': 'goodpass',
    })

    user1 = user1.json()
   
    user3 = requests.post(config.url + 'auth/register/v2', json={
        'email': 'terrynguyen@gmail.com',
        'password': 'goodpass',
        'name_first': 'Terrance',
        'name_last': 'Nguyen'
    })
    user3 = user3.json()

    user2_login = requests.post(config.url + 'auth/login/v2', json={
        'email': 'philtran@gmail.com',
        'password': 'goodpass',
    })

    user2 = user2_login.json()

    user3_login = requests.post(config.url + 'auth/login/v2', json={
        'email': 'terrynguyen@gmail.com',
        'password': 'goodpass',
    })

    user3 = user3_login.json()

    assert {}