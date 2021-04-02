import pytest
import requests
import json
from src import config

INVALID_TOKEN = -1
INVALID_U_ID = -1
INVALID_DM_ID = -1
INPUTERROR = 400
ACCESSERROR = 403


@pytest.fixture
def clear_data():
    requests.delete(config.url + 'clear/v1')

@pytest.fixture
def test_user1():
    user_info = requests.post(config.url + 'auth/register/v2', json={
        'email': 'validemail@g.com',
        'password': 'validpass',
        'name_first': 'validname',
        'name_last': 'validname'
    })
    return user_info.json()

@pytest.fixture
def test_user2():
    user_info = requests.post(config.url + 'auth/register/v2', json={
        'email': 'dan@gmail.com',
        'password': 'password',
        'name_first': 'dan',
        'name_last': 'smith'
    })
    return user_info.json()

@pytest.fixture
def test_user3():
    user_info = requests.post(config.url + 'auth/register/v2', json={
        'email': 'danimatt@gmail.com',
        'password': 'valpassword',
        'name_first': 'danny',
        'name_last': 'smithy'
    })
    return user_info.json()

@pytest.fixture
def test_user4():
    user_info = requests.post(config.url + 'auth/register/v2', json={
        'email': 'danny@gmail.com',
        'password': 'password123',
        'name_first': 'danny',
        'name_last': 'james'
    })
    return user_info.json()

@pytest.fixture
def test_create_dm(test_user1, test_user2):
    dm = requests.post(config.url + 'dm/create/v1', json={
        'token': test_user1['token'],
        'u_ids': [test_user2['auth_user_id']],
    })
    dm_info = dm.json()
    return dm_info


################################################################################
# dm_details http tests                                                        #
################################################################################

#Function that shows expected output for dm_details.
def expected_output_details_v2():
    return {
        "name": 'dansmith, validnamevalidname',
        "members": [
            {
                'u_id': 1,
                'name_first': 'validname',
                'name_last': 'validname',
                'email': 'validemail@g.com',
                'handle_str': 'validnamevalidname'
            },
            {
                'u_id': 2,
                'name_first': 'dan',
                'name_last': 'Smith',
                'email': 'dan@gmail.com',
                'handle_str': 'dansmith'
            }
        ]
    }


def test_dm_details_invalid_dm_id(clear_data, test_user1, test_create_dm):
    dm_det = requests.get(config.url + 'dm/details/v1', json={
        'token': test_user1['token'],
        'dm_id': INVALID_DM_ID,
    })
    assert dm_det.status_code == INPUTERROR

def test_dm_details_invalid_token(clear_data,test_user1,test_create_dm):
    dm_det = requests.get(config.url + 'dm/details/v1', json={
        'token': INVALID_TOKEN,
        'dm_id': test_create_dm['dm_id'],
    })
    assert dm_det.status_code == ACCESSERROR

def test_dm_details_invalid_not_in_dm(clear_data,test_user3,test_create_dm):
    dm_det = requests.get(config.url + 'dm/details/v1', json={
        'token': test_user3['token'],
        'dm_id': test_create_dm['dm_id'],
    })
    assert dm_det.status_code == ACCESSERROR

def test_dm_details_valid(clear_data,test_user1,test_create_dm):
    dm_det = requests.get(config.url + 'dm/details/v1', json={
        'token': test_user1['token'],
        'dm_id': test_create_dm['dm_id'],
    })
    dm_info = dm_det.json()
    assert dm_info == expected_output_details_v2()

################################################################################
# dm_list http tests                                                          #
################################################################################

#Function that shows expected output for dm_list.
def expected_output_list_v1():
    return {
        'dm': [
            {
                "dm_id": 1,
                "dm_name": "dansmith, validnamevalidname"
            }
        ]
    }

def test_dm_list_invalid_token(clear_data,test_user1,test_create_dm):
    dm_list = requests.get(config.url + 'dm/list/v1', json={
        'token': INVALID_TOKEN,
    })
    assert dm_list.status_code == ACCESSERROR

def test_dm_list_valid_empty(clear_data,test_user1):
    dm_list = requests.get(config.url + 'dm/list/v1', json={
        'token': test_user1['token'],
    })
    dm_info = dm_list.json()
    assert dm_info == {'dm': []}

def test_dm_list_valid(clear_data, test_user1, test_user2, test_create_dm):
    dm_list = requests.get(config.url + 'dm/list/v1', json={
        'token': test_user1['token'],
    })
    dm_info = dm_list.json()
    assert dm_info == expected_output_list_v1()

################################################################################
# dm_create http tests                                                         #
################################################################################

# Function that shows expected output for dm_create. Note it is different from the 
# output for list, despite looking similar.
def expected_output_create_v1():
    return {
        "dm_id": 1,
        "dm_name": "dansmith, validnamevalidname"
    }

def test_dm_create_invalid_token(clear_data,test_user1, test_user2):
    dm = requests.post(config.url + 'dm/create/v1', json={
        'token': INVALID_TOKEN,
        'u_ids': [test_user2['auth_user_id']]
    })
    assert dm.status_code == ACCESSERROR

def test_dm_create_invalid_u_id(clear_data,test_user1, test_user2):
    dm = requests.post(config.url + 'dm/create/v1', json={
        'token': test_user1['token'],
        'u_ids': [INVALID_U_ID]
    })
    assert dm.status_code == ACCESSERROR


def test_dm_create_valid(clear_data,test_user1, test_user2):
    dm = requests.post(config.url + 'dm/create/v1', json={
        'token': test_user1['token'],
        'u_ids': [test_user2['auth_user_id']]
    })
    dm_info = dm.json()
    assert dm_info == expected_output_create_v1()
