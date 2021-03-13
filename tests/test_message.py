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

def test_message_send_invalid_uid(clear_database, channel1):
    with pytest.raises(AccessError):
        message_send_v1(1000, channel1, 'Hello World')
        
def test_message_send_uid_not_in_channel(clear_database, channel1, user2):
    with pytest.raises(AccessError):
        message_send_v1(user2, channel1, 'Hello World')
        
def test_message_send_invalid_messages(clear_database, user1, channel1):
    i = 0
    message = ''
    while i < 500:
        message += str(i)
        i += 1
    with pytest.raises(InputError):
        message_send_v1(user1, channel1, message)
        
def test_message_send_invalid_channel(clear_database, user1):
    with pytest.raises(InputError):
        message_send_v1(user1, 1000, 'Nice to meet you!')
        
# Assuming that empty messages will not be valid/code will not add an empty message
# which is either blank or only contains whitespace
def test_message_send_empty_message(clear_database, user1, channel1):
    with pytest.raises(InputError):
        message_send_v1(user1, channel1, '')
        
def test_message_send_single_message(clear_database, user1, channel1):
    msgid = message_send_v1(user1, channel1, 'Hello World')
    
    channel_messages = channel_messages_v1(user1, channel1, 0)['messages']
    assert len(channel_messages) == 1
    assert channel_messages[0]['message_id'] == msgid['message_id']
    assert channel_messages[0]['u_id'] == user1
    assert channel_messages[0]['message'] == 'Hello World'


