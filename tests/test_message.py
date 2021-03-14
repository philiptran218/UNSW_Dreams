import pytest
from src.error import InputError, AccessError 
from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.other import clear_v1
from src.channel import channel_messages_v1, channel_join_v1
from src.message import message_send_v1, message_remove_v1

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
    
def test_message_remove_deleted_message(clear_database, user1, channel1, message1):  
    message_remove_v1(user1, message1)
    with pytest.raises(InputError):
        message_remove_v1(user1, message1)
               
def test_message_remove_accesserror(clear_database, user1, channel1, user2, message1):
    with pytest.raises(AccessError):
        message_remove_v1(user2, message1)
     
def test_message_remove_accesserror2(clear_database, user1, channel1, user2, message1):
    # This test is similar to previous test, but user2 is now a member of 
    # channel1
    channel_join_v1(user2, channel1)
    with pytest.raises(AccessError):
        message_remove_v1(user2, message1)
        
def test_message_remove_uid_does_not_exist(clear_database, user1, channel1, message1):
    with pytest.raises(AccessError):
        message_remove_v1(1000, message1)
        
# Assuming InputError raised when message_id does not exist
def test_message_remove_invalid_messageid(clear_database, user1, channel1):
    with pytest.raises(InputError):
        message_remove_v1(user1, 1000)
        
# Assuming that removed messages will no longer appear in channel
def test_message_remove_valid_single(clear_database, user1, channel1, message1):
    message_remove_v1(user1, message1)
    assert channel_messages_v1(user1, channel1, 0) == {'messages': [], 'start': 0, 'end': -1}

# Also write another test for removing from dm and channel simultaneously        

