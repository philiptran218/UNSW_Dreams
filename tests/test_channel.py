import pytest
from src.error import InputError, AccessError
from src.auth import auth_register_v1
from src.channels import channels_create_v1, channels_listall_v1, channels_list_v1
from src.channel import channel_invite_v1, channel_details_v1, channel_messages_v1, channel_join_v1
from src.other import clear_v1
from src.message import message_send_v1
from src.helper import is_valid_channelid
from src.database import data

INVALID_VALUE = -1

################################################################################
# channel_invites_v1 tests                                                     #
################################################################################

@pytest.fixture
def user_1():
    user = auth_register_v1("johnsmith@gmail.com", "password", "John", "Smith")
    return user['auth_user_id']

@pytest.fixture
def user_2():
    user = auth_register_v1("terrynguyen@gmail.com", "password", "Terry", "Nguyen")
    return user['auth_user_id']

@pytest.fixture
def public_channel(user_1):
    channel = channels_create_v1(user_1, "John's Channel", True)
    return channel['channel_id']
    
@pytest.fixture
def private_channel(user_2):
    channel = channels_create_v1(user_2, "Terry's Channel", False)
    return channel['channel_id']

@pytest.fixture
def clear_data():
    clear_v1()

def test_invite_invalid_channel(clear_data, user_1, user_2):
    with pytest.raises(InputError):
        channel_invite_v1(user_1, INVALID_VALUE, user_2)

def test_invite_invalid_uid(clear_data, user_1, user_2, public_channel):
    with pytest.raises(InputError):
        channel_invite_v1(user_1, public_channel, INVALID_VALUE)

def test_invite_invalid_auth_id(clear_data, user_1, user_2, public_channel):
    with pytest.raises(AccessError):
        channel_invite_v1(user_2, public_channel, user_1)

def test_invite_duplicate_uid(clear_data, user_1, user_2, public_channel):
    channel_invite_v1(user_1, public_channel, user_2)
    channel_invite_v1(user_1, public_channel, user_2)

def test_invite_valid_inputs(clear_data, user_1, user_2, public_channel):
    channel_invite_v1(user_1, public_channel, user_2)
    channel_members = channel_details_v1(user_1, public_channel)
    member_found = False
    for members in channel_members['all_members']:
        print(members)
        if members['u_id'] == user_2:
            member_found = True
            print(member_found)
    assert member_found == True

################################################################################
# channel_details_v1 tests                                                     #
################################################################################

def expected_output_details():
    John_Channel_Details = {
        'name': "John's Channel",
        'owner_members': [
            {
                'u_id': 1,
                'name_first': 'John',
                'name_last': 'Smith',
                'email': 'johnsmith@gmail.com',
                'handle_str': 'johnsmith',
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'name_first': 'John',
                'name_last': 'Smith',
                'email': 'johnsmith@gmail.com',
                'handle_str': 'johnsmith',
            },
            {
                'u_id': 2,
                'name_first': 'Terry',
                'name_last': 'Nguyen',
                'email': 'terrynguyen@gmail.com',
                'handle_str': 'terrynguyen',
            }
        ]
    }

    return John_Channel_Details

def test_details_invalid_channel(clear_data, user_1):
    with pytest.raises(InputError):
        channel_details_v1(user_1, INVALID_VALUE)

def test_details_invalid_auth_id(clear_data, user_2, public_channel):
    with pytest.raises(AccessError):
        channel_details_v1(user_2, public_channel)

def test_details_valid_inputs(clear_data, user_1, user_2, public_channel):
    channel_invite_v1(user_1, public_channel, user_2)
    assert channel_details_v1(user_1, public_channel) == expected_output_details()

################################################################################
# channel_messages_v1 tests                                                    #
################################################################################
     
def test_channel_messages_invalid_channel(clear_data, user_1, public_channel):
    # Raises InputError since channel_id 123456 does not exist
    with pytest.raises(InputError):
        channel_messages_v1(user_1, 123456, 0) 
        
        
def test_channel_messages_invalid_start(clear_data, user_1, public_channel):
    # Raises InputError since start is greater than num messages in channel
    # (there are no messages in channel)
    with pytest.raises(InputError):
        channel_messages_v1(user_1, public_channel, 10) 
    

def test_channel_messages_authid_not_member(clear_data, user_1, public_channel, user_2):
    # Raises AccessError since user_2 is not a member of channel
    with pytest.raises(AccessError):
        channel_messages_v1(user_2, public_channel, 0) 
        
               
def test_channel_messages_invalid_authid(clear_data, user_1, public_channel):
    # Raises AccessError since u_id 123456 does not exist
    with pytest.raises(AccessError):
        channel_messages_v1(123456, public_channel, 0) 

# This tests requires message_send_v1 to be implemented.   
'''        
def test_channel_messages_valid_single(clear_data, user_1, public_channel):
    # Tests for a single message in channel
    message_send_v1(user_1, public_channel, 'A new message')
    message_detail = channel_messages_v1(user_1, public_channel, 0)
    
    # Checking the message dictionary to see if message has been appended
    assert message_detail['messages'][0]['message_id'] == 1
    assert message_detail['messages'][0]['u_id'] == user_1
    assert message_detail['messages'][0]['message'] == 'A new message'
    assert message_detail['start'] == 0
    assert message_detail['end'] == -1
''' 

# This tests requires message_send_v1 to be implemented.  
'''     
def test_channel_messages_multiple(clear_data, user_1, public_channel):
    # Testing for multiple messages, and non-zero start value 
    # Sends 55 messages to channel, the messages are just numbers as strings
    i = 1
    while i <= 55:
        message_send_v1(user_1, public_channel, f"{i}")
        i += 1
    
    message_detail = channel_messages_v1(user_1, public_channel, 2)
   
    # Checking that the messages have been appended correctly
    i = 53
    j = 0
    while i >= 4:
        assert message_detail['messages'][j]['message_id'] == i
        assert message_detail['messages'][j]['u_id'] == user_1
        assert message_detail['messages'][j]['message'] == str(i)
        i -= 1
        j += 1 
    assert message_detail['start'] == 2
    assert message_detail['end'] == 52
''' 
    
################################################################################
# channel_join_v1 tests                                                        #
################################################################################
    
def test_channel_join_invalid_authid(clear_data, user_1, public_channel):
    # Raises AccessError since auth_user_id 123456 does not exist
    with pytest.raises(AccessError):
        channel_join_v1(123456, public_channel) 
                
    
def test_channel_join_invalid_channel(clear_data, user_1, public_channel):
    # Raises InputError since channel_id 2 does not exist
    with pytest.raises(InputError):
        channel_join_v1(user_1, 2) 
        
        
def test_channel_join_private_channel(clear_data, user_2, private_channel, user_1):        
    # Raises AccessError since user_1 is a member attempting to enter a private
    # channel
    with pytest.raises(AccessError):    
        channel_join_v1(user_1, private_channel) 
        
        
def test_channel_join_valid(clear_data, user_1, public_channel, user_2):
    # Testing if a single member can join a public channel
    channel_join_v1(user_2, public_channel)
    
    channels = channel_details_v1(user_1, public_channel)
    assert len(channels['all_members']) == 2
    assert channels['all_members'][0]['u_id'] == user_1
    assert channels['all_members'][1]['u_id'] == user_2    
    
    
def test_channel_join_valid_multi(clear_data, user_1, user_2, public_channel):
    user_3 = auth_register_v1("philiptran@gmail.com", "password", "Philip", "Tran")
    # Testing if multiple members can join a public channel
    channel_join_v1(user_2, public_channel)
    channel_join_v1(user_3['auth_user_id'], public_channel)

    channels = channel_details_v1(user_1, public_channel)
    assert len(channels['all_members']) == 3
    assert channels['all_members'][0]['u_id'] == user_1
    assert channels['all_members'][1]['u_id'] == user_2
    assert channels['all_members'][2]['u_id'] == user_3['auth_user_id']
    

def test_channel_join_global_private(clear_data, user_1, user_2, private_channel):
    # Test to see if a global member (user_1), gets added as a member and owner
    # of private_channel
    channel_join_v1(user_1, private_channel)
    
    channels = channel_details_v1(user_2, private_channel)
    # Checking if user_1 has been added into the members and owners list 
    assert len(channels['all_members']) == 2
    assert len(channels['owner_members']) == 2
    assert channels['all_members'][0]['u_id'] == user_2
    assert channels['all_members'][1]['u_id'] == user_1
    assert channels['owner_members'][0]['u_id'] == user_2
    assert channels['owner_members'][1]['u_id'] == user_1

