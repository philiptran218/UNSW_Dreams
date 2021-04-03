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
def test_create_dm(test_user1,test_user2):
    dm = requests.post(config.url + 'dm/create/v1', json={
        'token': test_user1['token'],
        'u_ids': [test_user2['auth_user_id']]
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
                'name_last': 'smith',
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
=======
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
        'dm_id': test_create_dm['dm_id'],
        'u_id': INVALID_U_ID
    })
    assert dm_inv.status_code == INPUTERROR

def test_dm_invite_user_not_a_member(clear_data,test_user1,test_user2,test_user3,test_create_dm):
    dm_inv = requests.post(config.url + 'dm/invite/v1', json={
        'token': test_user3['token'],
        'dm_id': test_create_dm['dm_id'],
        'u_id': test_user2['auth_user_id']
    })
    assert dm_inv.status_code == ACCESSERROR

def test_dm_invite_invalid_token(clear_data,test_user1,test_user2,test_create_dm):
    dm_inv = requests.post(config.url + 'dm/invite/v1', json={
        'token': INVALID_TOKEN,
        'dm_id': test_create_dm['dm_id'],
        'u_id': test_user2['auth_user_id']
    })
    assert dm_inv.status_code == ACCESSERROR   

def test_dm_invite_already_in_dm(clear_data,test_user1,test_user2,test_create_dm):
    dm_inv = requests.post(config.url + 'dm/invite/v1', json={
        'token': test_user1['token'],
        'dm_id': test_create_dm['dm_id'],
        'u_id': test_user2['auth_user_id']
    })
    assert dm_inv.json()== {} 

def test_dm_invite_valid(clear_data,test_user1,test_user2,test_user4,test_create_dm):
    requests.post(config.url + 'dm/invite/v1', json={
        'token': test_user1['token'],
        'dm_id': test_create_dm['dm_id'],
        'u_id': test_user4['auth_user_id']
    })
    
    member_check = False
    dm_deets = requests.get(config.url + 'dm/details/v1', json={
        'token': test_user1['token'],
        'dm_id': test_create_dm['dm_id']
    }) 
    members_list = dm_deets.json()['members']
    for member in members_list:
        if member['u_id'] == test_user4['auth_user_id']:
            member_check = True
    assert(member_check)


################################################################################
# dm_leave_v1 tests                                                            #
################################################################################

def test_dm_leave_invalid_dm_id(clear_data,test_user1,test_user2,test_create_dm):
    leave = requests.post(config.url + 'dm/leave/v1', json={
        'token': test_user1['token'],
        'dm_id':INVALID_DM_ID
    })
    assert leave.status_code == INPUTERROR 

def test_dm_leave_user_not_a_member(clear_data,test_user1,test_user2,test_user3,test_create_dm):
    leave = requests.post(config.url + 'dm/leave/v1', json={
        'token': test_user3['token'],
        'dm_id':test_create_dm['dm_id']
    })
    assert leave.status_code == ACCESSERROR

def test_dm_leave(clear_data,test_user1,test_user2,test_create_dm):
    requests.post(config.url + 'dm/leave/v1', json={
        'token': test_user2['token'],
        'dm_id':test_create_dm['dm_id']
    })
    member_left = True
    dlist = requests.get(config.url + 'dm/details/v1', json={
        'token': test_user1['token'],
        'dm_id': test_create_dm['dm_id']
    }) 
    members = dlist.json()['members']
    for member in members:
        if member['u_id'] == test_user2['auth_user_id']:
            member_left = False
    assert(member_left)

def test_dm_leave_invalid_token(clear_data,test_user1,test_user2,test_create_dm):
    leave = requests.post(config.url + 'dm/leave/v1', json={
        'token': INVALID_TOKEN,
        'dm_id':test_create_dm['dm_id']
    })
    assert leave.status_code == ACCESSERROR   


################################################################################
# dm_messages_v1 tests                                                         #
################################################################################

def test_dm_messages_invalid_dm_id(clear_data,test_create_dm,test_user1,test_user2):
    msg = requests.get(config.url + 'dm/messages/v1', json={
        'token': test_user1['token'],
        'dm_id': INVALID_DM_ID,
        'start': 0
    })
    assert msg.status_code == INPUTERROR

def test_dm_messages_invalid_token(clear_data,test_create_dm,test_user1,test_user2):
    msg = requests.get(config.url + 'dm/messages/v1', json={
        'token': INVALID_TOKEN,
        'dm_id': test_create_dm['dm_id'],
        'start': 0
    })
    assert msg.status_code == ACCESSERROR

def test_dm_messages_invalid_start(clear_data,test_create_dm,test_user1,test_user2):
    msg = requests.get(config.url + 'dm/messages/v1', json={
        'token': test_user1['token'],
        'dm_id': test_create_dm['dm_id'],
        'start': 20
    })
    assert msg.status_code == INPUTERROR

def test_dm_messages_user_not_member(clear_data,test_create_dm,test_user1,test_user2,test_user3):
    msg = requests.get(config.url + 'dm/messages/v1', json={
        'token': test_user3['token'],
        'dm_id': test_create_dm['dm_id'],
        'start': 0
    })
    assert msg.status_code == ACCESSERROR    

def test_dm_messages_start_equal(clear_data,test_create_dm,test_user1,test_user2):
    msg = requests.get(config.url + 'dm/messages/v1', json={
        'token': test_user1['token'],
        'dm_id': test_create_dm['dm_id'],
        'start': 0
    })
    dms = msg.json()
    assert(dms == {'messages': [], 'start': 0, 'end': -1})

def test_dm_messages_valid_single(clear_data,test_create_dm,test_user1,test_user2):
    requests.post(config.url + 'message/senddm/v1', json={
        'token': test_user1['token'],
        'dm_id': test_create_dm['dm_id'],
        'message': 'singlemessage'
    })

    msg = requests.get(config.url + 'dm/messages/v1', json={
        'token': test_user1['token'],
        'dm_id': test_create_dm['dm_id'],
        'start': 0
    })

    message_detail = msg.json()
    print(message_detail)
    assert message_detail['messages'][0]['message_id'] == 1
    assert message_detail['messages'][0]['u_id'] == test_user1['auth_user_id']
    assert message_detail['messages'][0]['message'] == 'singlemessage'
    assert message_detail['start'] == 0
    assert message_detail['end'] == -1

def test_dm_messages_multiple(clear_data,test_create_dm,test_user1,test_user2):
    i = 1
    while i <= 55:
        requests.post(config.url + 'message/senddm/v1',json={
            'token':test_user1['token'],
            'dm_id':test_create_dm['dm_id'],
            'message':f"{i}"
        })
        i += 1
    msg = requests.get(config.url + 'dm/messages/v1', json={
        'token': test_user1['token'],
        'dm_id': test_create_dm['dm_id'],
        'start': 2
    })

    message_detail = msg.json()

    i = 53
    j = 0
    while i >= 4:
        assert message_detail['messages'][j]['message_id'] == i
        assert message_detail['messages'][j]['u_id'] == test_user1['auth_user_id']
        assert message_detail['messages'][j]['message'] == str(i)
        i -= 1
        j += 1 
    assert message_detail['start'] == 2
    assert message_detail['end'] == 52



################################################################################
# dm_remove_v1 tests                                                           #
################################################################################

def test_dm_remove_v1(clear_data,test_user1,test_user2,test_create_dm):
    dmsdict = requests.get(config.url + 'dm/list/v1', json={
        'token': test_user1['token']
    })
    dmsdict = dmsdict.json()

    requests.delete(config.url +'dm/remove/v1', json={
        'token': test_user1['token'],
        'dm_id': test_create_dm['dm_id']
    })

    assert( bool (dmsdict['dm']))

def test_dm_remove_v1_invalid_dm(clear_data,test_user1,test_create_dm):
    removed_dm = requests.delete(config.url +'dm/remove/v1', json={
        'token': test_user1['token'],
        'dm_id': INVALID_DM_ID
    })
    assert removed_dm.status_code == INPUTERROR

def test_dm_remove_v1_invalid_token(clear_data,test_user1,test_create_dm):
    removed_dm = requests.delete(config.url +'dm/remove/v1', json={
        'token': INVALID_TOKEN,
        'dm_id': test_create_dm['dm_id']
    })
    assert removed_dm.status_code == ACCESSERROR


def test_dm_remove_v1_unoriginal(clear_data,test_user1,test_user2,test_user3,test_create_dm):
    removed_dm = requests.delete(config.url +'dm/remove/v1', json={
        'token': test_user3['token'],
        'dm_id': test_create_dm['dm_id']
    })
    assert removed_dm.status_code == ACCESSERROR    

def test_dm_remove_v1_inval_dm_id_not_creator(clear_data,test_user1,test_user2,test_user3,test_create_dm):
    removed_dm = requests.delete(config.url +'dm/remove/v1', json={
        'token': test_user3['token'],
        'dm_id': INVALID_DM_ID
    })
    assert removed_dm.status_code == INPUTERROR   
