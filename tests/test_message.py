import pytest
from src.error import InputError, AccessError 
from src.auth import auth_register_v1
# Change to import dm once created
from src.other import clear_v1
from src.message import message_senddm_v1

INVALID_ID = -1

@pytest.fixture
def user1():
    new_user1 = auth_register_v1('johnsmith@gmail.com', 'password', 'John', 'Smith')
    return new_user1['auth_user_id']
    
@pytest.fixture
def user2():
    new_user2 = auth_register_v1('philtran@gmail.com', 'password', 'Philip', 'Tran')
    return new_user2['auth_user_id']

@pytest.fixture
def dm1(user1):
    new_dm1 = dm_create_v1(user1, [user1])
    return new_dm1['dm_id']

@pytest.fixture
def clear_database():
    clear_v1()
    
################################################################################
# message_senddm_v1 tests                                                      #
################################################################################

def test_message_senddm_invalid_uid(clear_database, user1, dm1):
    # Raises AccessError since u_id INVALID_ID does not exist
    with pytest.raises(AccessError):
        message_senddm_v1(INVALID_ID, dm1, 'Hello World')
        
def test_message_senddm_invalid_dm(clear_database, user1):
    # Raises InputError since dm_id INVALID_ID does not exist
    with pytest.raises(InputError):
        message_senddm_v1(user1, INVALID_ID, 'Nice to meet you!')
        
def test_message_senddm_uid_not_in_dm(clear_database, user1, dm1, user2):
    # Raises AccessError since user2 is not in dm1
    with pytest.raises(AccessError):
        message_senddm_v1(user2, dm1, 'Hello World')
        
def test_message_senddm_invalid_messages(clear_database, user1, dm1):
    # Raises InputError since message > 1000 characters
    i = 0
    message = ''
    while i < 500:
        message += str(i)
        i += 1
    with pytest.raises(InputError):
        message_senddm_v1(user1, dm1, message)
            
def test_message_senddm_empty_message(clear_database, user1, dm1):
    # Assuming that function will not send empty messages (or messages with just
    # whitespace) and instead raises InputError
    with pytest.raises(InputError):
        message_senddm_v1(user1, dm1, '')
        
def test_message_senddm_empty_message2(clear_database, user1, dm1):
    # This test is same as above, but takes in a message filled with only
    # whitespace
    with pytest.raises(InputError):
        message_senddm_v1(user1, dm1, '          ')
        
def test_message_senddm_single_message(clear_database, user1, dm1):
    # Tests sending a single message to DM
    msgid = message_senddm_v1(user1, dm1, 'Hello World')
    
    dm_messages = dm_messages_v1(user1, dm1, 0)['messages']
    assert len(dm_messages) == 1
    assert dm_messages[0]['message_id'] == msgid['message_id']
    assert dm_messages[0]['u_id'] == user1
    assert dm_messages[0]['message'] == 'Hello World'

