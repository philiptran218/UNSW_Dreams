import pytest
from src.other import clear_v1
from src.auth import auth_register_v1
from src.dm import dm_remove_v1 , dm_create_v1, dm_list_v1, dm_messages_v1, dm_invite_v1, dm_details_v1, dm_leave_v1
from src.error import AccessError, InputError 
from src.message import message_senddm_v1
INVALID_DM_ID = -1
INVALID_TOKEN = -1
INVALID_U_ID = -1



################################################################################
# pytest_fixtures                                                              #
################################################################################

# Fixture that clears and resets all the internal data of the application
@pytest.fixture
def clear_data():
    clear_v1()

# Fixture that creates a user and used to return their token
@pytest.fixture
def test_user1_token():
    user_info = auth_register_v1("validemail@g.com", "validpass", "validname","validname")
    return user_info

#fixture that creates a user and used to return their auth_user_id
@pytest.fixture
def test_user2_u_id():
    user_info = auth_register_v1("dan@gmail.com", "password", "dan", "Smith")
    return user_info

# Fixture that creates a user and used to return their token
@pytest.fixture
def test_user3_token():
    user_info = auth_register_v1("danimatt@gmail.com", "valpassword", "danny", "Smithy")
    return user_info

#fixture that creates a user and used to return their auth_user_id
@pytest.fixture
def test_user4_u_id():
    user_info = auth_register_v1("danny@gmail.com", "password123", "danny", "james")
    return user_info

#fixture that creates a dm by user1
@pytest.fixture
def test_create_dm(test_user1_token,test_user2_u_id):
    dm = dm_create_v1(test_user1_token['token'],test_user2_u_id['auth_user_id'])
    return dm['dm_id']

################################################################################
# dm_invite_v1 tests                                                           #
################################################################################

#testing when dm_id is invalid -> Input Error is raised
def test_dm_invite_invalid_dm_id(clear_data,test_user1_token,test_user2_u_id,test_create_dm):
    with pytest.raises(InputError):
        dm_invite_v1(test_user1_token['token'],INVALID_DM_ID,test_user2_u_id['auth_user_id'])
#testing when u_id is invalid -> Input Error is raised
def test_dm_invite_invalid_u_id(clear_data,test_user1_token,test_user2_u_id,test_create_dm):
    with pytest.raises(InputError):
        dm_invite_v1(test_user1_token['token'],test_create_dm,INVALID_U_ID)
#testing when user who is calling the fucntion is not part of the dm
def test_dm_invite_user_not_a_member(clear_data,test_user1_token,test_user2_u_id,test_user3_token,test_create_dm):
    with pytest.raises(AccessError):
        dm_invite_v1(test_user3_token['token'],test_create_dm,test_user2_u_id['auth_user_id'])

#testing a valid case by inviting a user and checking for membership
def test_dm_invite_valid(clear_data,test_user1_token,test_user2_u_id,test_user4_u_id,test_create_dm):
    dm_invite_v1(test_user1_token['token'],test_create_dm,test_user4_u_id['auth_user_id'])
    member_check = False
    dm_details = dm_details_v1(test_user1_token['token'],test_create_dm)
    members_list = dm_details['dm_members']
    for member in members_list:
        if member['u_id'] == test_user4_u_id['auth_user_id']:
            member_check = True
    assert(member_check)


################################################################################
# dm_remove_v1 tests                                                           #
################################################################################

def test_dm_remove_v1(clear_data,test_user1_token,test_user2_u_id,test_create_dm):
    dmsdict =  dm_list_v1(test_user1_token['token'])
    dm_remove_v1(test_user1_token['token'],test_create_dm) 
    assert( bool (dmsdict['dm']))

#testing when dm_id is invalid -> InputError is raised
def test_dm_remove_v1_invalid_dm(clear_data,test_user1_token,test_create_dm):
    with pytest.raises(InputError):
        dm_remove_v1(test_user1_token['token'],INVALID_DM_ID)


#testing when user trying to remove is not the original dm creator
def test_dm_remove_v1_unoriginal(clear_data,test_user1_token,test_user2_u_id,test_user3_token,test_create_dm):
    with pytest.raises(AccessError):
        dm_remove_v1(test_user3_token['token'],test_create_dm)



################################################################################
# dm_messages_v1 tests                                                         #
################################################################################

#testing when dm_id is invalid -> InputError is raised
def test_dm_messages_invalid_dm_id(clear_data,test_create_dm,test_user1_token,test_user2_u_id):
    with pytest.raises(InputError):
        dm_messages_v1(test_user1_token['token'],INVALID_DM_ID,0)

#testing when token is invalid -> AccessError is raised 
def test_dm_messages_invalid_token(clear_data,test_create_dm,test_user1_token,test_user2_u_id):
    with pytest.raises(AccessError):
        dm_messages_v1(INVALID_TOKEN,test_create_dm,0)

#testing when start is not equal to 0 when there are 0 messages -> InputError is raised
def test_dm_messages_invalid_start(clear_data,test_create_dm,test_user1_token,test_user2_u_id):
    with pytest.raises(InputError):
        dm_messages_v1(test_user1_token['token'],test_create_dm,20)

#testing when user who calls dm_messages with a sepcific dm_id is not part of that dm -> AccessError is raised 
def test_dm_messages_user_not_member(clear_data,test_create_dm,test_user1_token,test_user2_u_id,test_user3_token):
    with pytest.raises(AccessError):
        dm_messages_v1(test_user3_token['token'],test_create_dm,0)


#testing when start is equal to number of messages 
def test_dm_messages_start_equal(clear_data,test_create_dm,test_user1_token,test_user2_u_id):
    dms = dm_messages_v1(test_user1_token['token'],test_create_dm,0)
    assert (dms == {'messages': [], 'start': 0, 'end': -1})


#testing when one message is sent in the dm
def test_dm_messages_valid_single(clear_data,test_create_dm,test_user1_token,test_user2_u_id):
    # Tests for a single message in dm
    message_senddm_v1(test_user1_token['token'],test_create_dm,'A new message')
    message_detail = dm_messages_v1(test_user1_token['token'], test_create_dm, 0)
    
    # Checking the message dictionary to see if message has been appended
    assert message_detail['messages'][0]['message_id'] == 1
    assert message_detail['messages'][0]['u_id'] == test_user1_token['auth_user_id']
    assert message_detail['messages'][0]['message'] == 'A new message'
    assert message_detail['start'] == 0
    assert message_detail['end'] == -1

#testing when more than one message is sent in the dm
def test_dm_messages_multiple(clear_data,test_create_dm,test_user1_token,test_user2_u_id):
    # Testing for multiple messages, and non-zero start value 
    # Sends 55 messages to dm, the messages are just numbers as strings
    i = 1
    while i <= 55:
        message_senddm_v1(test_user1_token['token'], test_create_dm, f"{i}")
        i += 1
    
    message_detail = dm_messages_v1(test_user1_token['token'],test_create_dm, 2)
   
    # Checking that the messages have been appended correctly
    i = 53
    j = 0
    while i >= 4:
        assert message_detail['messages'][j]['message_id'] == i
        assert message_detail['messages'][j]['u_id'] == test_user1_token['auth_user_id']
        assert message_detail['messages'][j]['message'] == str(i)
        i -= 1
        j += 1 
    assert message_detail['start'] == 2
    assert message_detail['end'] == 52


################################################################################
# dm_leave_v1 tests                                                           #
################################################################################

#testing when dm_id is invalid -> InputError is raised
def test_dm_leave_invalid_dm_id(clear_data,test_user1_token,test_user2_u_id,test_create_dm):
    with pytest.raises(InputError):
        dm_leave_v1(test_user1_token['token'],INVALID_DM_ID)

#testing when user who is calling the fucntion is not part of the dm -> AccessError is raised
def test_dm_leave_user_not_a_member(clear_data,test_user1_token,test_user2_u_id,test_user3_token,test_create_dm):
    with pytest.raises(AccessError):
        dm_leave_v1(test_user3_token['token'],test_create_dm)

#testing if a  member of the dm left it and after calling dm_leave.
def test_dm_leave(clear_data,test_user1_token,test_user2_u_id,test_create_dm):
    dm_leave_v1(test_user1_token['token'],test_create_dm)
    member_left = True
    dlist = dm_list_v1(test_user1_token['token'])
    for dm in dlist['dm']:
        for member in dm['dm_members']:
            if member['u_id'] == test_user1_token['auth_u_id']:
                member_left = False
    assert(member_left)
                

    