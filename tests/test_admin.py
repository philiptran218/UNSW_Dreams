import pytest
from src.other import clear_v1
from src.auth import auth_register_v2
from src.user import user_profile_v1
from src.channel import channel_join_v2, channel_details_v2
from src.channels import channels_create_v2
from src.admin import admin_user_remove_v1, admin_userpermission_change_v1
from src.error import AccessError, InputError

INVALID_TOKEN = -1
INVALID_U_ID = -1
INVALID_PERMISSION_ID = -1
OWNER = 1
MEMBER = 2

# Fixture that clears and resets all the internal data of the application
@pytest.fixture
def clear_data():
    clear_v1()

#Fixtures that create specific tokens and user_id's, needed to test the functions. 
@pytest.fixture
def test_user1_token():
    user_info = auth_register_v2("validemail@g.com", "validpass", "validname","validname")
    return user_info["token"]

@pytest.fixture
def test_user1_u_id():
    user_info = auth_register_v2("validemail@g.com", "validpass", "validname","validname")
    return user_info["u_id"]

@pytest.fixture
def test_user2_token():
    user_info = auth_register_v2("dan@gmail.com", "password", "dan", "Smith")
    return user_info['token']

@pytest.fixture
def test_user2_u_id():
    user_info = auth_register_v2("dan@gmail.com", "password", "dan", "Smith")
    return user_info['user_id']

#Fixture that creates new private channel. This will be needed for testing userpermissions_change
@pytest.fixture
def test_channel(test_user1_token):
    test_channel = channels_create_v2(test_user1_token, "test_channel", False)
    return test_channel

# Expected output for the admin_user_remove function.
@pytest.fixture
def expected_output_admin_user_remove():
    return {
        [
            {
                'u_id': 2,
                'email': 'dan@gmail.com',
                'name_first': 'Removed',
                'name_last': 'user', 
                'handle_str': "danSmith",
            },
        ]
    }

################################################################################
#  admin_user_remove_v1 testing                                                #
################################################################################

def test_admin_user_remove_v1_valid(clear_data, test_user1_token, test_user2_u_id):
    admin_user_remove_v1(test_user1_token, test_user2_u_id)
    # admin functions have no output. In order to test if the function has worked. Other functions
    # need to be used in the assert. In this case, user_profile_v1 is used.
    assert(user_profile_v1(test_user1_token, test_user2_u_id) == expected_output_admin_user_remove())

def test_admin_user_remove_v1_invalid_u_id(clear_data, test_user1_token):
    with pytest.raises(InputError):
        admin_user_remove_v1(test_user1_token, INVALID_U_ID)

def test_admin_user_remove_v1_invalid_only_owner(clear_data, test_user1_token, test_user1_u_id):
    with pytest.raises(InputError):
        admin_user_remove_v1(test_user1_token, test_user1_u_id)

def test_admin_user_remove_v1_invalid_not_owner(clear_data, test_user2_token, test_user1_u_id):
    with pytest.raises(AccessError):
        admin_user_remove_v1(test_user2_token, test_user1_u_id)

def test_admin_user_remove_v1_invalid_token(clear_data, test_user1_u_id):
    with pytest.raises(AccessError):
        admin_user_remove_v1(INVALID_TOKEN, test_user1_u_id)

################################################################################
#  test_admin_userpermission_change_v1 testing                                 #
################################################################################      

def test_admin_userpermission_change_v1_valid(clear_data, test_user1_token, test_user2_token, test_user2_u_id, test_channel):
    admin_userpermission_change_v1(test_user1_token, test_user2_u_id, OWNER)
    
    # admin functions have no output. In order to test if the function has worked. Other functions
    # need to be used in the assert. In this case, channel_join and channel_details are used, where
    # the test_user can join a private channel as they are now an owner. This should be registered in 
    # channel_details.

    channel_join_v2(test_user2_token, test_channel) 
    channels = channel_details_v2(test_user2_token ,test_channel)
    assert(channels['all_members'][1]['u_id'] == test_user2_u_id)

def test_admin_userpermission_change_v1_invalid_u_id(clear_data, test_user1_token):
    with pytest.raises(InputError):
        admin_userpermission_change_v1(test_user1_token, INVALID_U_ID, OWNER)

def test_admin_userpermission_change_v1_invalid_perm_id(clear_data, test_user1_token, test_user1_u_id):
    with pytest.raises(InputError):
        admin_userpermission_change_v1(test_user1_token, test_user2_u_id, INVALID_PERMISSION_ID)

def test_admin_userpermission_change_v1_invalid_not_owner(clear_data, test_user2_token, test_user1_u_id):
    with pytest.raises(AccessError):
        admin_userpermission_change_v1(test_user1_token, test_user2_u_id, MEMBER)

def test_admin_userpermission_change_v1_invalid_token(clear_data, test_user1_u_id):
    with pytest.raises(AccessError):
        admin_userpermission_change_v1(INVALID_TOKEN, test_user2_u_id, OWNER)