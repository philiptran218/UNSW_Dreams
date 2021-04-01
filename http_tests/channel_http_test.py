import pytest
import requests
import json
from src import config

INVALID_TOKEN = -1
INVALID_CHANNEL_ID = -1
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
def make_user_2_owner_in_channel_1(user_1, user_2, channel_1):
    requests.post(config.url + 'channel/invite/v2', json={
        'token': user_1['token'],
        'channel_id': channel_1,
        'u_id': user_2['auth_user_id']
    })
    requests.post(config.url + 'channel/addowner/v1', json={
        'token': user_1['token'],
        'channel_id': channel_1,
        'u_id': user_2['auth_user_id']
    })

@pytest.fixture 
def clear_database():
    requests.delete(config.url + 'clear')

################################################################################
# channel_invite http tests                                                    #
################################################################################

def test_channel_invite_invalid_token(clear_database, user_1, user_2, channel_1):
    
    invite = requests.post(config.url + 'channel/invite/v2', json={
        'token': INVALID_TOKEN,
        'channel_id': channel_1,
        'u_id': user_2['auth_user_id']
    })

    assert invite.status_code == ACCESSERROR

def test_channel_invite_invalid_channel(clear_database, user_1, user_2, channel_1):
    
    invite = requests.post(config.url + 'channel/invite/v2', json={
        'token': user_1['token'],
        'channel_id': INVALID_CHANNEL_ID,
        'u_id': user_2['auth_user_id']
    })

    assert invite.status_code == INPUTERROR

def test_channel_invite_invalid_uid(clear_database, user_1, user_2, channel_1):
    
    invite = requests.post(config.url + 'channel/invite/v2', json={
        'token': user_1['token'],
        'channel_id': channel_1,
        'u_id': INVALID_UID
    })

    assert invite.status_code == INPUTERROR

def test_channel_invite_invalid_auth_id(clear_database, user_1, user_2, user_3, channel_1):
    
    invite = requests.post(config.url + 'channel/invite/v2', json={
        'token': user_2['token'],
        'channel_id': channel_1,
        'u_id': user_3['auth_user_id']
    })

    assert invite.status_code == ACCESSERROR

def test_invite_duplicate_uid(clear_database, user_1, user_2, channel_1):

    requests.post(config.url + 'channel/invite/v2', json={
        'token': user_1['token'],
        'channel_id': channel_1,
        'u_id': user_2['auth_user_id']
    })
    requests.post(config.url + 'channel/invite/v2', json={
        'token': user_1['token'],
        'channel_id': channel_1,
        'u_id': user_2['auth_user_id']
    })
    channel_details_json = requests.get(config.url + 'channel/details/v2', json={
        'token': user_1['token'],
        'channel_id': channel_1
    })
    channel_details = channel_details_json.json()

    assert len(channel_details['owner_members']) == 1
    assert len(channel_details['all_members']) == 2
    assert channel_details['all_members'][0]['u_id'] == 1
    assert channel_details['all_members'][1]['u_id'] == 2

def test_invite_valid_inputs(clear_database, user_1, user_2, channel_1):

    requests.post(config.url + 'channel/invite/v2', json={
        'token': user_1['token'],
        'channel_id': channel_1,
        'u_id': user_2['auth_user_id']
    })
    channel_details_json = requests.get(config.url + 'channel/details/v2', json={
        'token': user_1['token'],
        'channel_id': channel_1
    })
    channel_details = channel_details_json.json()

    assert len(channel_details['owner_members']) == 1
    assert len(channel_details['all_members']) == 2
    assert channel_details['all_members'][0]['u_id'] == 1
    assert channel_details['all_members'][1]['u_id'] == 2

def test_invite_global_owner_allowed(clear_database, user_1, user_2, user_3, channel_2):

    requests.post(config.url + 'channel/invite/v2', json={
        'token': user_1['token'],
        'channel_id': channel_2,
        'u_id': user_3['auth_user_id']
    })
    channel_details_json = requests.get(config.url + 'channel/details/v2', json={
        'token': user_2['token'],
        'channel_id': channel_2
    })
    channel_details = channel_details_json.json()

    assert len(channel_details['owner_members']) == 1
    assert len(channel_details['all_members']) == 2
    assert channel_details['all_members'][0]['u_id'] == 2
    assert channel_details['all_members'][1]['u_id'] == 3

def test_invite_global_owner_invited(clear_database, user_1, user_2, channel_2):
    requests.post(config.url + 'channel/invite/v2', json={
        'token': user_2['token'],
        'channel_id': channel_2,
        'u_id': user_1['auth_user_id']
    })
    channel_details_json = requests.get(config.url + 'channel/details/v2', json={
        'token': user_2['token'],
        'channel_id': channel_2
    })
    channel_details = channel_details_json.json()

    assert len(channel_details['owner_members']) == 2
    assert channel_details['owner_members'][0]['u_id'] == 2
    assert channel_details['owner_members'][1]['u_id'] == 1
    assert len(channel_details['all_members']) == 2
    assert channel_details['all_members'][0]['u_id'] == 2
    assert channel_details['all_members'][1]['u_id'] == 1

################################################################################
# channel_details http tests                                                   #
################################################################################

def expected_output_details_1():
    return {
        'name': "Channel1",
        'is_public': True,
        'owner_members': [
            {
                'u_id': 1,
                'name_first': 'John',
                'name_last': 'Smith',
                'email': 'johnsmith@gmail.com',
                'handle_str': 'johnsmith',
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'name_first': 'John',
                'name_last': 'Smith',
                'email': 'johnsmith@gmail.com',
                'handle_str': 'johnsmith',
            },
            {
                'u_id': 2,
                'name_first': 'Philip',
                'name_last': 'Tran',
                'email': 'philtran@gmail.com',
                'handle_str': 'philtran',
            }
        ]
    }

def expected_output_details_2():
    return {
        'name': "Phil's Channel",
        'is_public': True,
        'owner_members': [
            {
                'u_id': 2,
                'name_first': 'Philip',
                'name_last': 'Tran',
                'email': 'philtran@gmail.com',
                'handle_str': 'philtran',
            }
        ],
        'all_members': [
            {
                'u_id': 2,
                'name_first': 'Philip',
                'name_last': 'Tran',
                'email': 'philtran@gmail.com',
                'handle_str': 'philtran',
            }
        ]
    }

def test_channel_details_invalid_token(clear_database, user_1, channel_1):
    
    channel_details_json = requests.get(config.url + 'channel/details/v2', json={
        'token': INVALID_TOKEN,
        'channel_id': channel_1
    })

    assert channel_details_json.status_code == ACCESSERROR

def test_channel_details_invalid_channel(clear_database, user_1, channel_1):
    
    channel_details_json = requests.get(config.url + 'channel/details/v2', json={
        'token': user_1['token'],
        'channel_id': INVALID_CHANNEL_ID
    })

    assert channel_details_json.status_code == INPUTERROR

def test_channel_details_invalid_auth_id(clear_database, user_1, user_2, channel_1):
    
    channel_details_json = requests.get(config.url + 'channel/details/v2', json={
        'token': user_2['token'],
        'channel_id': channel_1
    })

    assert channel_details_json.status_code == ACCESSERROR

def test_channel_details_owner_allowed(clear_database, user_1, user_2, channel_1):
    requests.post(config.url + 'channel/invite/v2', json={
        'token': user_1['token'],
        'channel_id': channel_1,
        'u_id': user_2['auth_user_id']
    })
    channel_details_json = requests.get(config.url + 'channel/details/v2', json={
        'token': user_1['token'],
        'channel_id': channel_1
    })
    channel_details = channel_details_json.json()

    assert channel_details == expected_output_details_1()

def test_channel_details_member_allowed(clear_database, user_1, user_2, channel_1):
    requests.post(config.url + 'channel/invite/v2', json={
        'token': user_1['token'],
        'channel_id': channel_1,
        'u_id': user_2['auth_user_id']
    })
    channel_details_json = requests.get(config.url + 'channel/details/v2', json={
        'token': user_2['token'],
        'channel_id': channel_1
    })
    channel_details = channel_details_json.json()

    assert channel_details == expected_output_details_1()

def test_channel_details_global_owner_allowed(clear_database, user_1, user_2, channel_2):
    channel_details_json = requests.get(config.url + 'channel/details/v2', json={
        'token': user_1['token'],
        'channel_id': channel_2
    })
    channel_details = channel_details_json.json()

    assert channel_details == expected_output_details_1()

def test_channel_details_new_channel(clear_database, user_1, user_2, channel_2):
    channel_details_json = requests.get(config.url + 'channel/details/v2', json={
        'token': user_2['token'],
        'channel_id': channel_2
    })
    channel_details = channel_details_json.json()

    assert channel_details == expected_output_details_1()

def test_channel_details_empty_channel(clear_database, user_1, user_2, channel_2):
    requests.post(config.url + 'channel/leave/v1', json={
        'token': user_2['token'],
        'channel_id': channel_2
    })
    channel_details_json = requests.get(config.url + 'channel/details/v2', json={
        'token': user_1['token'],
        'channel_id': channel_2
    })
    channel_details = channel_details_json.json()

    assert channel_details['name'] == "Phil's Channel"
    assert channel_details['is_public'] == True
    assert channel_details['owner_members'] == []
    assert channel_details['all_members'] == []

################################################################################
# channel_addowner http tests                                                  #
################################################################################

def test_channel_addowner_invalid_token(clear_database, user_1, user_2, channel_1):
    requests.post(config.url + 'channel/invite/v2', json={
        'token': user_1['token'],
        'channel_id': channel_1,
        'u_id': user_2['auth_user_id']
    })
    addowner = requests.post(config.url + 'channel/addowner/v1', json={
        'token': INVALID_TOKEN,
        'channel_id': channel_1,
        'u_id': user_2['auth_user_id']
    })

    assert addowner.status_code == ACCESSERROR

def test_channel_addowner_invalid_channel(clear_database, user_1, user_2, channel_1):
    requests.post(config.url + 'channel/invite/v2', json={
        'token': user_1['token'],
        'channel_id': channel_1,
        'u_id': user_2['auth_user_id']
    })
    addowner = requests.post(config.url + 'channel/addowner/v1', json={
        'token': user_1['token'],
        'channel_id': INVALID_CHANNEL_ID,
        'u_id': user_2['auth_user_id']
    })

    assert addowner.status_code == INPUTERROR

def test_channel_addowner_invalid_auth_id(clear_database, user_1, user_2, channel_1):
    requests.post(config.url + 'channel/invite/v2', json={
        'token': user_1['token'],
        'channel_id': channel_1,
        'u_id': user_2['auth_user_id']
    })
    addowner = requests.post(config.url + 'channel/addowner/v1', json={
        'token': user_2['token'],
        'channel_id': INVALID_CHANNEL_ID,
        'u_id': user_2['auth_user_id']
    })

    assert addowner.status_code == ACCESSERROR

def test_channel_addowner_invalid_uid(clear_database, user_1, user_2, channel_1):
    requests.post(config.url + 'channel/invite/v2', json={
        'token': user_1['token'],
        'channel_id': channel_1,
        'u_id': user_2['auth_user_id']
    })
    addowner = requests.post(config.url + 'channel/addowner/v1', json={
        'token': user_1['token'],
        'channel_id': channel_1,
        'u_id': INVALID_UID
    })

    assert addowner.status_code == ACCESSERROR

def test_channel_addowner_already_owner(clear_database, user_1, channel_1):
    requests.post(config.url + 'channel/invite/v2', json={
        'token': user_1['token'],
        'channel_id': channel_1,
        'u_id': user_2['auth_user_id']
    })
    addowner = requests.post(config.url + 'channel/addowner/v1', json={
        'token': user_1['token'],
        'channel_id': channel_1,
        'u_id': user_1['auth_user_id']
    })

    assert addowner.status_code == INPUTERROR

def test_channel_addowner_auth_user_not_owner(clear_database, user_1, user_2, channel_1):
    requests.post(config.url + 'channel/invite/v2', json={
        'token': user_1['token'],
        'channel_id': channel_1,
        'u_id': user_2['auth_user_id']
    })
    addowner = requests.post(config.url + 'channel/addowner/v1', json={
        'token': user_2['token'],
        'channel_id': channel_1,
        'u_id': user_2['auth_user_id']
    })

    assert addowner.status_code == ACCESSERROR

def test_channel_addowner_global_owner_allowed(clear_database, user_1, user_2, channel_2):
    requests.post(config.url + 'channel/invite/v2', json={
        'token': user_2['token'],
        'channel_id': channel_2,
        'u_id': user_1['auth_user_id']
    })
    requests.post(config.url + 'channel/addowner/v1', json={
        'token': user_1['token'],
        'channel_id': channel_1,
        'u_id': user_1['auth_user_id']
    })
    channel_details_json = requests.get(config.url + 'channel/details/v2', json={
        'token': user_2['token'],
        'channel_id': channel_2
    })
    channel_details = channel_details_json.json()

    assert channel_details['name'] == "Phil's Channel"
    assert channel_details['is_public'] == True
    assert len(channel_details['owner_members']) == 2
    assert channel_details['owner_members'][0]['u_id'] == 2
    assert channel_details['owner_members'][1]['u_id'] == 1
    assert len(channel_details['all_members']) == 2
    assert channel_details['all_members'][0]['u_id'] == 2
    assert channel_details['all_members'][1]['u_id'] == 1

def test_channel_addowner_valid_inputs(clear_database, user_1, user_2, channel_1, make_user_2_owner_in_channel_1):
    channel_details_json = requests.get(config.url + 'channel/details/v2', json={
        'token': user_1['token'],
        'channel_id': channel_1
    })
    channel_details = channel_details_json.json()

    assert channel_details['name'] == "Channel1"
    assert channel_details['is_public'] == True
    assert len(channel_details['owner_members']) == 2
    assert channel_details['owner_members'][0]['u_id'] == 1
    assert channel_details['owner_members'][1]['u_id'] == 2
    assert len(channel_details['all_members']) == 2
    assert channel_details['all_members'][0]['u_id'] == 1
    assert channel_details['all_members'][1]['u_id'] == 2

################################################################################
# channel_removeowner http tests                                               #
################################################################################

def test_channel_removeowner_invalid_token(clear_database, user_1, user_2, channel_1, make_user_2_owner_in_channel_1):
    removeowner = requests.post(config.url + 'channel/removeowner/v1', json={
        'token': INVALID_TOKEN,
        'channel_id': channel_1,
        'u_id': user_2['auth_user_id']
    })

    assert removeowner.status_code == ACCESSERROR

def test_channel_removeowner_invalid_channel(clear_database, user_1, user_2, channel_1, make_user_2_owner_in_channel_1):
    removeowner = requests.post(config.url + 'channel/removeowner/v1', json={
        'token': user_1['token'],
        'channel_id': INVALID_CHANNEL_ID,
        'u_id': user_2['auth_user_id']
    })

    assert removeowner.status_code == INPUTERROR

def test_channel_removeowner_invalid_auth_id(clear_database, user_1, user_2, channel_1):
    requests.post(config.url + 'channel/invite/v2', json={
        'token': user_1['token'],
        'channel_id': channel_1,
        'u_id': user_2['auth_user_id']
    })
    removeowner = requests.post(config.url + 'channel/removeowner/v1', json={
        'token': user_2['token'],
        'channel_id': INVALID_CHANNEL_ID,
        'u_id': user_1['auth_user_id']
    })

    assert removeowner.status_code == ACCESSERROR

def test_channel_removeowner_invalid_uid(clear_database, user_1, user_2, channel_1):
    requests.post(config.url + 'channel/invite/v2', json={
        'token': user_1['token'],
        'channel_id': channel_1,
        'u_id': user_2['auth_user_id']
    })
    removeowner = requests.post(config.url + 'channel/removeowner/v1', json={
        'token': user_1['token'],
        'channel_id': channel_1,
        'u_id': INVALID_UID
    })

    assert removeowner.status_code == ACCESSERROR

def test_channel_removeowner_auth_id_not_owner(clear_database, user_1, user_2, channel_1):
    requests.post(config.url + 'channel/invite/v2', json={
        'token': user_1['token'],
        'channel_id': channel_1,
        'u_id': user_2['auth_user_id']
    })
    removeowner = requests.post(config.url + 'channel/removeowner/v1', json={
        'token': user_2['token'],
        'channel_id': channel_1,
        'u_id': user_1['auth_user_id']
    })

    assert removeowner.status_code == INPUTERROR

def test_channel_removeowner_u_id_not_owner(clear_database, user_1, user_2, channel_1):
    requests.post(config.url + 'channel/invite/v2', json={
        'token': user_1['token'],
        'channel_id': channel_1,
        'u_id': user_2['auth_user_id']
    })
    removeowner = requests.post(config.url + 'channel/removeowner/v1', json={
        'token': user_1['token'],
        'channel_id': channel_1,
        'u_id': user_2['auth_user_id']
    })

    assert removeowner.status_code == INPUTERROR

def test_channel_removeowner_only_owner_in_channel(clear_database, user_1, channel_1):
    removeowner = requests.post(config.url + 'channel/removeowner/v1', json={
        'token': user_1['token'],
        'channel_id': channel_1,
        'u_id': user_1['auth_user_id']
    })

    assert removeowner.status_code == INPUTERROR

def test_channel_removeowner_valid_inputs(clear_database, user_1, user_2, channel_1, make_user_2_owner_in_channel_1):
    requests.post(config.url + 'channel/removeowner/v1', json={
        'token': user_1['token'],
        'channel_id': channel_1,
        'u_id': user_2['auth_user_id']
    })
    channel_details_json = requests.get(config.url + 'channel/details/v2', json={
        'token': user_1['token'],
        'channel_id': channel_1
    })
    channel_details = channel_details_json.json()

    assert len(channel_details['owner_members']) == 1
    assert channel_details['owner_members'][0]['u_id'] == 1
    assert len(channel_details['all_members']) == 2
    assert channel_details['all_members'][0]['u_id'] == 2
    assert channel_details['all_members'][1]['u_id'] == 1

def test_channel_removeowner_global_owner_allowed(clear_database, user_1, user_2, user_3,channel_2):
    requests.post(config.url + 'channel/invite/v2', json={
        'token': user_2['token'],
        'channel_id': channel_2,
        'u_id': user_3['auth_user_id']
    })
    requests.post(config.url + 'channel/addowner/v1', json={
        'token': user_2['token'],
        'channel_id': channel_2,
        'u_id': user_3['auth_user_id']
    })
    requests.post(config.url + 'channel/removeowner/v1', json={
        'token': user_1['token'],
        'channel_id': channel_2,
        'u_id': user_3['auth_user_id']
    })
    channel_details_json = requests.get(config.url + 'channel/details/v2', json={
        'token': user_2['token'],
        'channel_id': channel_2
    })
    channel_details = channel_details_json.json()

    assert len(channel_details['owner_members']) == 1
    assert channel_details['owner_members'][0]['u_id'] == 2
    assert len(channel_details['all_members']) == 2
    assert channel_details['all_members'][0]['u_id'] == 2
    assert channel_details['all_members'][1]['u_id'] == 3


################################################################################
# channel_leave http tests                                                     #
################################################################################

def test_channel_leave_invalid_token(clear_database, user_1, channel_1):
    leave = requests.post(config.url + 'channel/leave/v1', json={
        'token': INVALID_TOKEN,
        'channel_id': channel_1,
    })
    
    assert leave.status_code == ACCESSERROR

def test_channel_leave_invalid_channel(clear_database, user_1, channel_1):
    leave = requests.post(config.url + 'channel/leave/v1', json={
        'token': user_1['token'],
        'channel_id': INVALID_CHANNEL_ID,
    })
    
    assert leave.status_code == INPUTERROR

def test_channel_leave_invalid_auth_id(clear_database, user_1, user_2, channel_1):
    leave = requests.post(config.url + 'channel/leave/v1', json={
        'token': user_2['token'],
        'channel_id': channel_1,
    })
    
    assert leave.status_code == ACCESSERROR

def test_channel_leave_member(clear_database, user_1, user_2, channel_1):
    requests.post(config.url + 'channel/invite/v2', json={
        'token': user_1['token'],
        'channel_id': channel_1,
        'u_id': user_2['auth_user_id']
    })
    requests.post(config.url + 'channel/leave/v1', json={
        'token': user_2['token'],
        'channel_id': channel_1,
    })
    channel_details_json = requests.get(config.url + 'channel/details/v2', json={
        'token': user_1['token'],
        'channel_id': channel_1
    })
    channel_details = channel_details_json.json()

    assert channel_details['name'] == "Channel1"
    assert channel_details['is_public'] == True
    assert len(channel_details['owner_members']) == 1
    assert channel_details['owner_members'][0]['u_id'] == 1
    assert len(channel_details['all_members']) == 1
    assert channel_details['all_members'][0]['u_id'] == 1

def test_channel_leave_owner(clear_database, user_1, user_2, channel_1, make_user_2_owner_in_channel_1):
    requests.post(config.url + 'channel/leave/v1', json={
        'token': user_2['token'],
        'channel_id': channel_1,
    })
    channel_details_json = requests.get(config.url + 'channel/details/v2', json={
        'token': user_1['token'],
        'channel_id': channel_1
    })
    channel_details = channel_details_json.json()

    assert channel_details['name'] == "Channel1"
    assert channel_details['is_public'] == True
    assert len(channel_details['owner_members']) == 1
    assert channel_details['owner_members'][0]['u_id'] == 1
    assert len(channel_details['all_members']) == 1
    assert channel_details['all_members'][0]['u_id'] == 1

def test_channel_leave_last_user(clear_database, user_1, channel_1):
    requests.post(config.url + 'channel/leave/v1', json={
        'token': user_1['token'],
        'channel_id': channel_1,
    })
    channel_details_json = requests.get(config.url + 'channel/details/v2', json={
        'token': user_1['token'],
        'channel_id': channel_1
    })
    channel_details = channel_details_json.json()

    assert channel_details['name'] == "Channel1"
    assert channel_details['is_public'] == True
    assert channel_details['owner_members'] = []
    assert channel_details['all_members'] == []

    
    