import pytest
from src.other import clear_v1
from src.auth import auth_register_v2, auth_login_v2
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
def test_user1():
    user_info = auth_register_v2("validemail@g.com", "validpass", "validname","validname")
    return user_info

@pytest.fixture
def test_user2():
    user_info = auth_register_v2("dan@gmail.com", "password", "dan", "Smith")
    return user_info

@pytest.fixture
def test_user3():
    user_info = auth_register_v2("danimatt@gmail.com", "valpassword", "danny", "Smithy")
    return user_info

#Fixture that create a dm to test functions. 
@pytest.fixture
def test_dm(test_user1, test_user2):
    dm = dm_create_v1(test_user1['token'], test_user2['auth_user_id'])
    return dm

#Function that shows expected output for dm_details.
def expected_output_details_v1():
    return {
        "dm_name": 'dansmith, validnamevalidname',
        "dm_members": [
            {
                'u_id': 1,
                'name_first': 'validname',
                'name_last': 'validname',
                'email': 'validemail@g.com',
                'handle_str': 'validnamevalidname'
            },
            {
                'u_id': 2,
                'name_first': 'dan',
                'name_last': 'Smith',
                'email': 'dan@gmail.com',
                'handle_str': 'dansmith'
            }
        ]
    }

#Function that shows expected output for dm_list.
def expected_output_list_v1():
    return {
        'dm': [
            {
                "dm_id": 1,
                "dm_name": "dansmith, validnamevalidname"
            }
        ]
    }

# Function that shows expected output for dm_create. Note it is different from the 
# output for list, despite looking similar.
def expected_output_create_v1():
    return {
        "dm_id": 1,
        "dm_name": "dansmith, validnamevalidname"
    }

################################################################################
#  dm_details_v1 testing                                                       #
################################################################################

def test_dm_details_v1_valid(clear_data, test_dm, test_user1, test_user2):
    assert(dm_details_v1(test_user1['token'], test_dm['dm_id']) == expected_output_details_v1())

def test_dm_details_v1_invalid_InputError(clear_data, test_user1, test_dm):
    with pytest.raises(InputError):
        dm_details_v1(test_user1['token'], INVALID_DM_ID)

def test_dm_details_v1_invalid_AccessError(clear_data, test_dm, test_user3):
    with pytest.raises(AccessError):
        dm_details_v1(test_user3['token'], test_dm['dm_id'])

def test_dm_details_v1_invalid_token(clear_data, test_dm):
    with pytest.raises(AccessError):
        dm_details_v1(INVALID_TOKEN, test_dm['dm_id'])

################################################################################
#  dm_list_v1 testing                                                          #
################################################################################

def test_dm_list_v1_valid_empty(clear_data, test_user1):
    assert(dm_list_v1(test_user1['token']) == {'dm': []})

def test_dm_list_v1_valid(clear_data, test_user1, test_user2, test_dm):
    assert(dm_list_v1(test_user1['token']) == expected_output_list_v1())

def test_dm_list_v1_invalid(clear_data):
    with pytest.raises(AccessError):
        dm_list_v1(INVALID_TOKEN)

################################################################################
#  dm_create_v1 testing                                                        #
################################################################################

def test_dm_create_v1_valid(clear_data, test_user1, test_user2):
    assert(dm_create_v1(test_user1['token'], test_user2['auth_user_id']) == expected_output_create_v1())

def test_dm_create_v1_invalid_u_id(clear_data, test_user1):
    with pytest.raises(AccessError):
        dm_create_v1(test_user1['token'], INVALID_U_ID)

def test_dm_create_v1_invalid_token(clear_data, test_user2):
    user_list = [test_user2['auth_user_id']]
    with pytest.raises(AccessError):
        dm_create_v1(INVALID_TOKEN, user_list)
