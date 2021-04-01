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
    requests.delete(config.url + 'clear')

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
def test_create_dm(test_user1,test_user2):
    dm = requests.post(config.url + 'dm/create/v1', json={
        'token': test_user1['token'],
        'u_ids': [test_user2['auth_user_id']]
    })
    dm_info = dm.json()
    return dm_info['dm_id']


################################################################################
# dm_invite_v1 https tests                                                     #
################################################################################

def test_dm_invite_invalid_dm_id(clear_data,test_user1,test_user2,test_create_dm):
    dm_inv = requests.post(config.url + 'dm/invite/v1', json={
        'token': test_user1['token'],
        'dm_id': INVALID_DM_ID,
        'u_id': test_user2['auth_user_id']
    })
    assert dm_inv.status_code == INPUTERROR

def test_dm_invite_invalid_u_id(clear_data,test_user1,test_user2,test_create_dm):
    dm_inv = requests.post(config.url + 'dm/invite/v1', json={
        'token': test_user1['token'],
        'dm_id': test_create_dm,
        'u_id': INVALID_U_ID
    })
    assert dm_inv.status_code == INPUTERROR

def test_dm_invite_user_not_a_member(clear_data,test_user1,test_user2,test_user3,test_create_dm):
    dm_inv = requests.post(config.url + 'dm/invite/v1', json={
        'token': test_user3['token'],
        'dm_id': test_create_dm,
        'u_id': test_user2['auth_user_id']
    })
    assert dm_inv.status_code == ACCESSERROR

def test_dm_invite_invalid_token(clear_data,test_user1,test_user2,test_create_dm):
    dm_inv = requests.post(config.url + 'dm/invite/v1', json={
        'token': INVALID_TOKEN,
        'dm_id': test_create_dm,
        'u_id': test_user2['auth_user_id']
    })
    assert dm_inv.status_code == ACCESSERROR   

def test_dm_invite_already_in_dm(clear_data,test_user1,test_user2,test_create_dm):
    dm_inv = requests.post(config.url + 'dm/invite/v1', json={
        'token': test_user1['token'],
        'dm_id': test_create_dm,
        'u_id': test_user2['auth_user_id']
    })
    assert dm_inv.json()== {} #.json()?

def test_dm_invite_valid(clear_data,test_user1,test_user2,test_user4,test_create_dm):
    requests.post(config.url + 'dm/invite/v1', json={
        'token': test_user1['token'],
        'dm_id': test_create_dm,
        'u_id': test_user4['auth_user_id']
    })
    
    member_check = False
    dm_deets = requests.get(config.url + 'dm/details/v1', json={
        'token': test_user1['token'],
        'dm_id': test_create_dm
    }) 
    members_list = dm_deets.json()['members']
    for member in members_list:
        if member['u_id'] == test_user4['auth_user_id']:
            member_check = True
    assert(member_check)



