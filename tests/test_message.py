import pytest
from src.error import InputError, AccessError 
from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.other import clear_v1
from src.channel import channel_messages_v1
from src.message import message_send_v1

@pytest.fixture
def user1():
    new_user1 = auth_register_v1('johnsmith@gmail.com', 'password', 'John', 'Smith')
    return new_user1['auth_user_id']
    
@pytest.fixture
def user2():
    new_user2 = auth_register_v1('philtran@gmail.com', 'password', 'Philip', 'Tran')
    return new_user2['auth_user_id']

@pytest.fixture
def channel1(user1):
    new_channel1 = channels_create_v1(user1, 'Channel1', True)
    return new_channel1['channel_id']

@pytest.fixture
def clear_database():
    clear_v1()

INVALID_ID = -1

################################################################################
# message_send_v1 tests                                                        #
################################################################################

def test_message_send_invalid_uid(clear_database, user1, channel1):
    # Raises AccessError since u_id INVALID_ID does not exist
    with pytest.raises(AccessError):
        message_send_v1(INVALID_ID, channel1, 'Hello World')
        
def test_message_send_invalid_channel(clear_database, user1):
    # Raises InputError since channel_id INVALID_ID does not exist
    with pytest.raises(InputError):
        message_send_v1(user1, INVALID_ID, 'Nice to meet you!')
        
def test_message_send_uid_not_in_channel(clear_database, user1, channel1, user2):
    # Raises AccessError since user2 is not in channel1
    with pytest.raises(AccessError):
        message_send_v1(user2, channel1, 'Hello World')
        
def test_message_send_invalid_messages(clear_database, user1, channel1):
    # Raises InputError since message > 1000 characters
    i = 0
    message = ''
    while i < 500:
        message += str(i)
        i += 1
    with pytest.raises(InputError):
        message_send_v1(user1, channel1, message)
         
def test_message_send_empty_message(clear_database, user1, channel1):
    # Assuming that function will not add empty messages (or messages with just
    # whitespace) and instead raises InputError
    with pytest.raises(InputError):
        message_send_v1(user1, channel1, '')
        
def test_message_send_single_message(clear_database, user1, channel1):
    # Tests sending a single message to channel
    msgid = message_send_v1(user1, channel1, 'Hello World')
    
    channel_messages = channel_messages_v1(user1, channel1, 0)['messages']
    assert len(channel_messages) == 1
    assert channel_messages[0]['message_id'] == msgid['message_id']
    assert channel_messages[0]['u_id'] == user1
    assert channel_messages[0]['message'] == 'Hello World'

def test_message_send_multi_messages(clear_database, user1, channel1): 
    # Testing for multiple messages
    # Sends 55 messages to channel, the messages are just numbers as strings
    i = 1
    while i <= 55:
        message_send_v1(user1, channel1, f"{i}")
        i += 1
    
    message_detail = channel_messages_v1(user1, channel1, 2)
    # Checking that the messages have been appended correctly
    i = 53
    j = 0
    while i >= 4:
        assert message_detail['messages'][j]['message_id'] == i
        assert message_detail['messages'][j]['u_id'] == user1
        assert message_detail['messages'][j]['message'] == str(i)
        i -= 1
        j += 1 
    assert message_detail['start'] == 2
    assert message_detail['end'] == 52

