import pytest
from src.other import clear_v1
from src.auth import auth_register_v2
from src.dm import dm_remove_v1
from src.error import AccessError 
INVALID_DM_ID = -1

# Fixture that clears and resets all the internal data of the application
@pytest.fixture
def clear_data():
    clear_v1()

@pytest.fixture
def test_user1_token():
    user_info = auth_register_v2("validemail@g.com", "validpass", "validname","validname")
    return user_info["token"]


@pytest.fixture
def test_user2_u_id():
    user_info = auth_register_v2("dan@gmail.com", "password", "dan", "Smith")
    return user_info['auth_user_id']

@pytest.fixture
def test_user3_token():
    user_info = auth_register_v2("danimatt@gmail.com", "valpassword", "danny", "Smithy")
    return user_info['token']

def test_dm_remove_v1(clear_data,test_user1_token,test_user2_u_id):
    dm_id = dm_create_v1(test_user1_token,test_user2_u_id)['dm_id']
    dmsdict =  dm_list_v1(test_user1_token)
    assert(dm_remove_v1(test_user1_token,dm_id) ==( bool (not dmsdict['dms'])) )


def test_dm_remove_v1_invalid_dm(clear_data,test_user1_token,):
    dm_id = dm_create_v1(test_user1_token,test_user2_u_id)['dm_id']
    with pytest.raises(AccessError):
        dm_remove_v1(test_user1_token,INVALID_DM_ID)



def test_dm_remove_v1_unoriginal(clear_data,test_user1_token,test_user2_u_id,test_user3_token):
    dm_id = dm_create_v1(test_user1_token,test_user2_u_id)['dm_id']
    with pytest.raises(AccessError):
        dm_remove_v1(test_user3_token,dm_id)