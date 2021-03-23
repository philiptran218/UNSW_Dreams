import pytest
from src.other import clear_v1
from src.auth import auth_register_v1
from src.dm import dm_remove_v1, dm_create_v1, dm_list_v1, dm_messages_v1
from src.error import AccessError, InputError 
INVALID_DM_ID = -1
INVALID_TOKEN = -1

# Fixture that clears and resets all the internal data of the application
@pytest.fixture
def clear_data():
    clear_v1()

@pytest.fixture
def test_user1_token():
    user_info = auth_register_v1("validemail@g.com", "validpass", "validname","validname")
    return user_info["token"]


@pytest.fixture
def test_user2_u_id():
    user_info = auth_register_v1("dan@gmail.com", "password", "dan", "Smith")
    return user_info['auth_user_id']

@pytest.fixture
def test_user3_token():
    user_info = auth_register_v1("danimatt@gmail.com", "valpassword", "danny", "Smithy")
    return user_info['token']




@pytest.fixture
def test_create_dm(test_user1_token,test_user2_u_id):
    dm = dm_create_v1((test_user1_token,test_user2_u_id))
    return dm['dm_id']



#testing when dm_id is invalid -> InputError is raised
def test_dm_messages_invalid_dm_id(clear_data,test_create_dm,test_user1_token,test_user2_u_id):
    with pytest.raises(InputError):
        dm_messages_v1(test_user1_token,INVALID_DM_ID,0)

#testing when token is invalid -> AccessError is raised 
def test_dm_messages_invalid_token(clear_data,test_create_dm,test_user1_token,test_user2_u_id):
    with pytest.raises(AccessError):
        dm_messages_v1(INVALID_TOKEN,test_create_dm,0)

#testing when start is not equal to 0 when there are 0 messages -> InputError is raised
def test_dm_messages_invalid_start(clear_data,test_create_dm,test_user1_token,test_user2_u_id):
    with pytest.raises(InputError):
        dm_messages_v1(test_user1_token,test_create_dm,20)

#testing when user who calls dm_messages with a sepcific dm_id is not part of that dm -> AccessError is raised 
def test_dm_messages_user_not_member(clear_data,test_create_dm,test_user1_token,test_user2_u_id,test_user3_token):
    with pytest.raises(AccessError):
        dm_messages_v1(test_user3_token,test_create_dm,0)


#testing when start is equal to number of messages 
def test_dm_messages_start_equal(clear_data,test_create_dm,test_user1_token,test_user2_u_id):
    dms = dm_messages_v1(test_user1_token,test_create_dm,0)
    assert (dms == {'messages': [], 'start': 0, 'end': -1})

