from src.auth import auth_register_v1
from src.error import AccessError, InputError
from src.channels import channels_list_v1, channels_listall_v1,channels_create_v1
from src.other import clear_v1
from src.helper import is_valid_uid
from src.database import data
import pytest

INVALID_USER = -1

################################################################################
# channel_list_v1 and channel_listall_v1 tests                                 #
################################################################################

# Fixture that clears and resets all the internal data of the application
@pytest.fixture
def clear_data():
    clear_v1()

@pytest.fixture
def test_user():
    userid = auth_register_v1("validemail@g.com", "validpass", "validname","validname")
    return userid["auth_user_id"]

@pytest.fixture
def test_user2():
    user = auth_register_v1("johnsmith@gmail.com", "password", "John", "Smith")
    return user['auth_user_id']

@pytest.fixture
def test_channel(test_user):
    channels_create_v1(test_user, "validname's Channel", True)

@pytest.fixture
def test_channel2(test_user2):
    channels_create_v1(test_user2, "John's Channel", True)

def expected_output_list_v1():
    return {
        'channels':
        [
            {
                "channel_id": 1,
                "name":"validname's Channel"
            }
        ]
    }

def expected_output_listall_v1():
    return {
        'channels': [
            {
                "channel_id": 1,
                "name":"validname's Channel"
            },
            {
                "channel_id": 2,
                "name":"John's Channel"
            }
        ]
    }
def test_channels_list_v1_empty(clear_data, test_user):
    assert(channels_list_v1(test_user) == {'channels': []})

def test_channels_listall_v1_empty(clear_data, test_user):
    assert(channels_list_v1(test_user) == {'channels': []})

def test_channels_list_v1_valid(clear_data, test_user, test_channel,test_channel2):
    assert(channels_list_v1(test_user) == expected_output_list_v1())

def test_channels_listall_v1_valid(clear_data, test_user, test_channel,test_channel2):
    assert(channels_listall_v1(test_user) == expected_output_listall_v1())

def test_channels_list_v1_invalid(clear_data):
    with pytest.raises(AccessError):
        channels_list_v1(INVALID_USER)

def test_channels_listall_v1_invalid(clear_data):
    with pytest.raises(AccessError):
        channels_listall_v1(INVALID_USER)

################################################################################
# channel_create_v1 tests                                                      #
################################################################################

# Testing a valid case for channels_create
def test_valid_channels_create_v1_u_id(clear_data,test_user):
    # Valid case where a public channel with name "ValidChannelName" is created 
    # by user with auth_id userId
    assert(channels_create_v1(test_user, "ValidChannelName", True) == {'channel_id': 1})

# Testing if a channel is actaully being added to the list of channels
def test_valid_channels_create_v1(clear_data,test_user):
    # Valid case where a public channel with name "ValidChannelName" is created 
    # by user with auth_id userId
    channels_create_v1(test_user, "ValidChannelName", True)
    assert(bool(data['channels']))

# Testing if more than one channel is being added to the list of channels
def test_valid_channels_create_v1_multiple(clear_data,test_user):
    # Created a second user_id by regestring a valid user
    userId2 = auth_register_v1("validemail2@g.com", "validpass2", "validname2","validname2")
    # Valid case where a public channel with name "ValidChannelName1" is created 
    # by user with auth_id userId1
    channels_create_v1(test_user, "ValidChannelName1", True)
    # Valid case where a public channel with name "ValidChannelName2" is created 
    # by user with auth_id userId2
    channels_create_v1(userId2['auth_user_id'], "ValidChannelName2", True)
    assert(len(data['channels']) > 1)

# Testing an invalid case(channel name is more than 20 characters long) 
def test_invalidName_channels_create_v1(clear_data,test_user):

    # Channel name is more than 20 characters long
    invalidName = "nameismorethantwentycharacters"
    # An input error is raised when a channel name that is more than 20 
    # characters long is passed intot the function 
    with pytest.raises(InputError): 
        channels_create_v1(test_user,invalidName, True)
    


# Testing when a user with an invalid u_id trys to create a channel
def test_invalid_user(clear_data):
    # Invalid case where a public channel with name "ValidChannelName" is created 
    # by user with an Invalid u_id
    with pytest.raises(AccessError): 
        channels_create_v1(INVALID_USER,'channelname',True)
    

