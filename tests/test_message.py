import pytest
from src.error import InputError, AccessError 
from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.other import clear_v1
from src.channel import channel_messages_v1, channel_join_v1
from src.message import message_send_v1, message_remove_v1

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
def dm1(user1):
    new_dm1 = dm_create_v1(user1, [user1])
    return new_dm1['dm_id']

@pytest.fixture
def clear_database():
    clear_v1()
    
@pytest.fixture
def message1(user1, channel1):
    msgid = message_send_v1(user1, channel1, 'Hello World')
    return msgid['message_id']
    
@pytest.fixture
def message2(user1, dm1):
    msgid = message_senddm_v1(user1, dm1, 'Hello there')
    return msgid['message_id']

################################################################################
# message_remove_v1 tests                                                      #
################################################################################
   
def test_message_remove_uid_does_not_exist(clear_database, user1, channel1, message1):
    # Raises AccessError since u_id INVALID_ID does not exist
    with pytest.raises(AccessError):
        message_remove_v1(INVALID_ID, message1)
 
# Assuming InputError raised when message_id does not exist
def test_message_remove_invalid_messageid(clear_database, user1, channel1):
    # Raises InputError since message_id INVALID_ID does not exist
    with pytest.raises(InputError):
        message_remove_v1(user1, INVALID_ID)
    
def test_message_remove_deleted_message(clear_database, user1, channel1, message1): 
    # Raises InputError since message has already been deleted 
    message_remove_v1(user1, message1)
    with pytest.raises(InputError):
        message_remove_v1(user1, message1)
               
def test_message_remove_accesserror(clear_database, user1, channel1, user2, message1):
    # Raises AccessError since user2 is not an owner of channel1, is not an 
    # owner of Dreams and is not the author of message1
    with pytest.raises(AccessError):
        message_remove_v1(user2, message1)
     
def test_message_remove_accesserror2(clear_database, user1, channel1, user2, message1):
    # This test is similar to previous test, but should still raise AccessError
    # as user2 is just a member of channel1
    channel_join_v1(user2, channel1)
    with pytest.raises(AccessError):
        message_remove_v1(user2, message1)
        
def test_message_remove_accesserror3(clear_database, user1, user2, dm1, message2):
    # Raises AccessError since user2 is not an owner of dm1, is not an owner of
    # Dreams and is not the author of message2
    with pytest.raises(AccessError):
        message_remove_v1(user2, message2)
            
def test_message_remove_from_dm(clear_database, user1, channel1, message1):
    # Checking if message1 has been successfully removed from channel1
    message_remove_v1(user1, message1)
    assert channel_messages_v1(user1, channel1, 0) == {'messages': [], 'start': 0, 'end': -1}

def test_message_remove_from_dm(clear_database, user1, dm1, message2):
    # Checking if message2 has been successfully removed from dm1
    message_remove_v1(user1, message2)
    assert dm_messages_v1(user1, dm1, 0) == {'messages': [], 'start': 0, 'end': -1}
'''
def test_message_remove_from_channel_and_dm(clear_database, user1, channel1, dm1, message1):
    # Testing if a message in both a channel and DM is successfully removed
    new_channel2 = channels_create_v1(user1, 'Channel2', True)
    share_msg = message_share_v1(user1, message1, '', new_channel2['channel_id'], dm1)
    assert len(channel_messages_v1(user1, new_channel2['channel_id'], 0)['messages']) == 1
    assert len(dm_messages_v1(user1, dm1, 0)['messages']) == 1
    
    message_remove_v1(user1, share_msg['shared_message_id'])
    assert channel_messages_v1(user1, new_channel2['channel_id'], 0) == {'messages': [], 'start': 0, 'end': -1}
    assert dm_messages_v1(user1, dm1, 0) == {'messages': [], 'start': 0, 'end': -1}
'''        

