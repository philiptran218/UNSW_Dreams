import pytest
from src.error import InputError, AccessError 
from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.other import clear_v1
from src.channel import channel_messages_v1, channel_join_v1, channel_invite_v1, channel_leave_v1, channel_addowner_v1
from src.message import message_send_v1, message_edit_v1, message_remove_v1, message_pin_v1, message_unpin_v1, message_sendlater_v1, message_sendlaterdm_v1
from src.message import message_share_v1, message_senddm_v1, message_react_v1, message_unreact_v1
from src.dm import dm_create_v1, dm_messages_v1, dm_invite_v1, dm_leave_v1
from src.database import data

from datetime import datetime, timezone, timedelta
import threading
import time

INVALID_ID = 0
REACT_ID = 1

@pytest.fixture
def user1():
    new_user1 = auth_register_v1('johnsmith@gmail.com', 'password', 'John', 'Smith')
    return new_user1
    
@pytest.fixture
def user2():
    new_user2 = auth_register_v1('philtran@gmail.com', 'password', 'Philip', 'Tran')
    return new_user2

@pytest.fixture
def user3():
    new_user3 = auth_register_v1("terrynguyen@gmail.com", "password", "Terry", "Nguyen")
    return new_user3

@pytest.fixture
def channel1(user1):
    new_channel1 = channels_create_v1(user1['token'], 'Channel1', True)
    return new_channel1['channel_id']
    
@pytest.fixture
def channel2(user2):
    new_channel2 = channels_create_v1(user2['token'], 'Channel2', True)
    return new_channel2['channel_id']

@pytest.fixture
def dm1(user1):
    new_dm1 = dm_create_v1(user1['token'], [])
    return new_dm1['dm_id']
    
@pytest.fixture
def dm2(user2):
    new_dm2 = dm_create_v1(user2['token'], [])
    return new_dm2['dm_id']

@pytest.fixture
def message1(user1, channel1):
    msgid = message_send_v1(user1['token'], channel1, 'Hello World')
    return msgid['message_id']
    
@pytest.fixture
def message2(user1, dm1):
    msgid = message_senddm_v1(user1['token'], dm1, 'Hello There')
    return msgid['message_id']

@pytest.fixture
def message_time():
    time = datetime.now() + timedelta(0, 3)
    send_time = int(time.timestamp())
    return send_time

@pytest.fixture
def clear_database():
    clear_v1()

################################################################################
# message_send_v1 tests                                                        #
################################################################################

def test_message_send_invalid_token(clear_database, user1, channel1):
    # Raises AccessError since token INVALID_ID does not exist
    with pytest.raises(AccessError):
        message_send_v1(INVALID_ID, channel1, 'Hello World')
        
def test_message_send_invalid_channel(clear_database, user1):
    # Raises InputError since channel_id INVALID_ID does not exist
    with pytest.raises(InputError):
        message_send_v1(user1['token'], INVALID_ID, 'Nice to meet you!')
        
def test_message_send_invalid_channel_2(clear_database, user1):
    # Raises InputError since channel_id 10 does not exist
    with pytest.raises(InputError):
        message_send_v1(user1['token'], 10, 'Hello World')
        
def test_message_send_uid_not_in_channel(clear_database, user1, channel1, user2):
    # Raises AccessError since user2 is not in channel1
    with pytest.raises(AccessError):
        message_send_v1(user2['token'], channel1, 'Hello World')
        
def test_message_send_invalid_messages(clear_database, user1, channel1):
    # Raises InputError since message > 1000 characters
    i = 0
    message = ''
    while i < 500:
        message += str(i)
        i += 1
    with pytest.raises(InputError):
        message_send_v1(user1['token'], channel1, message)
         
def test_message_send_empty_message(clear_database, user1, channel1):
    # Assuming that function will not add empty messages (or messages with just
    # whitespace) and instead raises InputError
    with pytest.raises(InputError):
        message_send_v1(user1['token'], channel1, '')
        
def test_message_send_single_message(clear_database, user1, channel1):
    # Tests sending a single message to channel
    msgid = message_send_v1(user1['token'], channel1, 'Hello World')
    
    channel_messages = channel_messages_v1(user1['token'], channel1, 0)['messages']
    assert len(channel_messages) == 1
    assert channel_messages[0]['message_id'] == msgid['message_id']
    assert channel_messages[0]['u_id'] == user1['auth_user_id']
    assert channel_messages[0]['message'] == 'Hello World'

def test_message_send_multi_messages(clear_database, user1, channel1): 
    # Testing for multiple messages
    # Sends 55 messages to channel, the messages are just numbers as strings
    i = 1
    while i <= 55:
        message_send_v1(user1['token'], channel1, f"{i}")
        i += 1
    
    message_detail = channel_messages_v1(user1['token'], channel1, 2)
    # Checking that the messages have been appended correctly
    i = 53
    j = 0
    while i >= 4:
        assert message_detail['messages'][j]['message_id'] == i
        assert message_detail['messages'][j]['u_id'] == user1['auth_user_id']
        assert message_detail['messages'][j]['message'] == str(i)
        i -= 1
        j += 1 
    assert message_detail['start'] == 2
    assert message_detail['end'] == 52
    
################################################################################
# message_edit_v1 tests                                                        #
################################################################################

def test_message_edit_uid_does_not_exist(clear_database, user1, channel1, message1):
    # Raises AccessError since token INVALID_ID does not exist
    with pytest.raises(AccessError):
        message_edit_v1(INVALID_ID, message1, 'Another message edit')
        
def test_message_edit_invalid_messageid(clear_database, user1, channel1):
    # Raises InputError since message_id INVALID_ID does not exist
    with pytest.raises(InputError):
        message_edit_v1(user1['token'], INVALID_ID, 'An even better message')

def test_message_edit_removed_message(clear_database, user1, channel1, message1):
    # Raises InputError since message1 has been removed
    message_remove_v1(user1['token'], message1)
    with pytest.raises(InputError):
        message_edit_v1(user1['token'], message1, 'Modifying this message')

def test_message_edit_invalid_length(clear_database, user1, channel1, message1):
    # Raises InputError since edited message > 1000 characters
    i = 0
    message = ''
    while i < 500:
        message += str(i)
        i += 1
    with pytest.raises(InputError):
        message_edit_v1(user1['token'], message1, message)

def test_message_edit_accesserror_channel(clear_database, user1, channel1, user2, message1):
    # Raises AccessError since user2 is not an owner of channel1, is not an 
    # owner of Dreams and is not the author of message1
    with pytest.raises(AccessError):
        message_edit_v1(user2['token'], message1, 'A new message')
        
def test_message_edit_accesserror_dm(clear_database, user1, user2, dm1, message2):
    # Raises AccessError since user2 is not an owner of dm1, is not an 
    # owner of Dreams and is not the author of message2
    with pytest.raises(AccessError):
        message_edit_v1(user2['token'], message2, 'A new message')
                    
def test_message_edit_empty_message(clear_database, user1, user2, channel1, channel2, message1):
    # Tests if an empty edited message will remove the current message (being
    # removed by the owner of channel2)
    msgid = message_send_v1(user2['token'], channel2, 'Hi Everyone')
    channel_messages = channel_messages_v1(user2['token'], channel2, 0)['messages']
    assert channel_messages[0]['message'] == 'Hi Everyone'
    assert channel_messages[0]['u_id'] == user2['auth_user_id']
    
    message_edit_v1(user2['token'], msgid['message_id'], '')
    channel_messages = channel_messages_v1(user2['token'], channel2, 0)
    assert channel_messages == {'messages': [], 'start': 0, 'end': -1}

def test_message_edit_valid_single(clear_database, user1, channel1, message1):
    # Tests if message1 is successfully edited 
    channel_messages = channel_messages_v1(user1['token'], channel1, 0)['messages']
    assert channel_messages[0]['message'] == 'Hello World'
    assert channel_messages[0]['u_id'] == user1['auth_user_id']
    message_edit_v1(user1['token'], message1, 'This message has been edited')
    
    channel_messages = channel_messages_v1(user1['token'], channel1, 0)['messages']
    assert channel_messages[0]['message'] == 'This message has been edited'
    assert channel_messages[0]['u_id'] == user1['auth_user_id']

################################################################################
# message_remove_v1 tests                                                      #
################################################################################
   
def test_message_remove_uid_does_not_exist(clear_database, user1, channel1, message1):
    # Raises AccessError since token INVALID_ID does not exist
    with pytest.raises(AccessError):
        message_remove_v1(INVALID_ID, message1)
 
# Assuming InputError raised when message_id does not exist
def test_message_remove_invalid_messageid(clear_database, user1, channel1):
    # Raises InputError since message_id INVALID_ID does not exist
    with pytest.raises(InputError):
        message_remove_v1(user1['token'], INVALID_ID)
    
def test_message_remove_deleted_message(clear_database, user1, channel1, message1): 
    # Raises InputError since message has already been deleted 
    message_remove_v1(user1['token'], message1)
    with pytest.raises(InputError):
        message_remove_v1(user1['token'], message1)
               
def test_message_remove_accesserror(clear_database, user1, channel1, user2, message1):
    # Raises AccessError since user2 is not an owner of channel1, is not an 
    # owner of Dreams and is not the author of message1
    with pytest.raises(AccessError):
        message_remove_v1(user2['token'], message1)
     
def test_message_remove_accesserror2(clear_database, user1, channel1, user2, message1):
    # This test is similar to previous test, but should still raise AccessError
    # as user2 is just a member of channel1
    channel_join_v1(user2['token'], channel1)
    with pytest.raises(AccessError):
        message_remove_v1(user2['token'], message1)
        
def test_message_remove_accesserror3(clear_database, user1, user2, dm1, message2):
    # Raises AccessError since user2 is not an owner of dm1, is not an owner of
    # Dreams and is not the author of message2
    with pytest.raises(AccessError):
        message_remove_v1(user2['token'], message2)
            
def test_message_remove_from_channel(clear_database, user1, user2, channel1):
    # Checking if msgid has been successfully removed from channel1 (being
    # removed by the message author)
    channel_join_v1(user2['token'], channel1)
    msgid = message_send_v1(user2['token'], channel1, 'This is a test')
    message_remove_v1(user2['token'], msgid['message_id'])
    assert channel_messages_v1(user2['token'], channel1, 0) == {'messages': [], 'start': 0, 'end': -1}

def test_message_remove_from_dm(clear_database, user1, user2, dm1, dm2):
    # Checking if msgid has been successfully removed from dm2 (being removed
    # by the owner of dm2)
    msgid = message_senddm_v1(user2['token'], dm2, 'Sending to DM')
    message_remove_v1(user2['token'], msgid['message_id'])
    assert dm_messages_v1(user2['token'], dm2, 0) == {'messages': [], 'start': 0, 'end': -1}

################################################################################
# message_share_v1 tests                                                       #
################################################################################

def test_message_share_invalid_uid(clear_database, user1, user2, channel1, channel2, message1):
    # Raises AccessError since token INVALID_ID does not exist
    with pytest.raises(AccessError):
        message_share_v1(INVALID_ID, message1, '', channel2, -1)
        
def test_message_share_invalid_channel(clear_database, user1, user2, channel1, message1):
    # Raises InputError since channel_id INVALID_ID does not exist
    with pytest.raises(InputError):
        message_share_v1(user2['token'], message1, '', INVALID_ID, -1)
        
def test_message_share_invalid_dm(clear_database, user1, user2, dm1, message2):
    # Raises InputError since dm_id INVALID_ID does not exist
    with pytest.raises(InputError):
        message_share_v1(user2['token'], message2, '', -1, INVALID_ID)
       
def test_message_share_invalid_messageid(clear_database, user1, user2, channel1, channel2, message1):
    # Raises InputError since og_message_id INVALID_ID does not exist
    with pytest.raises(InputError):
        message_share_v1(user2['token'], INVALID_ID, '', channel2, -1)
        
def test_message_share_removed_message(clear_database, user1, user2, channel1, channel2, message1):
    # Raises InputError since message1 has been deleted
    message_remove_v1(user1['token'], message1)
    with pytest.raises(InputError):
        message_share_v1(user2['token'], message1, '', channel2, -1)

def test_message_share_channel_accesserror(clear_database, user1, user2, channel1, channel2, message1):
    # Raises AccessError since user1 is not in channel2
    with pytest.raises(AccessError):
        message_share_v1(user1['token'], message1, '', channel2, -1)
     
def test_message_share_dm_accesserror(clear_database, user1, user2, channel1, dm1, message1):
    # Raises AccessError since user2 is not in dm1
    with pytest.raises(AccessError):
        message_share_v1(user2['token'], message1, '', -1, dm1)
    
def test_message_share_invalid_length(clear_database, user1, user2, channel1, channel2, message1):
    # Raises InputError since og_message + message > 1000 characters
    i = 0
    message = ''
    while i < 500:
        message += str(i)
        i += 1
    with pytest.raises(InputError):
        message_share_v1(user2['token'], message1, message, channel2, -1)
     
def test_message_share_to_channel_simple(clear_database, user1, user2, channel1, channel2, message1):
    # Tests sharing a single message to a channel
    assert channel_messages_v1(user2['token'], channel2, 0) == {'messages': [], 'start': 0, 'end': -1}
    message_share_v1(user2['token'], message1, '', channel2, -1)
    
    channel_messages = channel_messages_v1(user2['token'], channel2, 0)['messages']
    assert channel_messages[0]['message'] == 'Hello World'
    assert channel_messages[0]['u_id'] == user2['auth_user_id']
       
def test_message_share_to_dm_simple(clear_database, user1, channel1, dm1, message1):
    # Tests sharing a single message to a DM
    assert dm_messages_v1(user1['token'], dm1, 0) == {'messages': [], 'start': 0, 'end': -1}
    message_share_v1(user1['token'], message1, '', -1, dm1)

    dm_messages = dm_messages_v1(user1['token'], dm1, 0)['messages']
    assert dm_messages[0]['message'] == 'Hello World'
    assert dm_messages[0]['u_id'] == user1['auth_user_id']
    
def test_message_share_optional_msg(clear_database, user1, channel1, dm1, message1):
    # Tests adding an optional message to the original message, then sharing it
    # to a DM
    assert dm_messages_v1(user1['token'], dm1, 0) == {'messages': [], 'start': 0, 'end': -1}
    message_share_v1(user1['token'], message1, 'Hello Everyone', -1, dm1)

    dm_messages = dm_messages_v1(user1['token'], dm1, 0)['messages']
    assert dm_messages[0]['message'] == 'Hello World Hello Everyone'
    assert dm_messages[0]['u_id'] == user1['auth_user_id']

################################################################################
# message_senddm_v1 tests                                                      #
################################################################################

def test_message_senddm_invalid_uid(clear_database, user1, dm1):
    # Raises AccessError since token INVALID_ID does not exist
    with pytest.raises(AccessError):
        message_senddm_v1(INVALID_ID, dm1, 'Hello World')
        
def test_message_senddm_invalid_dm(clear_database, user1):
    # Raises InputError since dm_id INVALID_ID does not exist
    with pytest.raises(InputError):
        message_senddm_v1(user1['token'], INVALID_ID, 'Nice to meet you!')
        
def test_message_senddm_invalid_dm_2(clear_database, user1):
    # Raises InputError since dm_id 10 does not exist
    with pytest.raises(InputError):
        message_senddm_v1(user1['token'], 10, 'Hello World')
        
def test_message_senddm_uid_not_in_dm(clear_database, user1, dm1, user2):
    # Raises AccessError since user2 is not in dm1
    with pytest.raises(AccessError):
        message_senddm_v1(user2['token'], dm1, 'Hello World')
        
def test_message_senddm_invalid_messages(clear_database, user1, dm1):
    # Raises InputError since message > 1000 characters
    i = 0
    message = ''
    while i < 500:
        message += str(i)
        i += 1
    with pytest.raises(InputError):
        message_senddm_v1(user1['token'], dm1, message)
            
def test_message_senddm_empty_message(clear_database, user1, dm1):
    # Assuming that function will not send empty messages (or messages with just
    # whitespace) and instead raises InputError
    with pytest.raises(InputError):
        message_senddm_v1(user1['token'], dm1, '')
        
def test_message_senddm_empty_message2(clear_database, user1, dm1):
    # This test is same as above, but takes in a message filled with only
    # whitespace
    with pytest.raises(InputError):
        message_senddm_v1(user1['token'], dm1, '          ')
        
def test_message_senddm_single_message(clear_database, user1, dm1):
    # Tests sending a single message to DM
    msgid = message_senddm_v1(user1['token'], dm1, 'Hello World')
    
    dm_messages = dm_messages_v1(user1['token'], dm1, 0)['messages']
    assert len(dm_messages) == 1
    assert dm_messages[0]['message_id'] == msgid['message_id']
    assert dm_messages[0]['u_id'] == user1['auth_user_id']
    assert dm_messages[0]['message'] == 'Hello World'

################################################################################
# message_react_v1 tests                                                       #
################################################################################

def test_message_react_invalid_token(clear_database, user1, channel1, message1):
    with pytest.raises(AccessError):
        message_react_v1(INVALID_ID, message1, REACT_ID)

def test_message_react_invalid_message_id(clear_database, user1, channel1, message1):
    with pytest.raises(InputError):
        message_react_v1(user1['token'], INVALID_ID, REACT_ID)

def test_message_react_invalid_react_id(clear_database, user1, channel1, message1):
    with pytest.raises(InputError):
        message_react_v1(user1['token'], message1, INVALID_ID)

def test_message_has_already_reacted(clear_database, user1, channel1, message1):
    message_react_v1(user1['token'], channel1, REACT_ID)
    with pytest.raises(InputError):
        message_react_v1(user1['token'], message1, REACT_ID)

def test_message_react_user_not_in_channel(clear_database, user1, user2, channel1, message1):
    with pytest.raises(AccessError):
        message_react_v1(user2['token'], message1, REACT_ID)   

def test_message_react_user_not_in_dm(clear_database, user1, user2, dm1, message2):
    with pytest.raises(AccessError):
        message_react_v1(user2['token'], message2, REACT_ID)

def test_message_react_valid_inputs_in_channel(clear_database, user1, channel1, message1):
    message_react_v1(user1['token'], channel1, REACT_ID)
    channel_messages = channel_messages_v1(user1['token'], channel1, 0)
    message = channel_messages['messages'][0]
    assert message['message_id'] == 1
    assert message['u_id'] == 1
    assert message['message'] == 'Hello World'
    assert message['reacts'][0]['react_id'] == 1
    assert message['reacts'][0]['u_ids'] == [1]
    assert message['reacts'][0]['is_this_user_reacted'] == True

def test_message_react_valid_inputs_in_dm(clear_database, user1, channel1, dm1, message1, message2):
    message_react_v1(user1['token'], message2, REACT_ID)
    dm_messages = dm_messages_v1(user1['token'], dm1, 0)
    message = dm_messages['messages'][0]
    assert message['message_id'] == 2
    assert message['u_id'] == 1
    assert message['message'] == 'Hello There'
    assert message['reacts'][0]['react_id'] == 1
    assert message['reacts'][0]['u_ids'] == [1]
    assert message['reacts'][0]['is_this_user_reacted'] == True

def test_message_react_multiple_reacts_in_channel(clear_database, user1, user2, user3, channel1, message1):
    channel_invite_v1(user1['token'], channel1, user2['auth_user_id'])
    channel_invite_v1(user1['token'], channel1, user3['auth_user_id'])
    message_react_v1(user1['token'], message1, REACT_ID)
    message_react_v1(user2['token'], message1, REACT_ID)
    channel_messages = channel_messages_v1(user3['token'], channel1, 0)
    message = channel_messages['messages'][0]
    assert message['message_id'] == 1
    assert message['u_id'] == 1
    assert message['message'] == 'Hello World'
    assert message['reacts'][0]['react_id'] == 1
    assert message['reacts'][0]['u_ids'] == [1,2]
    assert message['reacts'][0]['is_this_user_reacted'] == False

def test_message_react_multiple_reacts_in_dm(clear_database, user1, user2, user3, dm1, message2):
    dm_invite_v1(user1['token'], dm1, user2['auth_user_id'])
    dm_invite_v1(user1['token'], dm1, user3['auth_user_id'])
    message_react_v1(user1['token'], message2, REACT_ID)
    message_react_v1(user2['token'], message2, REACT_ID)
    dm_messages = dm_messages_v1(user3['token'], dm1, 0)
    message = dm_messages['messages'][0]
    assert message['message_id'] == 1
    assert message['u_id'] == 1
    assert message['message'] == 'Hello There'
    assert message['reacts'][0]['react_id'] == 1
    assert message['reacts'][0]['u_ids'] == [1,2]
    assert message['reacts'][0]['is_this_user_reacted'] == False

################################################################################
# message_unreact_v1 tests                                                     #
################################################################################

def test_message_unreact_invalid_token(clear_database, user1, channel1, message1):
    message_react_v1(user1['token'], message1, REACT_ID)
    with pytest.raises(AccessError):
        message_unreact_v1(INVALID_ID, message1, REACT_ID)

def test_message_unreact_invalid_message_id(clear_database, user1, channel1, message1):
    message_react_v1(user1['token'], message1, REACT_ID)
    with pytest.raises(InputError):
        message_unreact_v1(user1['token'], INVALID_ID, REACT_ID)

def test_message_unreact_invalid_react_id(clear_database, user1, channel1, message1):
    message_react_v1(user1['token'], message1, REACT_ID)
    with pytest.raises(InputError):
        message_unreact_v1(user1['token'], message1, INVALID_ID)

def test_message_unreact_no_reacts(clear_database, user1, channel1, message1):
    with pytest.raises(InputError):
        message_unreact_v1(user1['token'], message1, REACT_ID)

def test_message_has_already_unreacted(clear_database, user1, channel1, message1):
    message_react_v1(user1['token'], message1, REACT_ID)
    message_unreact_v1(user1['token'], channel1, REACT_ID)
    with pytest.raises(InputError):
        message_unreact_v1(user1['token'], message1, REACT_ID)

def test_message_unreact_user_not_in_channel(clear_database, user1, user2, channel1, message1):
    message_react_v1(user1['token'], message1, REACT_ID)
    channel_leave_v1(user1['token'], channel1)
    with pytest.raises(AccessError):
        message_unreact_v1(user1['token'], message1, REACT_ID)   

def test_message_unreact_user_not_in_dm(clear_database, user1, user2, dm1, message2):
    message_react_v1(user1['token'], message2, REACT_ID)
    dm_leave_v1(user1['token'], dm1)
    with pytest.raises(AccessError):
        message_unreact_v1(user1['token'], message2, REACT_ID)

def test_message_unreact_valid_inputs_in_channel(clear_database, user1, channel1, message1):
    message_react_v1(user1['token'], message1, REACT_ID)
    message_unreact_v1(user1['token'], message1, REACT_ID)
    channel_messages = channel_messages_v1(user1['token'], channel1, 0)
    message = channel_messages['messages'][0]
    assert message['message_id'] == 1
    assert message['u_id'] == 1
    assert message['message'] == 'Hello World'
    assert message['reacts'][0]['react_id'] == 1
    assert message['reacts'][0]['u_ids'] == []
    assert message['reacts'][0]['is_this_user_reacted'] == False

def test_message_unreact_valid_inputs_in_dm(clear_database, user1, channel1, dm1, message1, message2):
    message_react_v1(user1['token'], message2, REACT_ID)
    message_unreact_v1(user1['token'], message2, REACT_ID)
    dm_messages = dm_messages_v1(user1['token'], dm1, 0)
    message = dm_messages['messages'][0]
    assert message['message_id'] == 2
    assert message['u_id'] == 1
    assert message['message'] == 'Hello There'
    assert message['reacts'][0]['react_id'] == 1
    assert message['reacts'][0]['u_ids'] == []
    assert message['reacts'][0]['is_this_user_reacted'] == False

def test_message_unreact_multiple_unreacts_in_channel(clear_database, user1, user2, user3, channel1, message1):
    channel_invite_v1(user1['token'], channel1, user2['auth_user_id'])
    channel_invite_v1(user1['token'], channel1, user3['auth_user_id'])
    message_react_v1(user1['token'], message1, REACT_ID)
    message_react_v1(user2['token'], message1, REACT_ID)
    message_react_v1(user3['token'], message1, REACT_ID)
    message_unreact_v1(user1['token'], message1, REACT_ID)
    message_unreact_v1(user2['token'], message1, REACT_ID)
    channel_messages = channel_messages_v1(user3['token'], channel1, 0)
    message = channel_messages['messages'][0]
    assert message['message_id'] == 1
    assert message['u_id'] == 1
    assert message['message'] == 'Hello World'
    assert message['reacts'][0]['react_id'] == 1
    assert message['reacts'][0]['u_ids'] == [3]
    assert message['reacts'][0]['is_this_user_reacted'] == True

def test_message_unreact_multiple_reacts_in_dm(clear_database, user1, user2, user3, dm1, message2):
    dm_invite_v1(user1['token'], dm1, user2['auth_user_id'])
    dm_invite_v1(user1['token'], dm1, user3['auth_user_id'])
    message_react_v1(user1['token'], message2, REACT_ID)
    message_react_v1(user2['token'], message2, REACT_ID)
    message_react_v1(user3['token'], message2, REACT_ID)
    message_unreact_v1(user1['token'], message2, REACT_ID)
    message_unreact_v1(user2['token'], message2, REACT_ID)
    dm_messages = dm_messages_v1(user3['token'], dm1, 0)
    message = dm_messages['messages'][0]
    assert message['message_id'] == 1
    assert message['u_id'] == 1
    assert message['message'] == 'Hello There'
    assert message['reacts'][0]['react_id'] == 1
    assert message['reacts'][0]['u_ids'] == [3]
    assert message['reacts'][0]['is_this_user_reacted'] == True

################################################################################
# message_pin_v1 tests                                                         #
################################################################################

def test_message_pin_invalid_token(clear_database, user1, channel1, message1):
    with pytest.raises(AccessError):
        message_pin_v1(INVALID_ID, message1)

def test_message_pin_invalid_message_id(clear_database, user1, channel1, message1):
    with pytest.raises(InputError):
        message_pin_v1(user1['token'], INVALID_ID)

def test_message_same_user_pin_again(clear_database, user1, channel1, message1):
    message_pin_v1(user1['token'], message1)
    with pytest.raises(InputError):
        message_pin_v1(user1['token'], message1)

def test_message_channel_member_pin(clear_database, user1, user2, channel1, message1):
    channel_invite_v1(user1['token'], channel1, user2['auth_user_id'])
    with pytest.raises(AccessError):
        message_pin_v1(user2['token'], message1)

def test_message_diff_user_pin_again(clear_database, user1, user2, channel1, message1):
    message_pin_v1(user1['token'], message1)
    channel_invite_v1(user1['token'], channel1, user2['auth_user_id'])
    channel_addowner_v1(user1['token'], channel1, user2['auth_user_id'])
    with pytest.raises(InputError):
        message_pin_v1(user2['token'], message1)

def test_message_pin_user_not_in_channel(clear_database, user1, user2, channel1, message1):
    with pytest.raises(AccessError):
        message_pin_v1(user2['token'], message1)   

def test_message_dm_member_pin(clear_database, user1, user2, dm1, message2):
    dm_invite_v1(user1['token'], dm1, user2['auth_user_id'])
    with pytest.raises(AccessError):
        message_pin_v1(user2['token'], message2)

def test_message_pin_user_not_in_dm(clear_database, user1, user2, dm1, message2):
    with pytest.raises(AccessError):
        message_pin_v1(user2['token'], message2)

def test_message_pin_valid_inputs_in_channel(clear_database, user1, channel1, message1):
    message_pin_v1(user1['token'], message1)
    channel_messages = channel_messages_v1(user1['token'], channel1, 0)
    message = channel_messages['messages'][0]
    assert message['message_id'] == 1
    assert message['u_id'] == 1
    assert message['message'] == 'Hello World'
    assert message['is_pinned'] == True

def test_message_pin_valid_inputs_in_dm(clear_database, user1, channel1, dm1, message1, message2):
    message_pin_v1(user1['token'], message2)
    dm_messages = dm_messages_v1(user1['token'], dm1, 0)
    message = dm_messages['messages'][0]
    assert message['message_id'] == 2
    assert message['u_id'] == 1
    assert message['message'] == 'Hello There'
    assert message['is_pinned'] == True

def test_message_pin_another_user_in_channel(clear_database, user1, user2, channel1, message1):
    channel_invite_v1(user1['token'], channel1, user2['auth_user_id'])
    channel_addowner_v1(user1['token'], channel1, user2['auth_user_id'])
    message_pin_v1(user2['token'], message1)
    channel_messages = channel_messages_v1(user1['token'], channel1, 0)
    message = channel_messages['messages'][0]
    assert message['message_id'] == 1
    assert message['u_id'] == 1
    assert message['message'] == 'Hello World'
    assert message['is_pinned'] == True

################################################################################
# message_unpin_v1 tests                                                       #
################################################################################

def test_message_unpin_invalid_token(clear_database, user1, channel1, message1):
    message_pin_v1(user1['token'], message1)
    with pytest.raises(AccessError):
        message_unpin_v1(INVALID_ID, message1)

def test_message_unpin_invalid_message_id(clear_database, user1, channel1, message1):
    message_pin_v1(user1['token'], message1)
    with pytest.raises(InputError):
        message_unpin_v1(user1['token'], INVALID_ID)

def test_message_same_user_unpin_again(clear_database, user1, channel1, message1):
    message_pin_v1(user1['token'], message1)
    message_unpin_v1(user1['token'], message1)
    with pytest.raises(InputError):
        message_unpin_v1(user1['token'], message1)

def test_message_diff_user_unpin_again(clear_database, user1, user2, channel1, message1):
    message_pin_v1(user1['token'], message1)
    channel_invite_v1(user1['token'], channel1, user2['auth_user_id'])
    channel_addowner_v1(user1['token'], channel1, user2['auth_user_id'])
    message_unpin_v1(user1['token'], message1)
    with pytest.raises(InputError):
        message_unpin_v1(user2['token'], message1)

def test_message_unpin_user_not_in_channel(clear_database, user1, user2, channel1, message1):
    message_pin_v1(user1['token'], message1)
    with pytest.raises(AccessError):
        message_unpin_v1(user2['token'], message1)   

def test_message_channel_member_unpin(clear_database, user1, user2, channel1, message1):
    channel_invite_v1(user1['token'], channel1, user2['auth_user_id'])
    with pytest.raises(AccessError):
        message_pin_v1(user2['token'], message1)

def test_message_unpin_user_not_in_dm(clear_database, user1, user2, dm1, message2):
    message_pin_v1(user1['token'], message2)
    with pytest.raises(AccessError):
        message_unpin_v1(user2['token'], message2)

def test_message_dm_member_unpin(clear_database, user1, user2, dm1, message2):
    message_pin_v1(user1['token'], message2)
    dm_invite_v1(user1['token'], dm1, user2['auth_user_id'])
    with pytest.raises(AccessError):
        message_pin_v1(user2['token'], message2)

def test_message_unpin_valid_inputs_in_channel(clear_database, user1, channel1, message1):
    message_pin_v1(user1['token'], message1)
    message_unpin_v1(user1['token'], message1)
    channel_messages = channel_messages_v1(user1['token'], channel1, 0)
    message = channel_messages['messages'][0]
    assert message['message_id'] == 1
    assert message['u_id'] == 1
    assert message['message'] == 'Hello World'
    assert message['is_pinned'] == False

def test_message_unpin_valid_inputs_in_dm(clear_database, user1, channel1, dm1, message1, message2):
    message_pin_v1(user1['token'], message2)
    message_unpin_v1(user1['token'], message2)
    dm_messages = dm_messages_v1(user1['token'], dm1, 0)
    message = dm_messages['messages'][0]
    assert message['message_id'] == 2
    assert message['u_id'] == 1
    assert message['message'] == 'Hello There'
    assert message['is_pinned'] == False

def test_message_unpin_another_user_in_channel(clear_database, user1, user2, channel1, message1):
    channel_invite_v1(user1['token'], channel1, user2['auth_user_id'])
    channel_addowner_v1(user1['token'], channel1, user2['auth_user_id'])
    message_pin_v1(user1['token'], message1)
    message_unpin_v1(user2['token'], message1)
    channel_messages = channel_messages_v1(user1['token'], channel1, 0)
    message = channel_messages['messages'][0]
    assert message['message_id'] == 1
    assert message['u_id'] == 1
    assert message['message'] == 'Hello World'
    assert message['is_pinned'] == False

################################################################################
# message_sendlater_v1 tests                                                   #
################################################################################

def test_message_sendlater_invalid_token(clear_database, user1, channel1, message_time):
    # Raises AccessError since token INVALID_ID does not exist
    with pytest.raises(AccessError):
        message_sendlater_v1(INVALID_ID, channel1, 'Hello World', message_time)
        
def test_message_sendlater_invalid_channel(clear_database, user1, message_time):
    # Raises InputError since channel_id INVALID_ID does not exist
    with pytest.raises(InputError):
        message_sendlater_v1(user1['token'], INVALID_ID, 'Nice to meet you!', message_time)

def test_message_sendlater_user_not_in_channel(clear_database, user1, channel1, user2, channel2, message_time):
    # Raises AccessError since user2 is not in channel1
    with pytest.raises(AccessError):
        message_sendlater_v1(user2['token'], channel1, 'Hello World', message_time)

def test_message_sendlater_invalid_message(clear_database, user1, channel1, message_time):
    # Raises InputError since message > 1000 characters
    i = 0
    message = ''
    while i < 500:
        message += str(i)
        i += 1
    with pytest.raises(InputError):
        message_sendlater_v1(user1['token'], channel1, message, message_time)

def test_message_sendlater_empty_message(clear_database, user1, channel1, message_time):
    # Assuming that function will not add empty messages (or messages with just
    # whitespace) and instead raises InputError
    with pytest.raises(InputError):
        message_sendlater_v1(user1['token'], channel1, '', message_time)

def test_message_sendlater_past_time(clear_database, user1, channel1):
    # Raises InputError since the time_sent argument is in the past
    time = datetime.now() - timedelta(0, 3)
    send_time = int(time.timestamp())
    with pytest.raises(InputError):
        message_sendlater_v1(user1['token'], channel1, 'Hi Channel1!', send_time)

def check_before_send_time(token, channel_id, dm_id):
    if dm_id == -1:
        chan_msg = channel_messages_v1(token, channel_id, 0)
        assert chan_msg == {'messages': [], 'start': 0, 'end': -1}
    elif channel_id == -1:
        dm_msg = dm_messages_v1(token, dm_id, 0)
        assert dm_msg == {'messages': [], 'start': 0, 'end': -1}        

def test_message_sendlater_valid_message(clear_database, user1, channel1):
    # Testing a valid case where a message is set to send 5 seconds later
    send_time = datetime.now() + timedelta(0, 5)
    send_time = int(send_time.timestamp())

    # Checks if message is there after 4 seconds, should confirm that it has
    # not yet been sent
    check_send = threading.Timer(4, check_before_send_time, args=(user1['token'], channel1, -1))
    check_send.start()
    message = message_sendlater_v1(user1['token'], channel1, 'Hi everyone!', send_time)
    chan_msg = channel_messages_v1(user1['token'], channel1, 0)['messages']
    assert len(chan_msg) == 1
    assert chan_msg[0]['message'] == 'Hi everyone!'
    assert chan_msg[0]['message_id'] == message['message_id']
    assert chan_msg[0]['u_id'] == user1['auth_user_id']
    time_diff = chan_msg[0]['time_created'] - send_time
    assert (time_diff >= -1 and time_diff <= 1)

def check_message_sent(user, channel_id, dm_id, message):
    if channel_id != -1:
        chan_msg = channel_messages_v1(user['token'], channel_id, 0)['messages']
        assert len(chan_msg) == 1
        assert chan_msg[0]['message'] == message
        assert chan_msg[0]['u_id'] == user['auth_user_id']
        assert chan_msg[0]['message_id'] == 1
    elif dm_id != -1:
        dm_msg = dm_messages_v1(user['token'], dm_id, 0)['messages']
        assert len(dm_msg) == 1
        assert dm_msg[0]['message'] == message
        assert dm_msg[0]['u_id'] == user['auth_user_id']
        assert dm_msg[0]['message_id'] == 1

def test_message_sendlater_valid_multiple(clear_database, user1, user2, channel1):
    # Sending two messages that are going to be sent several seconds apart
    channel_join_v1(user2['token'], channel1)
    send_time_1 = datetime.now() + timedelta(0, 2)
    send_time_1 = int(send_time_1.timestamp())
    send_time_2 = datetime.now() + timedelta(0, 5)
    send_time_2 = int(send_time_2.timestamp())
    # This thread checks messages sent 3 seconds from now
    check_send = threading.Timer(3, check_message_sent, args=(user2, channel1, -1, 'This should be first'))
    check_send.start()
    # This thread sends a message 2 seconds from now (so previous thread should
    # be able to confirm it has been sent)
    send_first = threading.Thread(target=message_sendlater_v1, args=(user2['token'], channel1, 'This should be first', send_time_1))
    send_first.start()
    # Checks for messages sent right now (should be empty)
    chan_msg = channel_messages_v1(user1['token'], channel1, 0)
    assert chan_msg == {'messages': [], 'start': 0, 'end': -1}
    # Sends a message 5 seconds from now, should be most recent msg in channel
    msg = message_sendlater_v1(user1['token'], channel1, 'Hi everyone!', send_time_2)
    chan_msg = channel_messages_v1(user1['token'], channel1, 0)['messages']
    assert len(chan_msg) == 2
    assert chan_msg[0]['message'] == 'Hi everyone!'
    assert chan_msg[0]['u_id'] == user1['auth_user_id']
    assert chan_msg[0]['message_id'] == msg['message_id']
    assert chan_msg[1]['message'] == 'This should be first'
    assert chan_msg[1]['u_id'] == user2['auth_user_id']
    assert chan_msg[1]['message_id'] == 1

def test_message_sendlater_and_send(clear_database, user1, user2, channel1):
    # Testing message_send and message_sendlater alongside each other
    channel_join_v1(user2['token'], channel1)
    send_time = datetime.now() + timedelta(0, 5)
    send_time = int(send_time.timestamp())
    # Thread sends a message 5 seconds from now
    send_later = threading.Thread(target=message_sendlater_v1, args=(user2['token'], channel1, 'This is last', send_time))
    send_later.start()
    # Sends a message immediately 
    msg = message_send_v1(user1['token'], channel1, 'This is first')
    chan_msg = channel_messages_v1(user1['token'], channel1, 0)['messages']
    assert len(chan_msg) == 1
    assert chan_msg[0]['message'] == 'This is first'
    assert chan_msg[0]['u_id'] == user1['auth_user_id']
    assert chan_msg[0]['message_id'] == msg['message_id']
    # Checks for messages 4 seconds from now (should only show 1 message)
    check_send = threading.Timer(4, check_message_sent, args=(user1, channel1, -1, 'This is first'))
    check_send.start()
    # Sleeping for 6 seconds to allow send_later thread to finish
    time.sleep(6)
    chan_msg = channel_messages_v1(user1['token'], channel1, 0)['messages']
    assert len(chan_msg) == 2
    assert chan_msg[0]['message'] == 'This is last'
    assert chan_msg[0]['u_id'] == user2['auth_user_id']
    assert chan_msg[0]['message_id'] == 2
    assert chan_msg[1]['message'] == 'This is first'
    assert chan_msg[1]['u_id'] == user1['auth_user_id']
    assert chan_msg[1]['message_id'] == msg['message_id']

################################################################################
# message_sendlaterdm_v1 tests                                                 #
################################################################################

def test_message_sendlaterdm_invalid_token(clear_database, user1, dm1, message_time):
    # Raises AccessError since token INVALID_ID does not exist
    with pytest.raises(AccessError):
        message_sendlaterdm_v1(INVALID_ID, dm1, 'Hello World', message_time)
        
def test_message_sendlaterdm_invalid_dm(clear_database, user1, message_time):
    # Raises InputError since dm_id INVALID_ID does not exist
    with pytest.raises(InputError):
        message_sendlaterdm_v1(user1['token'], INVALID_ID, 'Nice to meet you!', message_time)

def test_message_sendlaterdm_user_not_in_dm(clear_database, user1, dm1, user2, dm2, message_time):
    # Raises AccessError since user2 is not in dm1
    with pytest.raises(AccessError):
        message_sendlaterdm_v1(user2['token'], dm1, 'Hello World', message_time)

def test_message_sendlaterdm_invalid_message(clear_database, user1, dm1, message_time):
    # Raises InputError since message > 1000 characters
    i = 0
    message = ''
    while i < 500:
        message += str(i)
        i += 1
    with pytest.raises(InputError):
        message_sendlaterdm_v1(user1['token'], dm1, message, message_time)

def test_message_sendlaterdm_empty_message(clear_database, user1, dm1, message_time):
    # Assuming that function will not add empty messages (or messages with just
    # whitespace) and instead raises InputError
    with pytest.raises(InputError):
        message_sendlaterdm_v1(user1['token'], dm1, '      ', message_time)

def test_message_sendlaterdm_past_time(clear_database, user1, dm1):
    # Raises InputError since the time_sent argument is in the past
    time = datetime.now() - timedelta(0, 3)
    send_time = int(time.timestamp())
    with pytest.raises(InputError):
        message_sendlaterdm_v1(user1['token'], dm1, 'Hi DM!', send_time)

def test_message_sendlaterdm_valid_message(clear_database, user1, dm1):
    # Testing a valid case where a message is set to send 5 seconds later
    send_time = datetime.now() + timedelta(0, 5)
    send_time = int(send_time.timestamp())

    check_send = threading.Timer(4, check_before_send_time, args=(user1['token'], -1, dm1))
    check_send.start()
    message = message_sendlaterdm_v1(user1['token'], dm1, 'Hello everyone!', send_time)
    dm_msg = dm_messages_v1(user1['token'], dm1, 0)['messages']
    assert len(dm_msg) == 1
    assert dm_msg[0]['message'] == 'Hello everyone!'
    assert dm_msg[0]['message_id'] == message['message_id']
    assert dm_msg[0]['u_id'] == user1['auth_user_id']
    time_diff = dm_msg[0]['time_created'] - send_time
    assert (time_diff >= -1 and time_diff <= 1)

def test_message_sendlaterdm_valid_multiple(clear_database, user1, user2, dm1):
    # Sending two messages that are going to be sent several seconds apart
    dm_invite_v1(user1['token'], dm1, user2['auth_user_id'])
    send_time_1 = datetime.now() + timedelta(0, 2)
    send_time_1 = int(send_time_1.timestamp())
    send_time_2 = datetime.now() + timedelta(0, 5)
    send_time_2 = int(send_time_2.timestamp())
    # This thread checks messages sent 3 seconds from now
    check_send = threading.Timer(3, check_message_sent, args=(user2, -1, dm1, 'This should be first'))
    check_send.start()
    # This thread sends a message 5 seconds from now (previous thread will not
    # see that it has been sent)
    send_last = threading.Thread(target=message_sendlaterdm_v1, args=(user1['token'], dm1, 'This should be second', send_time_2))
    send_last.start()
    # Checks for messages sent right now (should be empty)
    dm_msg = dm_messages_v1(user1['token'], dm1, 0)
    assert dm_msg == {'messages': [], 'start': 0, 'end': -1}
    # Sends a message 2 seconds from now, should be first message in DM
    msg = message_sendlaterdm_v1(user2['token'], dm1, 'This should be first', send_time_1)
    # Sleeping for 4 seconds to wait for the send_last thread to finish
    time.sleep(4)
    dm_msg = dm_messages_v1(user1['token'], dm1, 0)['messages']
    assert len(dm_msg) == 2
    assert dm_msg[0]['message'] == 'This should be second'
    assert dm_msg[0]['u_id'] == user1['auth_user_id']
    assert dm_msg[0]['message_id'] == 2
    assert dm_msg[1]['message'] == 'This should be first'
    assert dm_msg[1]['u_id'] == user2['auth_user_id']
    assert dm_msg[1]['message_id'] == msg['message_id']

def test_message_sendlaterdm_and_senddm(clear_database, user1, user2, dm1):
    # Testing message_senddm and message_sendlaterdm alongside each other
    dm_invite_v1(user1['token'], dm1, user2['auth_user_id'])
    send_time = datetime.now() + timedelta(0, 5)
    send_time = int(send_time.timestamp())

    # Thread sends a message 6 seconds from now (using senddm)
    send_last = threading.Timer(6, message_senddm_v1, args=(user2['token'], dm1, 'This is last'))
    send_last.start()
    # Thread sends a message 5 seconds from now (using sendlaterdm)
    send_first = threading.Thread(target=message_sendlaterdm_v1, args=(user1['token'], dm1, 'This is first', send_time))
    send_first.start()
    # Checks for messages in DM right now (should be none)
    dm_msg = dm_messages_v1(user1['token'], dm1, 0)
    assert dm_msg == {'messages': [], 'start': 0, 'end': -1}
    # Checks for messages 4 seconds from now (should show no messages)
    check_send = threading.Timer(4, check_before_send_time, args=(user1['token'], -1, dm1))
    check_send.start()
    # Sleeping for 7 seconds to allow send_first and send_last threads to finish
    time.sleep(7)
    dm_msg = dm_messages_v1(user1['token'], dm1, 0)['messages']
    assert len(dm_msg) == 2
    assert dm_msg[0]['message'] == 'This is last'
    assert dm_msg[0]['u_id'] == user2['auth_user_id']
    assert dm_msg[0]['message_id'] == 2
    assert dm_msg[1]['message'] == 'This is first'
    assert dm_msg[1]['u_id'] == user1['auth_user_id']
    assert dm_msg[1]['message_id'] == 1

