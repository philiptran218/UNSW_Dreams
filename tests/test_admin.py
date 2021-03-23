import pytest
from src.other import clear_v1
from src.auth import auth_register_v2
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
    return user_info['auth_user_id']

################################################################################
#  admin_user_remove_v1 and admin_userpermission_change_v1 testing             #
################################################################################

def test_admin_user_remove_v1_valid(clear_data, test_dm, test_user1_token, test_user2_u_id):
    #assert()
    pass

def test_admin_user_remove_v1_invalid_u_id(clear_data, test_dm, test_user1_token):
    with pytest.raises(InputError):
        admin_user_remove_v1(test_user1_token, INVALID_U_ID)

def test_admin_user_remove_v1_invalid_only_owner(clear_data, test_dm, test_user1_token, test_user1_u_id):
    with pytest.raises(InputError):
        admin_user_remove_v1(test_user1_token, test_user1_u_id)

def test_admin_user_remove_v1_invalid_not_owner(clear_data, test_dm, test_user2_token, test_user1_u_id):
    with pytest.raises(AccessError):
        admin_user_remove_v1(test_user2_token, test_user1_u_id)

def test_admin_userpermission_change_v1_valid(clear_data, test_dm, test_user1_token, test_user2_u_id):
    #assert()
    pass

def test_admin_userpermission_change_v1_invalid_u_id(clear_data, test_dm, test_user1_token):
    with pytest.raises(InputError):
        admin_userpermission_change_v1(test_user1_token, INVALID_U_ID, OWNER)

def test_admin_userpermission_change_v1_invalid_perm_id(clear_data, test_dm, test_user1_token, test_user1_u_id):
    with pytest.raises(InputError):
        admin_userpermission_change_v1(test_user1_token, test_user2_u_id, INVALID_PERMISSION_ID)

def test_admin_userpermission_change_v1_invalid_not_owner(clear_data, test_dm, test_user2_token, test_user1_u_id):
    with pytest.raises(AccessError):
        admin_userpermission_change_v1(test_user1_token, test_user2_u_id, MEMBER)