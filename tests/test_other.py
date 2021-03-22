from src.other import clear_v1, search_v1
from src.auth import auth_register_v1, auth_login_v1
from src.channel import channel_messages_v1
from src.channels import channels_create_v1, channels_listall_v1
from src.user import user_profile_v1
from src.database import data
from src.error import InputError, AccessError
from src.message import message_send_v1

import pytest
import random
import string

INVALID_STRING_LENGTH = 1001

LOWER_QUERY_STR = "hows it going"
UPPER_QUERY_STR = "HOWS IT GOING"
MIXED_LETTERS_QUERY_STR = "Hows it going"
NUMERIC_QUERY_STR = "123456789"
SYMBOLS_QUERY_STR = "!#$%&()*+"
MIXED_QUERY_STR = "1. How's it going?"
EMPTY_QUERY_STR = ""

@pytest.fixture
def user_1():
    user = auth_register_v1("johnsmith@gmail.com", "password", "John", "Smith")
    return user['auth_user_id']

@pytest.fixture
def public_channel(user_1):
    channel = channels_create_v1(user_1, "John's Channel", True)
    return channel['channel_id']

@pytest.fixture
def clear_data():
    clear_v1()

def test_clear_users(clear_data, user_1, public_channel):
    clear_v1()
    # Should raise InputError as registered user has been deleted and thus
    # cannot login.
    with pytest.raises(InputError):
        auth_login_v1("johnsmith@gmail.com", "password")

def test_clear_channels(clear_data, user_1, public_channel):
    clear_v1()
    user_2 = auth_register_v1("terrynguyen@gmail.com", "password", "Terry", "Nguyen")
    # Run channels_listall_v1() with user_2 which should return an empty list as 
    # all channels have been deleted.
    assert(channels_listall_v1(user_2['auth_user_id']) == {'channels': []})

    # If both of the above tests are passed, then clear_v1() works as all of both
    # users and channels were deleted

    # Cannot check if messages have been cleared yet (Iteration 1).
'''
def create_invalid_string():
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for counter in range(INVALID_STRING_LENGTH))

def test_search_invalid_query_str(user_1):
    string = create_invalid_string()
    with pytest.raises(InputError):
        search_v1(user_1['u_id'], string)

def test_search_only_DMs():

def test_search_only_channels(clear_data, user_1, public_channel):
    message_send_v1(user_1['auth_user_id'], public_channel['channel_id'], MIXED_QUERY_STR)
    assert search_v1(user_1['u_id'], MIXED_QUERY_STR) == {???}

def test_search_DMs_and_channels():

def test_search_no_query_str_matches():

def test_search_lowercase_query_str():

def test_search_uppercase_query_str():

def test_search_mixed_letters_query_str():

def test_search_numeric_query_str():

def test_search_symbols_query_str():

def test_search_mixed_query_str():

def test_search_empty_query_str():

def test_search_empty_database():
'''