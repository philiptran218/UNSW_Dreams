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
# users_all http tests                                                         #
################################################################################

def expected_output_all_users():
    return {
        'users': [
            {
                'u_id': 1,
                'email': 'johnsmith@gmail.com',
                'name_first': 'John',
                'name_last': 'Smith',
                'handle_str': 'johnsmith',
            },
            {
                'u_id': 2,
                'email': 'philtran@gmail.com',
                'name_first': 'Philip',
                'name_last': 'Tran',
                'handle_str': 'philiptran',
            },
            {
                'u_id': 3,
                'email': 'terrynguyen@gmail.com',
                'name_first': 'Terrance',
                'name_last': 'Nguyen',
                'handle_str': 'terrancenguyen', 
            }
        ]   
    }

def test_all_invalid_token(clear_database, user_1, user_2, user_3):

    all_profiles = requests.get(f"{config.url}users/all/v1?token={INVALID_TOKEN}")
    assert all_profiles.status_code == ACCESSERROR

def test_all_valid(clear_database, user_1, user_2, user_3):
    all_profiles_json = requests.get(f"{config.url}users/all/v1?token={user_1['token']}")
    all_profiles = all_profiles_json.json()

    assert all_profiles == expected_output_all_users()
