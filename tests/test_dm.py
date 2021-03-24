import pytest
from src.other import clear_v1
from src.auth import auth_register_v2
from src.dm import is_valid_dm_id, is_valid_uid, is_dm_creator, dm_create_v1, dm_details_v1, dm_list_v1
from src.error import AccessError, InputError 
INVALID_DM_ID = -1
INVALID_TOKEN = -1
INVALID_U_ID = -1

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
    return user_info["auth_u_id"]

@pytest.fixture
def test_user2_token():
    user_info = auth_register_v2("dan@gmail.com", "password", "dan", "Smith")
    return user_info["token"]

@pytest.fixture
def test_user2_u_id():
    user_info = auth_register_v2("dan@gmail.com", "password", "dan", "Smith")
    return user_info["auth_u_id"]

#Fixture that create a dm to test functions. 
@pytest.fixture
def test_dm(test_user1_token, test_user1_u_id):
    dm = dm_create_v1(test_user1_token, test_user1_u_id)
    return dm["dm_id"], dm["dm_name"] 

#Function that shows expected output for dm_details.
def expected_output_details_v1():
    return {
        "dm_name": 'validnamevalidname',
        "members": [
            {
                'u_id': 1,
                'name_first': 'validname',
                'name_last': 'vaidname',
                'email': 'validemail@g.com',
                'handle_str': 'validnamevalidname'
            }
        ]
    }

#Function that shows expected output for dm_list.
def expected_output_list_v1():
    return {
        'dms': [
            {
                "dm_id": 1,
                "name": "validnamevalidname"
            }
        ]
    }

#Function that shows expected output for dm_create.
def expected_output_create_v1():
    return {
        {
            "dm_id": 1,
            "dm_name": "validnamevalidname"
        }
    }

################################################################################
#  dm_details_v1, dm_list_v1 and dm_create_v1 testing                          #
################################################################################

def test_dm_details_v1_valid(clear_data, test_dm, test_user1_token, test_user1_u_id):
    assert(dm_details_v1(test_user1_token, test_user1_u_id) == expected_output_details_v1())

def test_dm_details_v1_invalid_InputError(clear_data, test_dm, test_user1_token):
    with pytest.raises(InputError):
        dm_details_v1(test_user1_token, INVALID_DM_ID)

def test_dm_details_v1_invalid_AccessError(clear_data, test_dm, test_user2_token, test_user2_u_id):
    with pytest.raises(AccessError):
        dm_details_v1(test_user2_token, test_user2_u_id)

def test_dm_details_v1_invalid_token(clear_data, test_dm, test_user1_u_id):
    with pytest.raises(AccessError):
        dm_details_v1(INVALID_TOKEN, test_user1_u_id)

def test_dm_list_v1_valid():
    assert(dm_list_v1(test_user1_token) == expected_output_list_v1())

def test_dm_list_v1_invalid(clear_data, test_dm):
    with pytest.raises(AccessError):
        dm_list_v1(INVALID_TOKEN)

def test_dm_create_v1_valid(clear_data, test_dm, test_user1_token, test_user1_u_id):
    assert(dm_create_v1(test_user1_token, test_user1_u_id) == expected_output_create_v1())

def test_dm_create_v1_invalid_u_id(clear_data, test_dm, test_user1_token):
    with pytest.raises(AccessError):
        dm_create_v1(test_user1_token, INVALID_U_ID)

def test_dm_create_v1_invalid_token(clear_data, test_dm, test_user1_u_id):
    with pytest.raises(AccessError):
        dm_create_v1(INVALID_TOKEN, test_user1_u_id)
