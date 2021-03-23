from src.other import clear_v1, search_v1
from src.auth import auth_register_v1, auth_login_v1
from src.channel import channel_messages_v1, channel_invite_v1
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
NUMERIC_QUERY_STR = "123456789"
SYMBOLS_QUERY_STR = "!#$%&()*+"
MIXED_QUERY_STR = "1. How's it going?"
EMPTY_QUERY_STR = ""
SUB_STRING = "it"

@pytest.fixture
def user_1():
    user = auth_register_v1("johnsmith@gmail.com", "password", "John", "Smith")
    return user['auth_user_id']

@pytest.fixture
def user_2():
    user = auth_register_v1("terrynguyen@gmail.com", "password", "Terry", "Nguyen")
    return user['auth_user_id']

@pytest.fixture
def public_channel_1 (user_1):
    channel = channels_create_v1(user_1, "John's Channel", True)
    return channel['channel_id']

@pytest.fixture
def public_channel_2 (user_2):
    channel = channels_create_v1(user_2, "Terry's Channel", True)
    return channel['channel_id']

@pytest.fixture
def user_1_dm (user_1, user_2):
    dm = dm_create_v1(user_1, [user_1, user_2])
    return dm['dm_id']

@pytest.fixture
def user_2_dm (user_1, user_2):
    dm = dm_create_v1(user_2, [user_1, user_2])
    return dm['dm_id']

@pytest.fixture
def clear_data():
    clear_v1()

################################################################################
# clear_v1() tests                                                             #
################################################################################

def test_clear_users(clear_data, user_1, public_channel_1):
    clear_v1()
    # Should raise InputError as registered user has been deleted and thus
    # cannot login.
    with pytest.raises(InputError):
        auth_login_v1("johnsmith@gmail.com", "password")

def test_clear_channels(clear_data, user_1, public_channel_1):
    clear_v1()
    user_2 = auth_register_v1("terrynguyen@gmail.com", "password", "Terry", "Nguyen")
    # Run channels_listall_v1() with user_2 which should return an empty list as 
    # all channels have been deleted.
    assert(channels_listall_v1(user_2['auth_user_id']) == {'channels': []})

    # If both of the above tests are passed, then clear_v1() works as all of both
    # users and channels were deleted

    # Cannot check if messages have been cleared yet (Iteration 1).

################################################################################
# search_v1 tests                                                              #
################################################################################

def create_invalid_string():
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for counter in range(INVALID_STRING_LENGTH))

def test_search_invalid_query_str(user_1):
    string = create_invalid_string()
    with pytest.raises(InputError):
        search_v1(user_1, string)

def test_search_only_DMs(clear_data, user_1, user_1_dm):
    message_senddm_v1(user_1, user_1_dm, MIXED_QUERY_STR)
    output = search_v1(user_1, MIXED_QUERY_STR)
    assert output['messages'][0]['message_id'] == 1
    assert output['messages'][0]['u_id'] == 1
    assert output['messages'][0]['channel_id'] == 0
    assert output['messages'][0]['dm_id'] == 1
    assert output['messages'][0]['message'] == MIXED_QUERY_STR

def test_search_only_channels(clear_data, user_1, public_channel_1):
    message_send_v1(user_1, public_channel_1, MIXED_QUERY_STR)
    output = search_v1(user_1, MIXED_QUERY_STR)
    assert output['messages'][0]['message_id'] == 1
    assert output['messages'][0]['u_id'] == 1
    assert output['messages'][0]['channel_id'] == 1
    assert output['messages'][0]['dm_id'] == 0
    assert output['messages'][0]['message'] == MIXED_QUERY_STR

def test_search_DMs_and_channels(clear_data, user_1, public_channel_1, user_1_dm):
    message_send_v1(user_1, public_channel_1, MIXED_QUERY_STR)
    message_senddm_v1(user_1, user_1_dm, MIXED_QUERY_STR)
    output = search_v1(user_1, MIXED_QUERY_STR)
    assert output['messages'][0]['message_id'] == 1
    assert output['messages'][0]['u_id'] == 1
    assert output['messages'][0]['channel_id'] == 1
    assert output['messages'][0]['dm_id'] == 0
    assert output['messages'][0]['message'] == MIXED_QUERY_STR
    assert output['messages'][1]['message_id'] == 2
    assert output['messages'][1]['u_id'] == 1
    assert output['messages'][1]['channel_id'] == 0
    assert output['messages'][1]['dm_id'] == 1
    assert output['messages'][1]['message'] == MIXED_QUERY_STR

def test_search_no_query_str_matches(clear_data, user_1, public_channel_1, user_1_dm):
    message_send_v1(user_1, public_channel_1, MIXED_QUERY_STR)
    message_senddm_v1(user_1, user_1_dm, MIXED_QUERY_STR)
    output = search_v1(user_1, UPPER_QUERY_STR)
    assert output['messages'] == []

def test_search_lowercase_query_str(clear_data, user_1, public_channel_1, user_1_dm):
    message_send_v1(user_1, public_channel_1, MIXED_QUERY_STR)
    message_senddm_v1(user_1, user_1_dm, MIXED_QUERY_STR)
    message_send_v1(user_1, public_channel_1, LOWER_QUERY_STR)
    message_senddm_v1(user_1, user_1_dm, LOWER_QUERY_STR)
    message_send_v1(user_1, public_channel_1, UPPER_QUERY_STR)
    message_senddm_v1(user_1, user_1_dm, UPPER_QUERY_STR)
    output = search_v1(user_1, LOWER_QUERY_STR)
    assert output['messages'][0]['message_id'] == 3
    assert output['messages'][0]['u_id'] == 1
    assert output['messages'][0]['channel_id'] == 1
    assert output['messages'][0]['dm_id'] == 0
    assert output['messages'][0]['message'] == LOWER_QUERY_STR
    assert output['messages'][1]['message_id'] == 4
    assert output['messages'][1]['u_id'] == 1
    assert output['messages'][1]['channel_id'] == 0
    assert output['messages'][1]['dm_id'] == 1
    assert output['messages'][1]['message'] == LOWER_QUERY_STR

def test_search_uppercase_query_str(clear_data, user_1, public_channel_1, user_1_dm):
    message_send_v1(user_1, public_channel_1, MIXED_QUERY_STR)
    message_senddm_v1(user_1, user_1_dm, MIXED_QUERY_STR)
    message_send_v1(user_1, public_channel_1, LOWER_QUERY_STR)
    message_senddm_v1(user_1, user_1_dm, LOWER_QUERY_STR)
    message_send_v1(user_1, public_channel_1, UPPER_QUERY_STR)
    message_senddm_v1(user_1, user_1_dm, UPPER_QUERY_STR)
    output = search_v1(user_1, UPPER_QUERY_STR)
    assert output['messages'][0]['message_id'] == 5
    assert output['messages'][0]['u_id'] == 1
    assert output['messages'][0]['channel_id'] == 1
    assert output['messages'][0]['dm_id'] == 0
    assert output['messages'][0]['message'] == UPPER_QUERY_STR
    assert output['messages'][1]['message_id'] == 6
    assert output['messages'][1]['u_id'] == 1
    assert output['messages'][1]['channel_id'] == 0
    assert output['messages'][1]['dm_id'] == 1
    assert output['messages'][1]['message'] == UPPER_QUERY_STR

def test_search_numeric_query_str(clear_data, user_1, public_channel_1, user_1_dm):
    message_send_v1(user_1, public_channel_1, NUMERIC_QUERY_STR)
    message_send_v1(user_1, public_channel_1, MIXED_QUERY_STR)
    message_senddm_v1(user_1, user_1_dm, MIXED_QUERY_STR)
    message_send_v1(user_1, public_channel_1, UPPER_QUERY_STR)
    message_senddm_v1(user_1, user_1_dm, UPPER_QUERY_STR)
    message_senddm_v1(user_1, user_1_dm, NUMERIC_QUERY_STR)
    output = search_v1(user_1, NUMERIC_QUERY_STR)
    assert output['messages'][0]['message_id'] == 1
    assert output['messages'][0]['u_id'] == 1
    assert output['messages'][0]['channel_id'] == 1
    assert output['messages'][0]['dm_id'] == 0
    assert output['messages'][0]['message'] == NUMERIC_QUERY_STR
    assert output['messages'][1]['message_id'] == 6
    assert output['messages'][1]['u_id'] == 1
    assert output['messages'][1]['channel_id'] == 0
    assert output['messages'][1]['dm_id'] == 1
    assert output['messages'][1]['message'] == NUMERIC_QUERY_STR

def test_search_symbols_query_str(clear_data, user_1, public_channel_1, user_1_dm):
    message_send_v1(user_1, public_channel_1, MIXED_QUERY_STR)
    message_senddm_v1(user_1, user_1_dm,SYMBOLS_QUERY_STR)
    message_send_v1(user_1, public_channel_1, NUMERIC_QUERY_STR)
    message_senddm_v1(user_1, user_1_dm, NUMERIC_QUERY_STR)
    message_send_v1(user_1, public_channel_1, SYMBOLS_QUERY_STR)
    message_senddm_v1(user_1, user_1_dm, UPPER_QUERY_STR)
    output = search_v1(user_1, SYMBOLS_QUERY_STR)
    assert output['messages'][0]['message_id'] == 2
    assert output['messages'][0]['u_id'] == 1
    assert output['messages'][0]['channel_id'] == 1
    assert output['messages'][0]['dm_id'] == 0
    assert output['messages'][0]['message'] == SYMBOLS_QUERY_STR
    assert output['messages'][1]['message_id'] == 5
    assert output['messages'][1]['u_id'] == 1
    assert output['messages'][1]['channel_id'] == 0
    assert output['messages'][1]['dm_id'] == 1
    assert output['messages'][1]['message'] == SYMBOLS_QUERY_STR

def test_search_empty_query_str(clear_data, user_1, public_channel_1, user_1_dm):
    message_send_v1(user_1, public_channel_1, MIXED_QUERY_STR)
    message_senddm_v1(user_1, user_1_dm, MIXED_QUERY_STR)
    output = search_v1(user_1, EMPTY_QUERY_STR)
    assert output['messages'] == []

def test_search_empty_database(clear_data, user_1):
    output = search_v1(user_1, MIXED_QUERY_STR)
    assert output['messages'] == []

def test_search_substring(clear_data, user_1, user_2, public_channel_1, user_1_dm):
    message_send_v1(user_1, public_channel_1, NUMERIC_QUERY_STR)  
    message_senddm_v1(user_2, user_1_dm, NUMERIC_QUERY_STR)
    message_send_v1(user_2, public_channel_1, MIXED_QUERY_STR)
    message_senddm_v1(user_1, user_1_dm, MIXED_QUERY_STR)
    message_send_v1(user_1, public_channel_1, UPPER_QUERY_STR)
    message_senddm_v1(user_2, user_1_dm, UPPER_QUERY_STR)
    message_send_v1(user_1, public_channel_1, LOWER_QUERY_STR)
    message_senddm_v1(user_2, user_1_dm, LOWER_QUERY_STR)
    output = search_v1(user_1, SUB_STRING)
    assert output['messages'][0]['message_id'] == 3
    assert output['messages'][0]['u_id'] == 2
    assert output['messages'][0]['channel_id'] == 1
    assert output['messages'][0]['dm_id'] == 0
    assert output['messages'][0]['message'] == MIXED_QUERY_STR
    assert output['messages'][1]['message_id'] == 4
    assert output['messages'][1]['u_id'] == 1
    assert output['messages'][1]['channel_id'] == 0
    assert output['messages'][1]['dm_id'] == 1
    assert output['messages'][1]['message'] == MIXED_QUERY_STR
    assert output['messages'][2]['message_id'] == 7
    assert output['messages'][2]['u_id'] == 1
    assert output['messages'][2]['channel_id'] == 1
    assert output['messages'][2]['dm_id'] == 0
    assert output['messages'][2]['message'] == MIXED_QUERY_STR
    assert output['messages'][3]['message_id'] == 8
    assert output['messages'][3]['u_id'] == 2
    assert output['messages'][3]['channel_id'] == 0
    assert output['messages'][3]['dm_id'] == 1
    assert output['messages'][3]['message'] == MIXED_QUERY_STR

def test_search_multiple_channels(clear_data, user_1, user_2, public_channel_1, public_channel_2):
    channel_invite_v1(user_2, public_channel_2, user_1)
    message_send_v1(user_1, public_channel_1, MIXED_QUERY_STR)
    message_send_v1(user_2, public_channel_2, MIXED_QUERY_STR)
    output = search_v1(user_1, SUB_STRING)
    assert output['messages'][0]['message_id'] == 1
    assert output['messages'][0]['u_id'] == 1
    assert output['messages'][0]['channel_id'] == 1
    assert output['messages'][0]['dm_id'] == 0
    assert output['messages'][0]['message'] == MIXED_QUERY_STR
    assert output['messages'][1]['message_id'] == 2
    assert output['messages'][1]['u_id'] == 2
    assert output['messages'][1]['channel_id'] == 2
    assert output['messages'][1]['dm_id'] == 0
    assert output['messages'][1]['message'] == MIXED_QUERY_STR

def test_search_multiple_dms(clear_data, user_1, user_2, user_1_dm, user_2_dm):
    message_senddm_v1(user_1, user_1_dm, MIXED_QUERY_STR)
    message_senddm_v1(user_2, user_2_dm, MIXED_QUERY_STR)
    output = search_v1(user_1, SUB_STRING)
    assert output['messages'][0]['message_id'] == 1
    assert output['messages'][0]['u_id'] == 1
    assert output['messages'][0]['channel_id'] == 0
    assert output['messages'][0]['dm_id'] == 1
    assert output['messages'][0]['message'] == MIXED_QUERY_STR
    assert output['messages'][1]['message_id'] == 2
    assert output['messages'][1]['u_id'] == 2
    assert output['messages'][1]['channel_id'] == 0
    assert output['messages'][1]['dm_id'] == 2
    assert output['messages'][1]['message'] == MIXED_QUERY_STR

def test_search_multiple_channels_and_dms(clear_data, user_1, user_2, user_1_dm, user_2_dm, public_channel_1, public_channel_2):
    channel_invite_v1(user_2, public_channel_2, user_1)
    message_send_v1(user_1, public_channel_1, MIXED_QUERY_STR)
    message_send_v1(user_1, public_channel_1, NUMERIC_QUERY_STR)
    message_send_v1(user_2, public_channel_2, NUMERIC_QUERY_STR)
    message_send_v1(user_2, public_channel_2, MIXED_QUERY_STR)
    message_senddm_v1(user_1, user_1_dm, SYMBOLS_QUERY_STR)
    message_senddm_v1(user_1, user_1_dm, MIXED_QUERY_STR)
    message_senddm_v1(user_2, user_2_dm, MIXED_QUERY_STR)
    message_senddm_v1(user_2, user_2_dm, SYMBOLS_QUERY_STR)
    output = search_v1(user_1, SUB_STRING)
    assert output['messages'][0]['message_id'] == 1
    assert output['messages'][0]['u_id'] == 1
    assert output['messages'][0]['channel_id'] == 1
    assert output['messages'][0]['dm_id'] == 0
    assert output['messages'][0]['message'] == MIXED_QUERY_STR
    assert output['messages'][1]['message_id'] == 4
    assert output['messages'][1]['u_id'] == 2
    assert output['messages'][1]['channel_id'] == 2
    assert output['messages'][1]['dm_id'] == 0
    assert output['messages'][1]['message'] == MIXED_QUERY_STR
    assert output['messages'][2]['message_id'] == 6
    assert output['messages'][2]['u_id'] == 1
    assert output['messages'][2]['channel_id'] == 0
    assert output['messages'][2]['dm_id'] == 1
    assert output['messages'][2]['message'] == MIXED_QUERY_STR
    assert output['messages'][3]['message_id'] == 7
    assert output['messages'][3]['u_id'] == 2
    assert output['messages'][3]['channel_id'] == 0
    assert output['messages'][3]['dm_id'] == 2
    assert output['messages'][3]['message'] == MIXED_QUERY_STR

