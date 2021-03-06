import pytest

from src.channel import channel_messages_v1, channel_join_v1, channel_details_v1
from src.error import InputError, AccessError 
from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.message import message_send_v1
from src.other import clear_v1

@pytest.fixture
def user1():
    new_user1 = auth_register_v1('johnsmith@gmail.com', 'goodpass', 'John', 'Smith')    
    return new_user1['auth_user_id']
    
@pytest.fixture
def user2():
    new_user2 = auth_register_v1('philt@gmail.com', 'badpass', 'Phil', 'Tran')
    return new_user2['auth_user_id']
    
@pytest.fixture
def user3():
    new_user3 = auth_register_v1('person@gmail.com', 'helloworld', 'First', 'Name')
    return new_user3['auth_user_id']
  
@pytest.fixture
def channel1(user1):   
    # This channel is public, created by user1
    new_chan1 = channels_create_v1(user1, 'channel1', True) 
    return new_chan1['channel_id']

@pytest.fixture    
def channel2(user2):
    # This channel is private, created by user2
    new_chan2 = channels_create_v1(user2, 'channel2', False) 
    return new_chan2['channel_id']

@pytest.fixture
def supply_message1(user1, channel1):
    # Sends a single message to channel1
    message_send_v1(user1, channel1, 'A new message')

@pytest.fixture    
def supply_multi1(user1, channel1, supply_message1):
    # Sends 55 messages to channel1, the messages are just numbers
    i = 1
    while i <= 55:
        message_send_v1(user1, channel1, f"{i}")
        i += 1
        
@pytest.fixture
def clear_database():
    clear_v1()
   
                          
################################################################################
# channel_messages_v1 tests
################################################################################
    
def test_channel_messages_invalid_channel(clear_database, user1, channel1):
    # Raises InputError since channel_id 123456 does not exist
    with pytest.raises(InputError):
        channel_messages_v1(user1, 123456, 0) 
        
        
def test_channel_messages_invalid_start(clear_database, user2, channel2):
    # Raises InputError since start is greater than num messages in channel2
    # (there are no messages in channel2)
    with pytest.raises(InputError):
        channel_messages_v1(user2, channel2, 10) 
    

def test_channel_messages_authid_not_member(clear_database, user1, channel1, user2):
    # Raises AccessError since user2 is not a member of channel1
    with pytest.raises(AccessError):
        channel_messages_v1(user2, channel1, 0) 
        
               
def test_channel_messages_invalid_authid(clear_database, user1, channel1):
    # Raises AccessError since u_id 123456 does not exist
    with pytest.raises(AccessError):
        channel_messages_v1(123456, channel1, 0) 
        
        
def test_channel_messages_valid_single(clear_database, user1, channel1, supply_message1):
    # Tests for a single message in channel1
    message_detail = channel_messages_v1(user1, channel1, 0)
    
    # Checking the message dictionary to see if message has been appended
    assert message_detail['messages'][0]['message_id'] == 1
    assert message_detail['messages'][0]['u_id'] == user1
    assert message_detail['messages'][0]['message'] == 'A new message'
    assert message_detail['start'] == 0
    assert message_detail['end'] == -1
    
   
def test_channel_messages_multiple(clear_database, user1, channel1, supply_multi1):
    # Testing for multiple messages, and non-zero start value
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
# channel_join_v1 tests
################################################################################
    
def test_channel_join_invalid_authid(clear_database, user1, channel1):
    # Raises AccessError since auth_user_id 123456 does not exist
    with pytest.raises(AccessError):
        channel_join_v1(123456, channel1) 
                
    
def test_channel_join_invalid_channel(clear_database, user1, channel1):
    # Raises InputError since channel_id 2 does not exist
    with pytest.raises(InputError):
        channel_join_v1(user1, 2) 
        
        
def test_channel_join_private_channel(clear_database, user2, channel2, user3):        
    # Raises AccessError since user3 is a member attempting to enter a private
    # channel
    with pytest.raises(AccessError):    
        channel_join_v1(user3, channel2) 
        
        
def test_channel_join_valid(clear_database, user1, channel1, user2):
    # Testing if a single member can join a public channel
    channel_join_v1(user2, channel1)
    
    channels = channel_details_v1(user1, channel1)
    assert len(channels['all_members']) == 2
    assert channels['all_members'][0]['u_id'] == user1
    assert channels['all_members'][1]['u_id'] == user2    
    
    
def test_channel_join_valid_multi(clear_database, user1, user2, user3, channel1):
    # Testing if multiple members can join a public channel
    channel_join_v1(user2, channel1)
    channel_join_v1(user3, channel1)

    channels = channel_details_v1(user1, channel1)
    assert len(channels['all_members']) == 3
    assert channels['all_members'][0]['u_id'] == user1
    assert channels['all_members'][1]['u_id'] == user2
    assert channels['all_members'][2]['u_id'] == user3
    

def test_channel_join_global_private(clear_database, user1, user2, channel2):
    # Test to see if a global member (user1), gets added as a member and owner
    # of channel2
    channel_join_v1(user1, channel2)
    
    channels = channel_details_v1(user2, channel2)
    # Checking if user1 has been added into the members and owners list 
    assert len(channels['all_members']) == 2
    assert len(channels['owner_members']) == 2
    assert channels['all_members'][0]['u_id'] == user2
    assert channels['all_members'][1]['u_id'] == user1
    assert channels['owner_members'][0]['u_id'] == user2
    assert channels['owner_members'][1]['u_id'] == user1
        
