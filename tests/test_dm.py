import pytest
from src.other import clear_v1
from src.auth import auth_register_v1
from src.dm import dm_remove_v1 , dm_create_v1, dm_list_v1, dm_messages_v1, dm_invite_v1, dm_details_v1
from src.error import AccessError, InputError 
from src.message import message_senddm_v1
INVALID_DM_ID = -1
INVALID_TOKEN = -1
INVALID_U_ID = -1

# Fixture that clears and resets all the internal data of the application
@pytest.fixture
def clear_data():
    clear_v1()

@pytest.fixture
def test_user1_token():
    user_info = auth_register_v1("validemail@g.com", "validpass", "validname","validname")
    return user_info["token"]


@pytest.fixture
def test_user2_u_id():
    user_info = auth_register_v1("dan@gmail.com", "password", "dan", "Smith")
    return user_info['auth_user_id']

@pytest.fixture
def test_user3_token():
    user_info = auth_register_v1("danimatt@gmail.com", "valpassword", "danny", "Smithy")
    return user_info['token']

@pytest.fixture
def test_user4_u_id():
    user_info = auth_register_v1("danny@gmail.com", "password123", "danny", "james")
    return user_info['auth_user_id']

@pytest.fixture
def test_create_dm(test_user1_token,test_user2_u_id):
    dm = dm_create_v1((test_user1_token,test_user2_u_id))
    return dm['dm_id']

################################################################################
# dm_invite_v1 tests                                                     #
################################################################################

#testing when dm_id is invalid -> Input Error is raised
def test_dm_invite_invalid_dm_id(clear_data,test_user1_token,test_user2_u_id,test_create_dm):
    with pytest.raises(InputError):
        dm_invite_v1(test_user1_token,INVALID_DM_ID,test_user2_u_id)
#testing when u_id is invalid -> Input Error is raised
def test_dm_invite_invalid_u_id(clear_data,test_user1_token,test_user2_u_id,test_create_dm):
    with pytest.raises(InputError):
        dm_invite_v1(test_user1_token,test_create_dm,INVALID_U_ID)
#testing when user who is calling the fucntion is not part of the dm
def test_dm_invite_user_not_a_member(clear_data,test_user1_token,test_user2_u_id,test_user3_token,test_create_dm):
    with pytest.raises(AccessError):
        dm_invite_v1(test_user3_token,test_create_dm,test_user2_u_id)

#testing a valid case by inviting a user and checking for membership
def test_dm_invite_valid(clear_data,test_user1_token,test_user2_u_id,test_user4_u_id,test_create_dm):
    dm_invite_v1(test_user1_token,test_create_dm,test_user4_u_id)
    member_check = False
    dm_details = dm_details_v1(test_user1_token,test_create_dm)
    members_list = dm_details['members']
    for member in members_list:
        if member['u_id'] == test_user4_u_id:
            member_check = True
    assert(member_check)

