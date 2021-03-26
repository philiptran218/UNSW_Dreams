import pytest
from src.error import InputError, AccessError
from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.channel import channel_invite_v1, channel_details_v1, channel_messages_v1
from src.channel import channel_join_v1, channel_addowner_v1, channel_removeowner_v1, channel_leave_v1
from src.other import clear_v1
from src.message import message_send_v1
from src.database import data

INVALID_VALUE = -1

@pytest.fixture
def user_1():
    user = auth_register_v1("johnsmith@gmail.com", "password", "John", "Smith")
    return user['auth_user_id']

@pytest.fixture
def user_2():
    user = auth_register_v1("terrynguyen@gmail.com", "password", "Terry", "Nguyen")
    return user['auth_user_id']

@pytest.fixture
def user_3():
    user = auth_register_v1('philt@gmail.com', 'badpass', 'Phil', 'Tran')
    return user['auth_user_id']

@pytest.fixture
def public_channel_1(user_1):
    channel = channels_create_v1(user_1, "John's Channel", True)
    return channel['channel_id']
    
@pytest.fixture
def public_channel_2(user_2):
    channel = channels_create_v1(user_2, "Terry's Channel", True)
    return channel['channel_id']

@pytest.fixture
def private_channel(user_2):
    channel = channels_create_v1(user_2, "Terry's Channel", False)
    return channel['channel_id']

@pytest.fixture
def clear_data():
    clear_v1()

################################################################################
# channel_invite_v1 tests                                                      #
################################################################################

def test_invite_invalid_channel(clear_data, user_1, user_2):
    with pytest.raises(InputError):
        channel_invite_v1(user_1, INVALID_VALUE, user_2)

def test_invite_invalid_uid(clear_data, user_1, user_2, public_channel_1):
    with pytest.raises(InputError):
        channel_invite_v1(user_1, public_channel_1, INVALID_VALUE)

def test_invite_invalid_auth_id(clear_data, user_1, user_2, public_channel_1):
    with pytest.raises(AccessError):
        channel_invite_v1(user_2, public_channel_1, user_1)

def test_invite_duplicate_uid(clear_data, user_1, user_2, public_channel_1):
    channel_invite_v1(user_1, public_channel_1, user_2)
    channel_invite_v1(user_1, public_channel_1, user_2)
    channel_members = channel_details_v1(user_1, public_channel_1)
    member_count = 0
    for members in channel_members['all_members']:
        if members['u_id'] == user_2:
            member_count += 1
    assert member_count == 1

def test_invite_valid_inputs(clear_data, user_1, user_2, public_channel_1):
    channel_invite_v1(user_1, public_channel_1, user_2)
    channel_members = channel_details_v1(user_1, public_channel_1)
    member_found = False
    for members in channel_members['all_members']:
        if members['u_id'] == user_2:
            member_found = True
    assert member_found == True

def test_invite_global_owner_allowed(clear_data, user_1, user_2, user_3, public_channel_2):
    channel_invite_v1(user_1, public_channel_2, user_3)
    channel_members = channel_details_v1(user_2, public_channel_2)
    member_found = False
    for members in channel_members['all_members']:
        if members['u_id'] == user_3:
            member_found = True
    assert member_found == True

################################################################################
# channel_details_v1 tests                                                     #
################################################################################

def expected_output_details_1():
    John_Channel_Details = {
        'name': "John's Channel",
        'is_public': True,
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

def expected_output_details_2():
    Terry_Channel_Details = {
        'name': "Terry's Channel",
        'is_public': True,
        'owner_members': [
            {
                'u_id': 2,
                'name_first': 'Terry',
                'name_last': 'Nguyen',
                'email': 'terrynguyen@gmail.com',
                'handle_str': 'terrynguyen',
            }
        ],
        'all_members': [
            {
                'u_id': 2,
                'name_first': 'Terry',
                'name_last': 'Nguyen',
                'email': 'terrynguyen@gmail.com',
                'handle_str': 'terrynguyen',
            },
            {
                'u_id': 3,
                'name_first': 'Phil',
                'name_last': 'Tran',
                'email': 'philt@gmail.com',
                'handle_str': 'philtran',
            }
        ]
    }
    return Terry_Channel_Details

def test_details_invalid_channel(clear_data, user_1):
    with pytest.raises(InputError):
        channel_details_v1(user_1, INVALID_VALUE)

def test_details_invalid_channel(clear_data, user_1):
    with pytest.raises(InputError):
        channel_details_v1(user_1, INVALID_VALUE)

def test_details_invalid_auth_id(clear_data, user_1, user_2, public_channel_1):
    with pytest.raises(AccessError):
        channel_details_v1(user_2, public_channel_1)

def test_details_valid_inputs(clear_data, user_1, user_2, public_channel_1):
    channel_invite_v1(user_1, public_channel_1, user_2)
    assert channel_details_v1(user_1, public_channel_1) == expected_output_details_1()

def test_details_global_owner_allowed(clear_data, user_1, user_2, user_3, public_channel_2):
    channel_invite_v1(user_2, public_channel_2, user_3)
    assert channel_details_v1(user_1, public_channel_2) == expected_output_details_2()

################################################################################
# channel_addowner_v1 tests                                                    #
################################################################################

def expected_output_addowner_1():
    John_Channel_Details = {
        'name': "John's Channel",
        'is_public': True,
        'owner_members': [
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

def expected_output_addowner_2():
    Terry_Channel_Details = {
        'name': "Terry's Channel",
        'is_public': True,
        'owner_members': [
            {
                'u_id': 2,
                'name_first': 'Terry',
                'name_last': 'Nguyen',
                'email': 'terrynguyen@gmail.com',
                'handle_str': 'terrynguyen',
            },
            {
                'u_id': 3,
                'name_first': 'Phil',
                'name_last': 'Tran',
                'email': 'philt@gmail.com',
                'handle_str': 'philtran',
            }
        ],
        'all_members': [
            {
                'u_id': 2,
                'name_first': 'Terry',
                'name_last': 'Nguyen',
                'email': 'terrynguyen@gmail.com',
                'handle_str': 'terrynguyen',
            },
            {
                'u_id': 3,
                'name_first': 'Phil',
                'name_last': 'Tran',
                'email': 'philt@gmail.com',
                'handle_str': 'philtran',
            }
        ]
    }
    return Terry_Channel_Details

def test_addowner_invalid_channel(clear_data, user_1, user_2, public_channel_1):
    with pytest.raises(InputError):
        channel_addowner_v1(user_1, INVALID_VALUE, user_2)

def test_addowner_invalid_auth_id(clear_data, user_1, user_2, public_channel_1):
    with pytest.raises(AccessError):
        channel_addowner_v1(INVALID_VALUE, public_channel_1, user_2)

def test_addowner_invalid_uid(clear_data, user_1, user_2, public_channel_1):
    with pytest.raises(AccessError):
        channel_addowner_v1(user_1, public_channel_1, INVALID_VALUE)

def test_addowner_already_owner(clear_data, user_1, public_channel_1):
    with pytest.raises(InputError):
        channel_addowner_v1(user_1, public_channel_1, user_1)

def test_addowner_auth_user_not_owner(clear_data, public_channel_1, user_2):
    with pytest.raises(AccessError):
        channel_addowner_v1(user_2, public_channel_1, user_2)

def test_addowner_global_owner_allowed(clear_data, user_1, user_2, user_3, public_channel_1, public_channel_2):
    channel_invite_v1(user_2, public_channel_2, user_3)
    channel_addowner_v1(user_1, public_channel_2, user_3)
    assert channel_details_v1(user_1, public_channel_2) == expected_output_addowner_2()

def test_addowner_valid_inputs(clear_data, user_1, user_2, public_channel_1):
    channel_invite_v1(user_1, public_channel_1, user_2)
    channel_addowner_v1(user_1, public_channel_1, user_2)
    assert channel_details_v1(user_1, public_channel_1) == expected_output_addowner_1()

################################################################################
# channel_removeowner_v1 tests                                                 #
################################################################################

def expected_output_removeowner():
    Terry_Channel_Details = {
        'name': "Terry's Channel",
        'is_public': True,
        'owner_members': [
            {
                'u_id': 2,
                'name_first': 'Terry',
                'name_last': 'Nguyen',
                'email': 'terrynguyen@gmail.com',
                'handle_str': 'terrynguyen',
            }
        ],
        'all_members': [
            {
                'u_id': 2,
                'name_first': 'Terry',
                'name_last': 'Nguyen',
                'email': 'terrynguyen@gmail.com',
                'handle_str': 'terrynguyen',
            },
            {
                'u_id': 3,
                'name_first': 'Phil',
                'name_last': 'Tran',
                'email': 'philt@gmail.com',
                'handle_str': 'philtran',
            }
        ]
    }
    return Terry_Channel_Details

def test_removeowner_invalid_channel(clear_data, user_1, user_2, public_channel_1):
    with pytest.raises(InputError):
        channel_removeowner_v1(user_1, INVALID_VALUE, user_2)

def test_removeowner_invalid_auth_id(clear_data, user_1, user_2, public_channel_1):
    with pytest.raises(AccessError):
        channel_removeowner_v1(INVALID_VALUE, public_channel_1, user_2)

def test_removeowner_invalid_uid(clear_data, user_1, user_2, public_channel_1):
    with pytest.raises(AccessError):
        channel_removeowner_v1(user_1, public_channel_1, INVALID_VALUE)
        
def test_removeowner_auth_id_not_owner(clear_data, user_1, user_2, public_channel_1):
    channel_invite_v1(user_1, public_channel_1, user_2)
    with pytest.raises(InputError):
        channel_removeowner_v1(user_2, public_channel_1, user_1)

def test_removeowner_only_owner_in_channel(clear_data, user_1, public_channel_1):
    with pytest.raises(InputError):
        channel_removeowner_v1(user_1, public_channel_1, user_1)

def test_removeowner_valid_inputs(clear_data, user_1, user_2, user_3, public_channel_2):
    channel_invite_v1(user_2, public_channel_2, user_3)
    channel_addowner_v1(user_2, public_channel_2, user_3)
    channel_removeowner_v1(user_2, public_channel_2, user_3)
    assert channel_details_v1(user_1, public_channel_2) == expected_output_removeowner()

def test_removeowner_global_owner_allowed(clear_data, user_1, user_2, user_3, public_channel_2):
    channel_invite_v1(user_2, public_channel_2, user_3)
    channel_addowner_v1(user_2, public_channel_2, user_3)
    channel_removeowner_v1(user_1, public_channel_2, user_3)
    assert channel_details_v1(user_1, public_channel_2) == expected_output_removeowner()

################################################################################
# channel_messages_v1 tests                                                    #
################################################################################
     
def test_channel_messages_invalid_channel(clear_data, user_1, public_channel_1):
    # Raises InputError since channel_id INVALID_VALUE does not exist
    with pytest.raises(InputError):
        channel_messages_v1(user_1, INVALID_VALUE, 0) 
        
        
def test_channel_messages_invalid_start(clear_data, user_1, public_channel_1):
    # Raises InputError since start is greater than num messages in channel
    # (there are no messages in channel)
    with pytest.raises(InputError):
        channel_messages_v1(user_1, public_channel_1, 10) 
    

def test_channel_messages_authid_not_member(clear_data, user_1, public_channel_1, user_2):
    # Raises AccessError since user_2 is not a member of channel
    with pytest.raises(AccessError):
        channel_messages_v1(user_2, public_channel_1, 0) 
        
               
def test_channel_messages_invalid_authid(clear_data, user_1, public_channel_1):
    # Raises AccessError since u_id INVALID_VALUE does not exist
    with pytest.raises(AccessError):
        channel_messages_v1(INVALID_VALUE, public_channel_1, 0) 
        
def test_channel_messages_start_equal(clear_data, user_1, public_channel_1):
    # Testing for when start = number of messages in channel
    channels = channel_messages_v1(user_1, public_channel_1, 0) 
    assert channels == {'messages': [], 'start': 0, 'end': -1}
    

# This tests requires message_send_v1 to be implemented.   
'''        
def test_channel_messages_valid_single(clear_data, user_1, public_channel_1):
    # Tests for a single message in channel
    message_send_v1(user_1, public_channel_1, 'A new message')
    message_detail = channel_messages_v1(user_1, public_channel_1, 0)
    
    # Checking the message dictionary to see if message has been appended
    assert message_detail['messages'][0]['message_id'] == 1
    assert message_detail['messages'][0]['u_id'] == user_1
    assert message_detail['messages'][0]['message'] == 'A new message'
    assert message_detail['start'] == 0
    assert message_detail['end'] == -1
''' 

# This tests requires message_send_v1 to be implemented.  
'''     
def test_channel_messages_multiple(clear_data, user_1, public_channel_1):
    # Testing for multiple messages, and non-zero start value 
    # Sends 55 messages to channel, the messages are just numbers as strings
    i = 1
    while i <= 55:
        message_send_v1(user_1, public_channel_1, f"{i}")
        i += 1
    
    message_detail = channel_messages_v1(user_1, public_channel_1, 2)
   
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
    
def test_channel_join_invalid_authid(clear_data, user_1, public_channel_1):
    # Raises AccessError since auth_user_id INVALID_VALUE does not exist
    with pytest.raises(AccessError):
        channel_join_v1(INVALID_VALUE, public_channel_1) 
                
    
def test_channel_join_invalid_channel(clear_data, user_1, public_channel_1):
    # Raises InputError since channel_id INVALID_VALUE does not exist
    with pytest.raises(InputError):
        channel_join_v1(user_1, INVALID_VALUE) 
        
        
def test_channel_join_private_channel(clear_data, user_2, private_channel, user_1):        
    # Raises AccessError since user_1 is a member attempting to enter a private
    # channel
    with pytest.raises(AccessError):    
        channel_join_v1(user_1, private_channel) 
  
        
def test_channel_join_valid(clear_data, user_1, public_channel_1, user_2):
    # Testing if a single member can join a public channel
    channel_join_v1(user_2, public_channel_1)
    
    channels = channel_details_v1(user_1, public_channel_1)
    assert len(channels['all_members']) == 2
    assert channels['all_members'][0]['u_id'] == user_1
    assert channels['all_members'][1]['u_id'] == user_2    
    
def test_channel_join_already_joined(clear_data, user_1, public_channel_1, user_2):
    # Testing when user_2, who is already a channel member, joins the channel again
    channel_join_v1(user_2, public_channel_1)
    assert channel_join_v1(user_2, public_channel_1) == {}
    channels = channel_details_v1(user_1, public_channel_1)
    
    assert len(channels['all_members']) == 2
    assert channels['all_members'][0]['u_id'] == user_1
    assert channels['all_members'][1]['u_id'] == user_2  
    
    
def test_channel_join_valid_multi(clear_data, user_1, user_2, public_channel_1):
    user_3 = auth_register_v1("philiptran@gmail.com", "password", "Philip", "Tran")
    # Testing if multiple members can join a public channel
    channel_join_v1(user_2, public_channel_1)
    channel_join_v1(user_3['auth_user_id'], public_channel_1)

    channels = channel_details_v1(user_1, public_channel_1)
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

################################################################################
# channel_leave_v1 tests                                                       #
################################################################################

def test_channel_leave_invalid_channel(clear_data, user_1, public_channel_1):
    with pytest.raises(InputError):
        channel_leave_v1(user_1, INVALID_VALUE)

def test_channel_leave_invalid_auth_id(clear_data, user_1, public_channel_1):
    with pytest.raises(AccessError):
        channel_leave_v1(INVALID_VALUE, public_channel_1)

def test_channel_leave_auth_id_not_in_channel(clear_data, user_1, user_2, public_channel_1):
    with pytest.raises(AccessError):
        channel_leave_v1(user_2, public_channel_1)

def test_channel_leave_valid_inputs(clear_data, user_1, user_2, public_channel_1):
    channel_invite_v1(user_1, public_channel_1, user_2)
    channel_leave_v1(user_2, public_channel_1)
    info = channel_details_v1(user_1, public_channel_1)
    user_found = False
    for member in info['all_members']:
        if member['u_id'] == user_2:
            user_found == True
    assert user_found == False

def test_channel_leave_owner_leaves(clear_data, user_1, user_2, public_channel_1):
    channel_invite_v1(user_1, public_channel_1, user_2)
    channel_addowner_v1(user_1, public_channel_1, user_2)
    channel_leave_v1(user_2, public_channel_1)
    info = channel_details_v1(user_1, public_channel_1)
    user_found = False
    for member in info['owner_members']:
        if member['u_id'] == user_2:
            user_found == True
    for member in info['all_members']:
        if member['u_id'] == user_2:
            user_found == True
    assert user_found == False

def test_channel_leave_last_member_leaves(clear_data, user_1, public_channel_1):
    channel_leave_v1(user_1, public_channel_1)
    info = channel_details_v1(user_1, public_channel_1)
    assert info['name'] == "John's Channel"
    assert info['is_public'] == True
    assert info['owner_members'] == []
    assert info['all_members'] == []
