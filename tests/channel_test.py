import pytest

from src.channel import channel_messages_v1, channel_join_v1, channel_details_v1
from src.error import InputError, AccessError 
from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.message import message_send_v1
# from src.data import data

@pytest.fixture
def supply_user1():
    
    ''' this user is a global owner '''
    new_user1 = auth_register_v1('johnsmith@gmail.com', 'goodpass', 'John', 'Smith')    
    return new_user1
    
@pytest.fixture
def supply_user2():
    
    new_user2 = auth_register_v1('philt@gmail.com', 'badpass', 'Phil', 'Tran')
    return new_user2
    
@pytest.fixture
def supply_user3():
    
    new_user3 = auth_register_v1('person@gmail.com', 'helloworld', 'First', 'Name')
    return new_user3
  
@pytest.fixture
def supply_chan1(supply_user1):   

    ''' channel1 is public ''' 
    new_chan1 = channels_create_v1(supply_user1, 'channel1', True) 
    return new_chan1

@pytest.fixture    
def supply_chan2(supply_user2):
    
    ''' channel2 is private '''
    new_chan2 = channels_create_v1(supply_user2, 'channel2', False) 
    return new_chan2

@pytest.fixture
def supply_message1(supply_user1, supply_chan1):
    
    message_send_v1(supply_user1, supply_chan1, 'A new message')

@pytest.fixture    
def supply_multi1(supply_user1, supply_chan1, supply_message1):

    i = 1
    while i <= 55:
        message_send_v1(supply_user1, supply_chan1, f'{i}')
        i += 1
        
    
    ''' data added from fixtures should look like this '''
'''
    data = {
        'users': [
            {
                'u_id': 1,
                'password': 'goodpass'
                'first_name': 'John',
                'last_name': 'Smith',
                'email': 'johnsmith@gmail.com',
                'perm_id': 1,
            },  
            {
                'u_id': 2,
                'password': 'badpass'
                'first_name': 'Phil',
                'last_name': 'Tran',
                'email': 'philt@gmail.com',
                'perm_id': 2,
            },
        ],
        'channels': [   
            {
                'channel_id': 1,
                'name': 'channel1',
                'owner_ids': [1],
                'member_ids': [1],
                'messages': [
                    {          
                        'message_id': 1,
                        'u_id': 1,
                        'message': 'A new message',
                        'time_created': this can be whatever.
                    }
                ],    
                'is_public': True 
            },
            {
                'channel_id': 2,
                'name': 'channel2',
                'owner_ids': [2],
                'member_ids': [2],
                'messages': [
                    currently blank
                ],    
                'is_public': False   
            }
        ]
    }
'''
                          
################################################################################
# channel_messages_v1 tests
################################################################################
    
def test_channel_messages_invalid_channel(clear_v1, supply_user1, supply_chan1):
    #clear_v1()
    with pytest.raises(InputError):
        channel_messages_v1(supply_user1, 123456, 0) 
        ''' channel_id 123456 doesnt exist '''
        
        
def test_channel_messages_invalid_start(supply_user2, supply_chan2):
    
    with pytest.raises(InputError):
        channel_messages_v1(supply_user2, supply_chan2, 10) 
        ''' raises error since start is 10, but there are no messages in supply_chan2 '''
    

def test_channel_messages_authid_not_member(supply_user1, supply_chan1, supply_user2):
    
    with pytest.raises(AccessError):
        channel_messages_v1(supply_user2, supply_chan1, 0) 
        ''' fails since supply_user2 is not in supply_chan1 '''
        
               
def test_channel_messages_invalid_authid(supply_user1, supply_chan1):

    with pytest.raises(AccessError):
        channel_messages_v1(123456, supply_chan1, 0) 
        ''' auth_id 123456 doesnt exist '''
        
        
def test_channel_messages_valid_single(supply_user1, supply_chan1, supply_message1):

    message_detail = channel_messages_v1(supply_user1, supply_chan1, 0)
    
    ''' checking each value is correct in the returned dictionary '''
    assert message_detail['messages'][0]['message_id'] == 1
    assert message_detail['messages'][0]['u_id'] == supply_user1
    assert message_detail['messages'][0]['message'] == 'A new message'
    assert message_detail['start'] == 0
    assert message_detail['end'] == -1
    
   
def test_channel_messages_multiple(supply_user1, supply_chan1, supply_message1, supply_multi1):

    message_detail = channel_messages_v1(supply_user1, supply_chan1, 0)
    
    assert message_detail['messages'][0]['message_id'] == 1
    assert message_detail['messages'][0]['u_id'] == supply_user1
    assert message_detail['messages'][0]['message'] == 'A new message'
    
    i = 1
    while i <= 50:
        assert message_detail['messages'][i]['message_id'] == i + 1
        assert message_detail['messages'][i]['u_id'] == supply_user1
        assert message_detail['messages'][i]['message'] == f'{i}'
        
    assert message_detail['start'] == 0
    assert message_detail['end'] == 50

    
    
################################################################################
# channel_join_v1 tests
################################################################################
    
def test_channel_join_invalid_authid(supply_user1, supply_user2, supply_chan1):

    with pytest.raises(AccessError):
        channel_join_v1(123456, supply_chan1) 
        ''' fails since auth_user_id 123456 doesnt exist '''
        
    
def test_channel_join_invalid_channel(supply_user1, supply_chan1):

    with pytest.raises(InputError):
        channel_join_v1(supply_user1, 2) 
        ''' should fail since channel_id 2 does not exist'''
        
        
def test_channel_join_private_channel(supply_user2, supply_chan2, supply_user3):        
        
    with pytest.raises(AccessError):    
        channel_join_v1(supply_user3, supply_chan2) 
        ''' should fail since supply_chan2 is private and supply_user3 is not a global owner '''
        
        
def test_channel_join_valid(supply_user1, supply_chan1, supply_user2):
    channel_join_v1(supply_user2, supply_chan1)
    
    channels = channel_details_v1(supply_user1, supply_chan1)
    
    ''' ensuring that number of members increases and their names are listed in order '''
    assert len(channels['all_members']) == 2
    assert channels['all_members'][0]['u_id'] == supply_user1
    assert channels['all_members'][1]['u_id'] == supply_user2    
    
    
def test_channel_join_valid_multi(supply_user1, supply_user2, supply_user3, supply_chan1):

    channel_join_v1(supply_user2, supply_chan1)
    channel_join_v1(supply_user3, supply_chan1)

    channels = channel_details_v1(supply_user1, supply_chan1)
    
    assert len(channels['all_members']) == 3
    assert channels['all_members'][0]['u_id'] == supply_user1
    assert channels['all_members'][1]['u_id'] == supply_user2
    assert channels['all_members'][2]['u_id'] == supply_user3
    

def test_channel_join_global_private(supply_user1, supply_user2, supply_chan2):

    ''' should allow global owner to join private channel '''
    channel_join_v1(supply_user1, supply_chan2)
    
    channels = channel_details_v1(supply_user2, supply_chan2)
    
    assert len(channels['all_members']) == 2
    assert len(channels['owner_members']) == 2
    assert channels['all_members'][0]['u_id'] == supply_user2
    assert channels['all_members'][1]['u_id'] == supply_user1
    assert channels['owner_members'][0]['u_id'] == supply_user2
    assert channels['owner_members'][1]['u_id'] == supply_user1
        
