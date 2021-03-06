from src.auth import auth_register_v1
from src.error import AccessError, InputError
from src.channels import channels_list_v1, channels_listall_v1,channels_create_v1
from src.other import clear_v1
from src.helper import is_valid_uid
from src.database import data
import pytest

#DEFINE INVALID_USER 130

#a fixture that clears and resets all the internal data of the application
@pytest.fixture
def clear_data():
    clear_v1()

@pytest.fixture
def test_user():
    userid = auth_register_v1("validemail@g.com", "validpass", "validname","validname")
    return userid["auth_user_id"]

def test_channels_list_v1_valid(clear_data, test_user):
    assert(channels_list_v1(test_user)["channels"] == data["channels"])

def test_channels_listall_v1_valid(clear_data, test_user):
    assert(channels_listall_v1(test_user)["channels"] == data["channels"])

def test_channels_list_v1_invalid(clear_data):
    with pytest.raises(AccessError):
        channels_list_v1(130)

def test_channels_listall_v1_invalid(clear_data):
    with pytest.raises(AccessError):
        channels_listall_v1(130)



#testing a valid case for channels_create
def test_valid_channels_create_v1_u_id(clear_data,test_user):
    #Valid case where a public channel with name "ValidChannelName" is created by user with auth_id userId
    assert(channels_create_v1(test_user, "ValidChannelName", True) == {'channel_id': 1})


#testing if a channel is actaully being added to the list of channels
def test_valid_channels_create_v1(clear_data,test_user):
    #Valid case where a public channel with name "ValidChannelName" is created by user with auth_id userId
    channels_create_v1(test_user, "ValidChannelName", True)
    assert(bool(data['channels']))

#testing if more than one channel is being added to the list of channels
def test_valid_channels_create_v1_multiple(clear_data,test_user):
    #created a second user_id by regestring a valid user
    userId2 = auth_register_v1("validemail2@g.com", "validpass2", "validname2","validname2")
    #Valid case where a public channel with name "ValidChannelName1" is created by user with auth_id userId1
    channels_create_v1(test_user, "ValidChannelName1", True)
    #Valid case where a public channel with name "ValidChannelName2" is created by user with auth_id userId2
    channels_create_v1(userId2['auth_user_id'], "ValidChannelName2", True)
    assert(len(data['channels']) > 1)



#testing an invalid case(channel name is more than 20 characters long) 
def test_invalidName_channels_create_v1(clear_data,test_user):

    #channel name is more than 20 characters long
    invalidName = "nameismorethantwentycharacters"
    with pytest.raises(InputError): # An input error is raised when a channel name that is more than 20 characters long is passed intot the function 
        channels_create_v1(test_user,invalidName, True)
    


'''#testing when a user with an invalid u_id trys to create a channel
def test_invalid_user(clear_data):
    #invalid case where a public channel with name "ValidChannelName" is created by user with an INvalid u_id
    with pytest.raises(AccessError): An accesserror is raised when user trying to register is an invlaid user
        channels_create_v1(8,'channelname',True)'''





    

