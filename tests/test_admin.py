import pytest
from src.other import clear_v1
from src.auth import auth_register_v1
from src.database import data
from src.user import user_profile_setname_v1, user_profile_v1
from src.message import message_send_v1
from src.channel import channel_join_v1, channel_details_v1, channel_messages_v1, channel_invite_v1
from src.channels import channels_create_v1, channels_listall_v1
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
def test_user1():
    user_info = auth_register_v1("validemail@g.com", "validpass", "validname","validname")
    return user_info

@pytest.fixture
def test_user2():
    user_info = auth_register_v1("dan@gmail.com", "password", "dan", "Smith")
    return user_info

#Fixture that creates new private channel. This will be needed for testing userpermissions_change
@pytest.fixture
def test_channel(test_user1, test_user2):
    test_channel = channels_create_v1(test_user1['token'], "test_channel", False)
    channel_invite_v1(test_user1['token'], test_channel['channel_id'], test_user2['auth_user_id'])
    return test_channel

#Fixture that sends message into the test channel.
@pytest.fixture
def test_message(test_user2, test_channel):
    message_id = message_send_v1(test_user2['token'], test_channel['channel_id'], 'Hello World' )
    return message_id

# Expected output for the admin_user_remove function.
@pytest.fixture
def expected_output_admin_user_remove():
    return { 'user': {
        'u_id': 2,
        'email': 'dan@gmail.com',
        'name_first': 'Removed',
        'name_last': 'User', 
        'handle_str': "dansmith",
    }
    }

################################################################################
#  admin_user_remove_v1 testing                                                #
################################################################################

def test_admin_user_remove_v1_valid(clear_data, test_user1, test_user2, test_message, test_channel, expected_output_admin_user_remove):
    admin_user_remove_v1(test_user1['token'], test_user2['auth_user_id'])
    # admin functions have no output. In order to test if the function has worked. Other functions
    # need to be used in the assert. In this case, user_profile_v1 and channel_messages_v2 is used

    assert(user_profile_v1(test_user1['token'], test_user2['auth_user_id']) == expected_output_admin_user_remove)
    messages = channel_messages_v1(test_user1["token"], test_channel['channel_id'], 0)
    assert(messages['messages'][0]['message'] == 'Removed User')

def test_admin_user_remove_v1_invalid_u_id1(clear_data, test_user1):
    with pytest.raises(InputError):
        admin_user_remove_v1(test_user1['token'], INVALID_U_ID)

def test_admin_user_remove_v1_invalid_u_id2(clear_data, test_user1):
    with pytest.raises(InputError):
        admin_user_remove_v1(test_user1['token'], 100)

def test_admin_user_remove_v1_invalid_only_owner(clear_data, test_user1):
    with pytest.raises(InputError):
        admin_user_remove_v1(test_user1['token'], test_user1['auth_user_id'])

def test_admin_user_remove_v1_invalid_not_owner(clear_data, test_user1, test_user2):
    with pytest.raises(AccessError):
        admin_user_remove_v1(test_user2['token'], test_user1['auth_user_id'])

def test_admin_user_remove_v1_invalid_token(clear_data, test_user1):
    with pytest.raises(AccessError):
        admin_user_remove_v1(INVALID_TOKEN, test_user1['auth_user_id'])

################################################################################
#  test_admin_userpermission_change_v1 testing                                 #
################################################################################      

def test_admin_userpermission_change_v1_valid(clear_data, test_user1, test_user2, test_channel):
    admin_userpermission_change_v1(test_user1['token'], test_user2['auth_user_id'], OWNER)
    
    # admin functions have no output. In order to test if the function has worked. Other functions
    # need to be used in the assert. In this case, channel_join and channel_details are used, where
    # the test_user can join a private channel as they are now an owner. This should be registered in 
    # channel_details.

    channel_join_v1(test_user2['token'], test_channel['channel_id']) 
    channels = channel_details_v1(test_user2['token'] ,test_channel['channel_id'])
    assert(channels['all_members'][1]['u_id'] == test_user2['auth_user_id'])

def test_admin_userpermission_change_v1_invalid_u_id(clear_data, test_user1):
    with pytest.raises(InputError):
        admin_userpermission_change_v1(test_user1['token'], INVALID_U_ID, OWNER)

def test_admin_userpermission_change_v1_invalid_perm_id(clear_data, test_user1, test_user2):
    with pytest.raises(InputError):
        admin_userpermission_change_v1(test_user1['token'], test_user2['auth_user_id'], INVALID_PERMISSION_ID)

def test_admin_userpermission_change_v1_invalid_not_owner(clear_data, test_user1, test_user2):
    with pytest.raises(AccessError):
        admin_userpermission_change_v1(test_user2['token'], test_user1['auth_user_id'], OWNER)

def test_admin_userpermission_change_v1_invalid_token(clear_data, test_user1):
    with pytest.raises(AccessError):
        admin_userpermission_change_v1(INVALID_TOKEN, test_user1['auth_user_id'], OWNER)