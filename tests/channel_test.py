import pytest
from src.error import InputError, AccessError
from src.auth import auth_register_v1
from src.channels import channels_create_v1, channels_listall_v1
from src.channel import channel_invite_v1, channel_details_v1
from src.other import clear_v1

@pytest.fixture
def user_1():
    user = auth_register_v1("john@gmail.com", "password", "John", "Smith")
    return user_1['auth_user_id']

@pytest.fixture
def user_2():
    user = auth_register_v1("terry@gmail.com", "password", "Terry", "Nguyen")
    return user_2['auth_user_id']

@pytest.fixture
def public_channel(user_1):
    channel = channels_create_v1(user_1, "John's Channel", True)
    return channel['channel_id']

@pytest.fixture
def clear():
    clear_v1()
################################################################################

def test_invite_invalid_channel(clear, user_1, user_2):
    with pytest.raises(InputError):
        channel_invite_v1(user_1, 2, user_2)

def test_invite_invalid_uid(clear, user_1, user_2, public_channel):
    with pytest.raises(InputError):
        channel_invite_v1(user_1, public_channel, 3)

def test_invite_invalid_auth_id(clear, user_1, user_2, public_channel):
    with pytest.raises(AccessError):
        channel_invite_v1(user_2, public_channel, user_1)

def test_invite_duplicate_uid(clear, user_1, user_2, public_channel):
    channel_invite_v1(user_1, public_channel, user_2)
    with pytest.raises(InputError):
        channel_invite_v1(user_1, public_channel, user_2)

def test_invite_valid_inputs(clear, user_1, user_2, public_channel):
    channel_invite_v1(user_1, public_channel, user_2)
    channel_members = channel_details_v1(user_1, public_channel)
    member_found = False
    for members in channel_members['all_members']:
        if members["u_id"] == user_2:
            member_found == True
    assert member_found == True

################################################################################
@pytest.fixture
def expected_output_details():
    John_Channel_Details = {
        'name': "John's Channel",
        'owner_members': [
            {
                'u_id': 1,
                'name_first': 'John',
                'name_last': 'Smith',
            }
        ],
        'all_members': [
            {
                'u_id': 2,
                'name_first': 'Terry',
                'name_last': 'Nguyen',
            }
        ],
    }
    return John_Channel_Details

def test_details_invalid_channel(clear, user_1):
    clear_v1()
    channel = public_channel
    with pytest.raises(InputError):
        channel_details_v1(user_1, 2)

def test_details_invalid_auth_id(clear, user_2, public_channel):
    with pytest.raises(AccessError):
        channel_details_v1(user_2, public_channel)

def test_details_valid_inputs(clear, user_1, public_channel, expected_output_details):
    channel_invite_v1(user_1, public_channel, user_2)
    assert channel_details_v1(user_1, public_channel) == expected_output_details


    



    
