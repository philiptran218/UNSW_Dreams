from src.channels import channels_create_v1
from src.auth import auth_register_v1
import pytest
from src.error import InputError

def test_channels_create_v1():
    #created a user_id by regestring a valid user
    userId = auth_register_v1("validemail@g.com", "validpass", "validname","validname")
    
    #Valid case
    assert(channels_create_v1(userId, "ValidChannelName", True) == {'channel_id': 1})
    
    #channel name is more than 20 characters long
    invalidName = "nameismorethantwentycharacters"
    with pytest.raises(InputError):
        assert (channels_create_v1(userId,invalidName, True))
    







    
