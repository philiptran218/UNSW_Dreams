from src.other import clear_v1
from src.auth import auth_register_v1, auth_login_v1
from src.channel import channel_messages_v1
from src.channels import channels_create_v1, channels_listall_v1
from src.database import data
import pytest
from src.error import InputError, AccessError

def test_clear_v1():
    email = "bob.b@gmail.com"
    password = "valpassword"
    user_id = auth_register_v1(email, password, "bobby", "flay")
    channels_create_v1(user_id['auth_user_id'],"bobschannel", True)
    clear_v1()
    # Should raise InputError as registered user has been deleted and thus
    # cannot login.
    with pytest.raises(InputError):
        auth_login_v1(email, password)
    # Create a user inorder to run channels_listall_v1() which should return
    # an empty list as all channels have been deleted.
    user_id = auth_register_v1(email, password, "bobby", "flay")
    assert(channels_listall_v1(user_id['auth_user_id']) == {'channels': []})

    # Cannot check if messages have been cleared yet (Iteration 1).
