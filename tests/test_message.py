import pytest
from src.error import InputError, AccessError 
from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.other import clear_v1
from src.channel import channel_messages_v1, channel_join_v1
from src.message import message_send_v1, message_remove_v1, message_edit_v1

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
    
@pytest.fixture
def message1(user1, channel1):
    msgid = message_send_v1(user1, channel1, 'Hello World')
    return msgid['message_id']

def test_message_edit_removed_message(clear_database, user1, channel1, message1):
    message_remove_v1(user1, message1)
    with pytest.raises(InputError):
        message_edit_v1(user1, message1, 'Modifying this message')

def test_message_edit_invalid_length(clear_database, user1, channel1, message1):
    i = 0
    message = ''
    while i < 500:
        message += str(i)
        i += 1
    with pytest.raises(InputError):
        message_edit_v1(user1, message1, message)

def test_message_edit_accesserror(clear_database, user1, channel1, user2, message1):
    with pytest.raises(AccessError):
        message_edit_v1(user2, message1, 'A new message')
        
def test_message_edit_accesserror2(clear_database, user1, channel1, user2, message1):
    # This test is similar to previous test, but user2 is now a member of 
    # channel1
    channel_join_v1(user2, channel1)
    with pytest.raises(AccessError):
        message_edit_v1(user2, message1, 'A new message')
        
# Assuming InputError raised when message_id does not exist (will report a 
# different error message compared to editing a deleted message_id)
def test_message_edit_invalid_messageid(clear_database, user1, channel1):
    with pytest.raises(InputError):
        message_edit_v1(user1, 1000, 'An even better message')
        
def test_message_edit_uid_does_not_exist(clear_database, user1, channel1, message1):
    with pytest.raises(AccessError):
        message_edit_v1(1000, message1, 'Another message edit')
        
def test_message_edit_valid_single(clear_database, user1, channel1, message1):
    channel_messages = channel_messages_v1(user1, channel1, 0)['messages']
    assert channel_messages[0]['message'] == 'Hello World'
    assert channel_messages[0]['u_id'] == user1
    message_edit_v1(user1, message1, 'This message has been edited')
    
    channel_messages = channel_messages_v1(user1, channel1, 0)['messages']
    assert channel_messages[0]['message'] == 'This message has been edited'
    assert channel_messages[0]['u_id'] == user1
    
# Also add more tests for complex cases and dealing with dms
# Add a case where message is edited by different author (update u_id)

