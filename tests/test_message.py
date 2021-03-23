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
    new_channel2 = channels_create_v1(user2, 'Channel2', True)
    return new_channel2['channel_id']
    
@pytest.fixture
def dm1(user1):
    new_dm1 = dm_create_v1(user1, [user1])
    return new_dm1['dm_id']
    
@pytest.fixture
def dm2(user2):
    new_dm2 = dm_create_v1(user2, [user2])
    return new_dm2['dm_id']
    
@pytest.fixture
def clear_database():
    clear_v1()
    
@pytest.fixture
def message1(user1, channel1):
    msgid = message_send_v1(user1, channel1, 'Hello World')
    return msgid['message_id']

################################################################################
# message_share_v1 tests                                                       #
################################################################################

def test_message_share_invalid_uid(clear_database, user1, user2, channel1, channel2, message1):
    # Raises AccessError since u_id INVALID_ID does not exist
    with pytest.raises(AccessError):
        message_share_v1(INVALID_ID, message1, '', channel2, -1)
        
def test_message_share_invalid_channel(clear_database, user1, user2, channel1, message1):
    # Raises InputError since channel_id INVALID_ID does not exist
    with pytest.raises(InputError):
        message_share_v1(user2, message1, '', INVALID_ID, -1)
        
def test_message_share_invalid_dm(clear_database, user1, user2, channel1, message1):
    # Raises InputError since dm_id INVALID_ID does not exist
    with pytest.raises(InputError):
        message_share_v1(user2, message1, '', -1, INVALID_ID)
       
def test_message_share_invalid_messageid(clear_database, user1, user2, channel1, channel2, message1):
    # Raises InputError since og_message_id INVALID_ID does not exist
    with pytest.raises(InputError):
        message_share_v1(user2, INVALID_ID, '', channel2, -1)
        
def test_message_share_removed_message(clear_database, user1, user2, channel1, channel2, message1):
    # Raises InputError since message1 has been deleted
    message_remove(user1, message1)
    with pytest.raises(InputError):
        message_share_v1(user2, message1, '', channel2, -1)

def test_message_share_channel_accesserror(clear_database, user1, user2, channel1, channel2, message1):
    # Raises AccessError since user1 is not in channel2
    with pytest.raises(AccessError):
        message_share_v1(user1, message1, '', channel2, -1)
     
def test_message_share_dm_accesserror(clear_database, user1, user2, channel1, dm2, message1):
    # Raises AccessError since user1 is not in dm2
    with pytest.raises(AccessError):
        message_share_v1(user1, message1, '', -1, dm2)
    
def test_message_share_invalid_length(clear_database, user1, user2, channel1, channel2, message1):
    # Raises InputError since og_message + message > 1000 characters
    i = 0
    message = ''
    while i < 500:
        message += str(i)
        i += 1
    with pytest.raises(InputError):
        message_share_v1(user2, message1, message, channel2, -1)
     
def test_message_share_to_channel_simple(clear_database, user1, user2, channel1, channel2, message1):
    # Tests sharing a single message to a channel
    assert channel_messages_v1(user2, channel2, 0) == {'messages': [], 'start': 0, 'end': -1}
    message_share_v1(user2, message1, '', channel2, -1)
    
    channel_messages = channel_messages_v1(user2, channel2, 0)['messages']
    assert channel_messages[0]['message'] == 'Hello World'
    assert channel_messages[0]['u_id'] == user2
       
def test_message_share_to_dm_simple(clear_database, user1, channel1, dm1, message1):
    # Tests sharing a single message to a DM
    assert dm_messages_v1(user1, dm1, 0) == {'messages': [], 'start': 0, 'end': -1}
    message_share_v1(user1, message1, '', -1, dm1)

    dm_messages = dm_messages_v1(user1, dm1, 0)['messages']
    assert dm_messages[0]['message'] == 'Hello World'
    assert dm_messages[0]['u_id'] == user1
    
def test_message_share_optional_msg(clear_database, user1, channel1, dm1, message1):
    # Tests adding an optional message to the original message, then sharing it
    # to a DM
    assert dm_messages_v1(user1, dm1, 0) == {'messages': [], 'start': 0, 'end': -1}
    message_share_v1(user1, message1, 'Hello Everyone', -1, dm1)

    dm_messages = dm_messages_v1(user1, dm1, 0)['messages']
    assert dm_messages[0]['message'] == 'Hello World Hello Everyone'
    assert dm_messages[0]['u_id'] == user1

