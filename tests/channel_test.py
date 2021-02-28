"""
Required Tests:
    - Test if channel_id is valid. (InputError)
        + Try passing in valid channel_id.
        + Try passing in invalid channel_id.
    - Test if u_id is valid. (InputError)
        + Try passing in valid u_id.
        + Try passing in invalid u_id.
    - Test if auth_user_id is member of channel. (AccessError)
        + Try passing an auth_user_id that is a member of channel.
        + Try passing an auth_user_id that is not a member of channel.
    - Test if u_id is
    - Ensure once invited the user is added to the channel immediately.
        + Check if user is in channel.
    Note: Have not add, commit, push yet
"""

import pytest
from src.error import InputError, AccessError
from src.auth import auth_register_v1
from src.channels import channels_create_v1, channels_listall_v1
from src.channel import channel_invite_v1, channel_details_v1

@pytest.fixture
def user_1():
    user = auth_register_v1("john@gmail.com", "password", "John", "Smith")
    return user_1

@pytest.fixture
def user_2():
    user = auth_register_v1("terry@gmail.com", "password", "Terry", "Nguyen")
    return user_2

@pytest.fixture
def public_channel(user_1):
    #user_1 = supply_user_1()
    channel = channels_create_v1(user_1, "John's Channel", True)
    return channel

def test_invite_invalid_channel(user_1, user_2):
    #user_1 = supply_user_1()
    #user_2 = supply_user_2()
    with pytest.raises(InputError):
        channel_invite_v1(user_1, 2, user_2)

def test_invite_valid_inputs(user_1, user_2, public_channel):
    #user_1 = supply_user_1()
    #user_2 = supply_user_2()
    channel_invite_v1(user_1, public_channel, user_2)
    channel_members = channel_details_v1(user_1, public_channel)
    member_found = False
    for members in channel_members['all_members']:
        if members["u_id"] == user_2:
            member_found == True
    assert member_found == True

def test_invite_invalid_uid(user_1, user_2, public_channel):
    #user_1 = supply_user_1()
    #user_2 = supply_user_2()
    with pytest.raises(InputError):
        channel_invite_v1(user_1, public_channel, 3)

def test_invite_invalid_auth_id(user_1, user_2, public_channel):
    #user_1 = supply_user_1()
    #user_2 = supply_user_2()
    with pytest.raises(AccessError):
        channel_invite_v1(user_2, public_channel, user_1)

def test_invite_duplicate_uid(user_1, user_2, public_channel):
    channel_invite_v1(user_1, public_channel, user_2)
    with pytest.raises(InputError):
        channel_invite_v1(user_1, public_channel, user_2)



# def test_details_invalid_channel():
    



    
