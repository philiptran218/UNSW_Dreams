from src.other import clear_v1
from src.auth import auth_register_v1, auth_login_v1
from src.channel import channel_messages_v1
from src.channels import channels_create_v1, channels_listall_v1
from src.user import user_profile_v1
from src.database import data
import pytest
from src.error import InputError, AccessError

def test_clear_v1():
    email = "bob.b@gmail.com"
    password = "valpassword"
    user_id = auth_register_v1(email, password, "bobby", "flay")
    channel = channels_create_v1(user_id['auth_user_id'],"bobschannel", True)

    clear_v1()
    with pytest.raises(InputError):
        auth_login_v1(email, password)
    with pytest.raises(AccessError):
        channels_listall_v1(user_id['auth_user_id'])
    with pytest.raises(AccessError):
        channel_messages_v1(user_id['auth_user_id'], channel['channel_id'], 0) 
    