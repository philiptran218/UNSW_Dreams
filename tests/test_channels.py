from src.channels import channels_create_v1
from src.auth import auth_register_v1
import pytest

class InputError(Exception):
    pass


def test_channels_create_v1():
    #created a user_id by regestring a valid user
    userId = auth_register_v1("validemail@g.com", "validpass", "validname","validname")
    
    #Valid case
    assert(channels_create_v1(userId, "channelname", True) == {'channel_id': 1})
   
    #channel name is more than 20 characters long
    invalidName = "nameismorethantwentycharacters"
    with pytest.raises(InputError):
        auth_register_v1("validemail@g.com", "validpass", invalidName, invalidName)
    







    
