from src.other import clear_v1
from src.auth import auth_register_v1, auth_login_v1
from src.channels import channels_create_v1
from src.user import user_profile_v1
from src.database import data
def test_clear_v1():
    email = "bob.b@gmail.com"
    password = "valpassword"
    auth_user_id = auth_register_v1(email, password, "bobby", "flay")
    channels_create_v1(auth_user_id,"bobschannel", True)
    

    clear_v1()
    assert(data['users'] == [])
    assert(data['channels'] == [])
    assert(data['messages'] == [])
