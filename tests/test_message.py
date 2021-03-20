import pytest
from src.error import InputError, AccessError 
from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.other import clear_v1
from src.channel import channel_messages_v1, channel_join_v1
from src.message import message_send_v1, message_remove_v1, message_edit_v1, message_share_v1

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
def channel1(user1):
    new_channel1 = channels_create_v1(user1, 'Channel1', True)
    return new_channel1['channel_id']
    
@pytest.fixture
def channel2(user2):
    new_channel2 = channels_create_v1(user1, 'Channel2', True)
    return new_channel2['channel_id']
    
@pytest.fixture
def clear_database():
    clear_v1()
    
@pytest.fixture
def message1(user1, channel1):
    msgid = message_send_v1(user1, channel1, 'Hello World')
    return msgid['message_id']

def test_message_share_uid_does_not_exist(clear_database, user1, user2, channel1, channel2, message1):
    with pytest.raises(AccessError):
        message_share_v1(INVALID_ID, message1, '', channel2, -1)

# Assuming AccessError if the channel does not exist        
def test_message_share_invalid_channel(clear_database, user1, user2, channel1, message1):
    with pytest.raises(AccessError):
        message_share_v1(user2, message1, '', INVALID_ID, -1)
        
# Assuming AccessError if the DM does not exist
def test_message_share_invalid_dm(clear_database, user1, user2, channel1, message1):
    with pytest.raises(AccessError):
        message_share_v1(user2, message1, '', -1, INVALID_ID)

# Assuming InputError if the message does not exist        
def test_message_share_invalid_messageid(clear_database, user1, user2, channel1, channel2, message1):
    with pytest.raises(InputError):
        message_share_v1(user2, INVALID_ID, '', channel2, -1)
        
def test_message_share_channel_accesserror(clear_database, user1, user2, channel1, channel2, message1):
    with pytest.raises(AccessError):
        message_share_v1(user1, message1, '', channel2, -1)

# Make a fixture to create a dm      
def test_message_share_dm_accesserror(clear_database, user1, channel1, message1):
    with pytest.raises(AccessError):
        message_share_v1(user1, message1, '', -1, 2)

# This test might not be needed (checks > 1000 for appended message)      
def test_message_share_invalid_length(clear_database, user1, user2, channel1, channel2, message1):
    i = 0
    message = ''
    while i < 500:
        message += str(i)
        i += 1
    with pytest.raises(InputError):
        message_share_v1(user2, message1, message, channel2, -1)
     
def test_message_share_to_channel_simple(clear_database, user1, user2, channel1, channel2, message1):
    message_share_v1(user2, message1, '', channel2, -1)
    
def test_message_share_to_dm_simple(clear_database, user1, channel1, dm1, message1):
    message_share_v1(user1, message1, '', -1, dm1)

# Add more complex cases, sharing from dm to channel, sharing multiple messages...
# Add test for sharing to both channel and dm (might not be needed)

