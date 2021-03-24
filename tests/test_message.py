import pytest
from src.error import InputError, AccessError 
from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.other import clear_v1
from src.channel import channel_messages_v1
from src.message import message_send_v1, message_edit_v1, message_remove_v1, message_share_v1, message_senddm_v1

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
def message1(user1, channel1):
    msgid = message_send_v1(user1, channel1, 'Hello World')
    return msgid['message_id']
    
@pytest.fixture
def message2(user1, dm1):
    msgid = message_senddm_v1(user1, dm1, 'Hello There')
    return msgid['message_id']

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
    
################################################################################
# message_edit_v1 tests                                                        #
################################################################################

def test_message_edit_uid_does_not_exist(clear_database, user1, channel1, message1):
    # Raises AccessError since u_id INVALID_ID does not exist
    with pytest.raises(AccessError):
        message_edit_v1(INVALID_ID, message1, 'Another message edit')
        
def test_message_edit_invalid_messageid(clear_database, user1, channel1):
    # Raises InputError since message_id INVALID_ID does not exist
    with pytest.raises(InputError):
        message_edit_v1(user1, INVALID_ID, 'An even better message')

def test_message_edit_removed_message(clear_database, user1, channel1, message1):
    # Raises InputError since message1 has been removed
    message_remove_v1(user1, message1)
    with pytest.raises(InputError):
        message_edit_v1(user1, message1, 'Modifying this message')

def test_message_edit_invalid_length(clear_database, user1, channel1, message1):
    # Raises InputError since edited message > 1000 characters
    i = 0
    message = ''
    while i < 500:
        message += str(i)
        i += 1
    with pytest.raises(InputError):
        message_edit_v1(user1, message1, message)

def test_message_edit_accesserror_channel(clear_database, user1, channel1, user2, message1):
    # Raises AccessError since user2 is not an owner of channel1, is not an 
    # owner of Dreams and is not the author of message1
    with pytest.raises(AccessError):
        message_edit_v1(user2, message1, 'A new message')
        
def test_message_edit_accesserror_dm(clear_database, user1, user2, dm1, message2):
    # Raises AccessError since user2 is not an owner of dm1, is not an 
    # owner of Dreams and is not the author of message2
    with pytest.raises(AccessError):
        message_edit_v1(user2, message2, 'A new message')
                    
def test_message_edit_empty_message(clear_database, user1, channel1, message1):
    # Tests if an empty edited message will remove the current message
    channel_messages = channel_messages_v1(user1, channel1, 0)['messages']
    assert channel_messages[0]['message'] == 'Hello World'
    assert channel_messages[0]['u_id'] == user1
    
    message_edit_v1(user1, message1, '')
    channel_messages = channel_messages_v1(user1, channel1, 0)
    assert channel_messages == {'messages': [], 'start': 0, 'end': -1}

def test_message_edit_valid_single(clear_database, user1, channel1, message1):
    # Tests if message1 is successfully edited 
    channel_messages = channel_messages_v1(user1, channel1, 0)['messages']
    assert channel_messages[0]['message'] == 'Hello World'
    assert channel_messages[0]['u_id'] == user1
    message_edit_v1(user1, message1, 'This message has been edited')
    
    channel_messages = channel_messages_v1(user1, channel1, 0)['messages']
    assert channel_messages[0]['message'] == 'This message has been edited'
    assert channel_messages[0]['u_id'] == user1

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

