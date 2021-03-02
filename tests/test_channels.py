from src.channels import channels_create_v1
from src.auth import auth_register_v1
import pytest
from src.error import InputError
from src.other import clear_v1

@pytest.fixture
def clear_data():
    clear_v1()

def test_valid_channels_create_v1(clear_data):
    #created a user_id by regestring a valid user
    userId = auth_register_v1("validemail@g.com", "validpass", "validname","validname")
    #Valid case
    assert(channels_create_v1(userId, "ValidChannelName", True) == {'channel_id': 1})
    
def test_invalidName_channels_create_v1(clear_data):
    #created a user_id by regestring a valid user
    userId = auth_register_v1("validemail@g.com", "validpass", "validname","validname")
    #channel name is more than 20 characters long
    invalidName = "nameismorethantwentycharacters"
    with pytest.raises(InputError):
        assert (channels_create_v1(userId,invalidName, True))
    







    
