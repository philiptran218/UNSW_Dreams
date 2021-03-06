from src.other import clear_v1, search_v1, notifications_get_v1
from src.auth import auth_register_v1, auth_login_v1
from src.channel import channel_messages_v1, channel_invite_v1
from src.channels import channels_create_v1, channels_listall_v1
from src.database import data
from src.error import InputError, AccessError
from src.message import message_send_v1, message_senddm_v1, message_edit_v1, message_react_v1
from src.dm import dm_create_v1, dm_invite_v1

import pytest
import random
import string

INVALID_VALUE = -1
INVALID_STRING_LENGTH = 1001

LOWER_QUERY_STR = "hows it going"
UPPER_QUERY_STR = "HOWS IT GOING"
NUMERIC_QUERY_STR = "123456789"
SYMBOLS_QUERY_STR = "!#$%&()*+"
MIXED_QUERY_STR = "1. How's it going?"
EMPTY_QUERY_STR = ""
SUB_STRING = "it"
WHITE_SPACE_QUERY_STR = "     it      "

@pytest.fixture
def user_1():
    user = auth_register_v1("johnsmith@gmail.com", "password", "John", "Smith")
    return user

@pytest.fixture
def user_2():
    user = auth_register_v1("terrynguyen@gmail.com", "password", "Terry", "Nguyen")
    return user

@pytest.fixture
def user_3():
    user = auth_register_v1('philt@gmail.com', 'badpass', 'Phil', 'Tran')
    return user

@pytest.fixture
def public_channel_1 (user_1):
    channel = channels_create_v1(user_1['token'], "John's Channel", True)
    return channel['channel_id']

@pytest.fixture
def public_channel_2 (user_2):
    channel = channels_create_v1(user_2['token'], "Terry's Channel", True)
    return channel['channel_id']

@pytest.fixture
def user_1_dm (user_1, user_2):
    dm = dm_create_v1(user_1['token'], [user_2['auth_user_id']])
    return dm['dm_id']

@pytest.fixture
def user_2_dm (user_1, user_2):
    dm = dm_create_v1(user_2['token'], [user_1['auth_user_id']])
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
    assert(channels_listall_v1(user_2['token']) == {'channels': []})

    # If both of the above tests are passed, then clear_v1() works as all of both
    # users and channels were deleted

    # Cannot check if messages have been cleared yet (Iteration 1).

################################################################################
# search_v1 tests                                                              #
################################################################################

def create_invalid_string():
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for counter in range(INVALID_STRING_LENGTH))

def test_search_invalid_token(clear_data, user_1):
    with pytest.raises(AccessError):
        search_v1(INVALID_VALUE, string)

def test_search_invalid_query_str(clear_data, user_1):
    string = create_invalid_string()
    with pytest.raises(InputError):
        search_v1(user_1['token'], string)

def test_search_only_DMs(clear_data, user_1, user_1_dm):
    message_senddm_v1(user_1['token'], user_1_dm, MIXED_QUERY_STR)
    output = search_v1(user_1['token'], MIXED_QUERY_STR)
    assert output['messages'][0]['message_id'] == 1
    assert output['messages'][0]['u_id'] == 1
    assert output['messages'][0]['message'] == MIXED_QUERY_STR

def test_search_only_channels(clear_data, user_1, public_channel_1):
    message_send_v1(user_1['token'], public_channel_1, MIXED_QUERY_STR)
    output = search_v1(user_1['token'], MIXED_QUERY_STR)
    assert output['messages'][0]['message_id'] == 1
    assert output['messages'][0]['u_id'] == 1
    assert output['messages'][0]['message'] == MIXED_QUERY_STR

def test_search_DMs_and_channels(clear_data, user_1, public_channel_1, user_1_dm):
    message_send_v1(user_1['token'], public_channel_1, MIXED_QUERY_STR)
    message_senddm_v1(user_1['token'], user_1_dm, MIXED_QUERY_STR)
    output = search_v1(user_1['token'], MIXED_QUERY_STR)
    assert output['messages'][0]['message_id'] == 1
    assert output['messages'][0]['u_id'] == 1
    assert output['messages'][0]['message'] == MIXED_QUERY_STR
    assert output['messages'][1]['message_id'] == 2
    assert output['messages'][1]['u_id'] == 1
    assert output['messages'][1]['message'] == MIXED_QUERY_STR

def test_search_no_query_str_matches(clear_data, user_1, public_channel_1, user_1_dm):
    message_send_v1(user_1['token'], public_channel_1, MIXED_QUERY_STR)
    message_senddm_v1(user_1['token'], user_1_dm, MIXED_QUERY_STR)
    output = search_v1(user_1['token'], UPPER_QUERY_STR)
    assert output['messages'] == []

def test_search_lowercase_query_str(clear_data, user_1, public_channel_1, user_1_dm):
    message_send_v1(user_1['token'], public_channel_1, MIXED_QUERY_STR)
    message_senddm_v1(user_1['token'], user_1_dm, MIXED_QUERY_STR)
    message_send_v1(user_1['token'], public_channel_1, LOWER_QUERY_STR)
    message_senddm_v1(user_1['token'], user_1_dm, LOWER_QUERY_STR)
    message_send_v1(user_1['token'], public_channel_1, UPPER_QUERY_STR)
    message_senddm_v1(user_1['token'], user_1_dm, UPPER_QUERY_STR)
    output = search_v1(user_1['token'], LOWER_QUERY_STR)
    assert output['messages'][0]['message_id'] == 3
    assert output['messages'][0]['u_id'] == 1
    assert output['messages'][0]['message'] == LOWER_QUERY_STR
    assert output['messages'][1]['message_id'] == 4
    assert output['messages'][1]['u_id'] == 1
    assert output['messages'][1]['message'] == LOWER_QUERY_STR

def test_search_uppercase_query_str(clear_data, user_1, public_channel_1, user_1_dm):
    message_send_v1(user_1['token'], public_channel_1, MIXED_QUERY_STR)
    message_senddm_v1(user_1['token'], user_1_dm, MIXED_QUERY_STR)
    message_send_v1(user_1['token'], public_channel_1, LOWER_QUERY_STR)
    message_senddm_v1(user_1['token'], user_1_dm, LOWER_QUERY_STR)
    message_send_v1(user_1['token'], public_channel_1, UPPER_QUERY_STR)
    message_senddm_v1(user_1['token'], user_1_dm, UPPER_QUERY_STR)
    output = search_v1(user_1['token'], UPPER_QUERY_STR)
    assert output['messages'][0]['message_id'] == 5
    assert output['messages'][0]['u_id'] == 1
    assert output['messages'][0]['message'] == UPPER_QUERY_STR
    assert output['messages'][1]['message_id'] == 6
    assert output['messages'][1]['u_id'] == 1
    assert output['messages'][1]['message'] == UPPER_QUERY_STR

def test_search_numeric_query_str(clear_data, user_1, public_channel_1, user_1_dm):
    message_send_v1(user_1['token'], public_channel_1, NUMERIC_QUERY_STR)
    message_send_v1(user_1['token'], public_channel_1, MIXED_QUERY_STR)
    message_senddm_v1(user_1['token'], user_1_dm, MIXED_QUERY_STR)
    message_send_v1(user_1['token'], public_channel_1, UPPER_QUERY_STR)
    message_senddm_v1(user_1['token'], user_1_dm, UPPER_QUERY_STR)
    message_senddm_v1(user_1['token'], user_1_dm, NUMERIC_QUERY_STR)
    output = search_v1(user_1['token'], NUMERIC_QUERY_STR)
    assert output['messages'][0]['message_id'] == 1
    assert output['messages'][0]['u_id'] == 1
    assert output['messages'][0]['message'] == NUMERIC_QUERY_STR
    assert output['messages'][1]['message_id'] == 6
    assert output['messages'][1]['u_id'] == 1
    assert output['messages'][1]['message'] == NUMERIC_QUERY_STR

def test_search_symbols_query_str(clear_data, user_1, public_channel_1, user_1_dm):
    message_send_v1(user_1['token'], public_channel_1, MIXED_QUERY_STR)
    message_senddm_v1(user_1['token'], user_1_dm,SYMBOLS_QUERY_STR)
    message_send_v1(user_1['token'], public_channel_1, NUMERIC_QUERY_STR)
    message_senddm_v1(user_1['token'], user_1_dm, NUMERIC_QUERY_STR)
    message_send_v1(user_1['token'], public_channel_1, SYMBOLS_QUERY_STR)
    message_senddm_v1(user_1['token'], user_1_dm, UPPER_QUERY_STR)
    output = search_v1(user_1['token'], SYMBOLS_QUERY_STR)
    assert output['messages'][0]['message_id'] == 2
    assert output['messages'][0]['u_id'] == 1
    assert output['messages'][0]['message'] == SYMBOLS_QUERY_STR
    assert output['messages'][1]['message_id'] == 5
    assert output['messages'][1]['u_id'] == 1
    assert output['messages'][1]['message'] == SYMBOLS_QUERY_STR

def test_search_empty_query_str(clear_data, user_1, public_channel_1, user_1_dm):
    message_send_v1(user_1['token'], public_channel_1, MIXED_QUERY_STR)
    message_senddm_v1(user_1['token'], user_1_dm, MIXED_QUERY_STR)
    output = search_v1(user_1['token'], EMPTY_QUERY_STR)
    assert output['messages'] == []

def test_search_empty_database(clear_data, user_1):
    output = search_v1(user_1['token'], MIXED_QUERY_STR)
    assert output['messages'] == []

def test_search_substring(clear_data, user_1, user_2, public_channel_1, user_1_dm):
    channel_invite_v1(user_1['token'], public_channel_1, user_2['auth_user_id'])
    message_send_v1(user_1['token'], public_channel_1, NUMERIC_QUERY_STR)  
    message_senddm_v1(user_2['token'], user_1_dm, NUMERIC_QUERY_STR)
    message_send_v1(user_2['token'], public_channel_1, MIXED_QUERY_STR)
    message_senddm_v1(user_1['token'], user_1_dm, MIXED_QUERY_STR)
    message_send_v1(user_1['token'], public_channel_1, UPPER_QUERY_STR)
    message_senddm_v1(user_2['token'], user_1_dm, UPPER_QUERY_STR)
    message_send_v1(user_1['token'], public_channel_1, LOWER_QUERY_STR)
    message_senddm_v1(user_2['token'], user_1_dm, LOWER_QUERY_STR)
    output = search_v1(user_1['token'], SUB_STRING)
    assert output['messages'][0]['message_id'] == 3
    assert output['messages'][0]['u_id'] == 2
    assert output['messages'][0]['message'] == MIXED_QUERY_STR
    assert output['messages'][1]['message_id'] == 4
    assert output['messages'][1]['u_id'] == 1
    assert output['messages'][1]['message'] == MIXED_QUERY_STR
    assert output['messages'][2]['message_id'] == 7
    assert output['messages'][2]['u_id'] == 1
    assert output['messages'][2]['message'] == LOWER_QUERY_STR
    assert output['messages'][3]['message_id'] == 8
    assert output['messages'][3]['u_id'] == 2
    assert output['messages'][3]['message'] == LOWER_QUERY_STR

def test_search_multiple_channels(clear_data, user_1, user_2, public_channel_1, public_channel_2):
    channel_invite_v1(user_2['token'], public_channel_2, user_1['auth_user_id'])
    message_send_v1(user_1['token'], public_channel_1, MIXED_QUERY_STR)
    message_send_v1(user_2['token'], public_channel_2, MIXED_QUERY_STR)
    output = search_v1(user_1['token'], SUB_STRING)
    assert output['messages'][0]['message_id'] == 1
    assert output['messages'][0]['u_id'] == 1
    assert output['messages'][0]['message'] == MIXED_QUERY_STR
    assert output['messages'][1]['message_id'] == 2
    assert output['messages'][1]['u_id'] == 2
    assert output['messages'][1]['message'] == MIXED_QUERY_STR

def test_search_multiple_dms(clear_data, user_1, user_2, user_1_dm, user_2_dm):
    message_senddm_v1(user_1['token'], user_1_dm, MIXED_QUERY_STR)
    message_senddm_v1(user_2['token'], user_2_dm, MIXED_QUERY_STR)
    output = search_v1(user_1['token'], SUB_STRING)
    assert output['messages'][0]['message_id'] == 1
    assert output['messages'][0]['u_id'] == 1
    assert output['messages'][0]['message'] == MIXED_QUERY_STR
    assert output['messages'][1]['message_id'] == 2
    assert output['messages'][1]['u_id'] == 2
    assert output['messages'][1]['message'] == MIXED_QUERY_STR

def test_search_multiple_channels_and_dms(clear_data, user_1, user_2, user_1_dm, user_2_dm, public_channel_1, public_channel_2):
    channel_invite_v1(user_2['token'], public_channel_2, user_1['auth_user_id'])
    message_send_v1(user_1['token'], public_channel_1, MIXED_QUERY_STR)
    message_send_v1(user_1['token'], public_channel_1, NUMERIC_QUERY_STR)
    message_send_v1(user_2['token'], public_channel_2, NUMERIC_QUERY_STR)
    message_send_v1(user_2['token'], public_channel_2, MIXED_QUERY_STR)
    message_senddm_v1(user_1['token'], user_1_dm, SYMBOLS_QUERY_STR)
    message_senddm_v1(user_1['token'], user_1_dm, MIXED_QUERY_STR)
    message_senddm_v1(user_2['token'], user_2_dm, MIXED_QUERY_STR)
    message_senddm_v1(user_2['token'], user_2_dm, SYMBOLS_QUERY_STR)
    output = search_v1(user_1['token'], SUB_STRING)
    assert output['messages'][0]['message_id'] == 1
    assert output['messages'][0]['u_id'] == 1
    assert output['messages'][0]['message'] == MIXED_QUERY_STR
    assert output['messages'][1]['message_id'] == 4
    assert output['messages'][1]['u_id'] == 2
    assert output['messages'][1]['message'] == MIXED_QUERY_STR
    assert output['messages'][2]['message_id'] == 6
    assert output['messages'][2]['u_id'] == 1
    assert output['messages'][2]['message'] == MIXED_QUERY_STR
    assert output['messages'][3]['message_id'] == 7
    assert output['messages'][3]['u_id'] == 2
    assert output['messages'][3]['message'] == MIXED_QUERY_STR

def test_search_query_string_with_white_space(clear_data, user_1, public_channel_1, user_1_dm):
    message_send_v1(user_1['token'], public_channel_1, MIXED_QUERY_STR)
    message_senddm_v1(user_1['token'], user_1_dm, MIXED_QUERY_STR)
    output = search_v1(user_1['token'], WHITE_SPACE_QUERY_STR)
    assert output['messages'] == []

def test_search_user_not_in_channel(clear_data, user_1, user_2, public_channel_1):
    message_send_v1(user_1['token'], public_channel_1, MIXED_QUERY_STR)
    output = search_v1(user_2['token'], MIXED_QUERY_STR)
    assert output['messages'] == []

def test_search_user_not_in_dm(clear_data, user_1, user_2, user_3, user_1_dm):
    message_senddm_v1(user_1['token'], user_1_dm, MIXED_QUERY_STR)
    output = search_v1(user_3['token'], MIXED_QUERY_STR)
    assert output['messages'] == []

################################################################################
# notifications_get_v1 tests                                                   #
################################################################################

def test_notifications_get_invalid_token(clear_data, user_1):
    # Raises AccessError since token does not exist
    with pytest.raises(AccessError):
        notifications_get_v1(-1)
        
def test_notifications_get_empty(clear_data, user_1):
    # Checks if an empty list is returned for no notifications 
    assert notifications_get_v1(user_1['token']) == {'notifications': []}
    
def test_notifications_get_join_channel(clear_data, user_1, user_2, public_channel_1):
    # Tests notification for when user_2 is invited to join public_channel_1
    channel_invite_v1(user_1['token'], public_channel_1, user_2['auth_user_id'])
    notif = notifications_get_v1(user_2['token'])['notifications']
    assert len(notif) == 1
    assert notif[0]['channel_id'] == public_channel_1
    assert notif[0]['dm_id'] == -1
    assert notif[0]['notification_message'] == "johnsmith added you to John's Channel"
    
def test_notifications_get_join_dm(clear_data, user_1, user_2, user_1_dm):
    # Tests notification for when user_2 is added to user_1_dm
    notif = notifications_get_v1(user_2['token'])['notifications']
    assert len(notif) == 1
    assert notif[0]['channel_id'] == -1
    assert notif[0]['dm_id'] == user_1_dm
    assert notif[0]['notification_message'] == "johnsmith added you to johnsmith, terrynguyen"
    
def test_notifications_multi_channels(clear_data, user_1, user_2, public_channel_1, public_channel_2):
    channel_invite_v1(user_1['token'], public_channel_1, user_2['auth_user_id'])
    channel_invite_v1(user_2['token'], public_channel_2, user_1['auth_user_id'])
    notif = notifications_get_v1(user_1['token'])['notifications']
    assert len(notif) == 1
    assert notif[0]['channel_id'] == public_channel_2
    assert notif[0]['dm_id'] == -1
    assert notif[0]['notification_message'] == "terrynguyen added you to Terry's Channel"
    
def test_notifications_multi_dms(clear_data, user_1, user_2, user_1_dm, user_2_dm):
    notif = notifications_get_v1(user_1['token'])['notifications']
    assert len(notif) == 1
    assert notif[0]['channel_id'] == -1
    assert notif[0]['dm_id'] == user_2_dm
    assert notif[0]['notification_message'] == "terrynguyen added you to johnsmith, terrynguyen"    
    
def test_notifications_get_channel_tag(clear_data, user_1, user_2, public_channel_1):
    # Tests notifications for invite and tag (in a channel)
    channel_invite_v1(user_1['token'], public_channel_1, user_2['auth_user_id'])
    message_send_v1(user_1['token'], public_channel_1, 'Hello @terrynguyen')
    notif = notifications_get_v1(user_2['token'])['notifications']
    assert len(notif) == 2
    assert notif[0]['channel_id'] == public_channel_1
    assert notif[0]['dm_id'] == -1
    assert notif[0]['notification_message'] == "johnsmith tagged you in John's Channel: Hello @terrynguyen"
    assert notif[1]['channel_id'] == public_channel_1
    assert notif[1]['dm_id'] == -1 
    assert notif[1]['notification_message'] == "johnsmith added you to John's Channel"
    
def test_notifications_get_dm_tag(clear_data, user_1, user_2, user_1_dm):
    # Tests notifications for invite and tag (in a dm)
    message_senddm_v1(user_1['token'], user_1_dm, 'Welcome @terrynguyen')
    notif = notifications_get_v1(user_2['token'])['notifications']
    assert len(notif) == 2
    assert notif[0]['channel_id'] == -1
    assert notif[0]['dm_id'] == user_1_dm
    assert notif[0]['notification_message'] == "johnsmith tagged you in johnsmith, terrynguyen: Welcome @terrynguyen"
    assert notif[1]['channel_id'] == -1
    assert notif[1]['dm_id'] == user_1_dm
    assert notif[1]['notification_message'] == "johnsmith added you to johnsmith, terrynguyen"
    
def test_notifications_get_channel_and_dm(clear_data, user_1, user_2, public_channel_1, user_1_dm):
    # Testing notifications for invite and tag (in both a channel and a dm)
    channel_invite_v1(user_1['token'], public_channel_1, user_2['auth_user_id'])
    message_send_v1(user_1['token'], public_channel_1, "You joined the channel again @terrynguyen")
    message_senddm_v1(user_1['token'], user_1_dm, "Hey @terrynguyen, welcome to the dm")
    notif = notifications_get_v1(user_2['token'])['notifications']
    assert len(notif) == 4
    assert notif[0]['channel_id'] == -1
    assert notif[0]['dm_id'] == user_1_dm
    assert notif[0]['notification_message'] == "johnsmith tagged you in johnsmith, terrynguyen: Hey @terrynguyen, we"
    assert notif[1]['channel_id'] == public_channel_1
    assert notif[1]['dm_id'] == -1
    assert notif[1]['notification_message'] == "johnsmith tagged you in John's Channel: You joined the chann"
    assert notif[2]['channel_id'] == public_channel_1
    assert notif[2]['dm_id'] == -1
    assert notif[2]['notification_message'] == "johnsmith added you to John's Channel"
    assert notif[3]['channel_id'] == -1
    assert notif[3]['dm_id'] == user_1_dm
    assert notif[3]['notification_message'] == "johnsmith added you to johnsmith, terrynguyen"

def test_notifications_get_tag_edit(clear_data, user_1, user_2, public_channel_1):
    # Testing if a notification is raised when a message is edited to tag a user
    channel_invite_v1(user_1['token'], public_channel_1, user_2['auth_user_id'])
    msg = message_send_v1(user_2['token'], public_channel_1, 'Hello @johnsmith')
    message_edit_v1(user_1['token'], msg['message_id'], 'I have edited this @terrynguyen')
    user_1_notif = notifications_get_v1(user_1['token'])['notifications']
    assert len(user_1_notif) == 1
    assert user_1_notif[0]['channel_id'] == public_channel_1
    assert user_1_notif[0]['dm_id'] == -1
    assert user_1_notif[0]['notification_message'] == "terrynguyen tagged you in John's Channel: Hello @johnsmith"

    user_2_notif = notifications_get_v1(user_2['token'])['notifications']
    assert len(user_2_notif) == 2
    assert user_2_notif[0]['channel_id'] == public_channel_1
    assert user_2_notif[0]['dm_id'] == -1
    assert user_2_notif[0]['notification_message'] == "johnsmith tagged you in John's Channel: I have edited this @"
    assert user_2_notif[1]['channel_id'] == public_channel_1
    assert user_2_notif[1]['dm_id'] == -1
    assert user_2_notif[1]['notification_message'] == "johnsmith added you to John's Channel"

def test_notifications_get_react(clear_data, user_1, user_2):
    # Testing notifications for react
    dm = dm_create_v1(user_1['token'], [])
    dm_invite_v1(user_1['token'], dm['dm_id'], user_2['auth_user_id'])
    msg = message_senddm_v1(user_1['token'], dm['dm_id'], 'Hi @terrynguyen')
    message_react_v1(user_2['token'], msg['message_id'], 1)
    message_react_v1(user_1['token'], msg['message_id'], 1)
    user_1_notif = notifications_get_v1(user_1['token'])['notifications']
    assert len(user_1_notif) == 2
    assert user_1_notif[0]['channel_id'] == -1
    assert user_1_notif[0]['dm_id'] == dm['dm_id']
    assert user_1_notif[0]['notification_message'] == "johnsmith reacted to your message in johnsmith"
    assert user_1_notif[1]['channel_id'] == -1
    assert user_1_notif[1]['dm_id'] == dm['dm_id']
    assert user_1_notif[1]['notification_message'] == "terrynguyen reacted to your message in johnsmith"

    user_2_notif = notifications_get_v1(user_2['token'])['notifications']
    assert len(user_2_notif) == 2
    assert user_2_notif[0]['channel_id'] == -1
    assert user_2_notif[0]['dm_id'] == dm['dm_id']
    assert user_2_notif[0]['notification_message'] == "johnsmith tagged you in johnsmith: Hi @terrynguyen"
    assert user_2_notif[1]['channel_id'] == -1
    assert user_2_notif[1]['dm_id'] == dm['dm_id']
    assert user_2_notif[1]['notification_message'] == "johnsmith added you to johnsmith"

def test_notifications_get_max(clear_data, user_1, user_2, public_channel_1, public_channel_2):
    # Testing for up to 20 notifications
    i = 0
    while i < 25:
        message_send_v1(user_1['token'], public_channel_1, 'hi @johnsmith')
        i += 1
    channel_invite_v1(user_2['token'], public_channel_2, user_1['auth_user_id'])
    notif = notifications_get_v1(user_1['token'])['notifications']
    assert len(notif) == 20
    assert notif[0]['channel_id'] == public_channel_2
    assert notif[0]['dm_id'] == -1
    assert notif[0]['notification_message'] == "terrynguyen added you to Terry's Channel"
    assert notif[1]['channel_id'] == public_channel_1
    assert notif[1]['dm_id'] == -1
    assert notif[1]['notification_message'] == "johnsmith tagged you in John's Channel: hi @johnsmith"
