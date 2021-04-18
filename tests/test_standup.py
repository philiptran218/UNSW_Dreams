import pytest
from src.error import AccessError, InputError
from src.auth import auth_register_v1
from src.channel import channel_messages_v1, channel_join_v1
from src.channels import channels_create_v1
from src.other import clear_v1
from src.database import data
from src.standup import standup_active_v1, standup_send_v1, standup_start_v1
import time
from datetime import datetime, timezone, timedelta
INVALID_CHANNEL_ID = -1
INVALID_TOKEN = -1




################################################################################
#                                   Fixtures                                   #
################################################################################

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
def public_channel_1(user_1):
    channel = channels_create_v1(user_1['token'], "John's Channel", True)
    return channel['channel_id']
    
@pytest.fixture
def public_channel_2(user_2):
    channel = channels_create_v1(user_2['token'], "Terry's Channel", True)
    return channel['channel_id']

@pytest.fixture
def private_channel(user_2):
    channel = channels_create_v1(user_2['token'], "Terry's Channel", False)
    return channel['channel_id']

@pytest.fixture
def clear_data():
    clear_v1()


################################################################################
# standup_start_v1 tests                                                      #
################################################################################

def test_standup_start_invalid_channel_id(clear_data,user_1,public_channel_1):
    with pytest.raises(InputError):
        standup_start_v1(user_1['token'],INVALID_CHANNEL_ID,20)
    
def test_currently_running_standup(clear_data,user_1,public_channel_1):
    standup_start_v1(user_1['token'],public_channel_1,20)
    with pytest.raises(InputError):
        standup_start_v1(user_1['token'],public_channel_1,55)

def test_user_not_in_channel(clear_data,user_1,user_2,public_channel_1):
    with pytest.raises(AccessError):
        standup_start_v1(user_2['token'],public_channel_1,20)

def test_standup_start_invalid_token(clear_data,user_1,public_channel_1):
    with pytest.raises(AccessError):
        standup_start_v1(INVALID_TOKEN,public_channel_1,20)

def test_standup_start(clear_data,user_1,public_channel_1):
    time_end = datetime.now() + timedelta(0, 10)
    time_end = round(time_end.replace(tzinfo=timezone.utc).timestamp())
    standup_info = standup_start_v1(user_1['token'],public_channel_1,10)
    assert standup_active_v1(user_1['token'], public_channel_1)['is_active'] == True
    assert standup_info['time_finish'] == time_end

################################################################################
# standup_active_v1 tests                                                      #
################################################################################

def test_standup_active_invalid_channel_id(clear_data,user_1,public_channel_1):
    with pytest.raises(InputError):
        standup_active_v1(user_1['token'],INVALID_CHANNEL_ID)

def test_standup_active_invalid_token(clear_data,user_1,public_channel_1):
    with pytest.raises(AccessError):
        standup_active_v1(INVALID_TOKEN,public_channel_1)

def test_standup_active(clear_data,user_1,public_channel_1):
    time_end = datetime.now() + timedelta(0, 10)
    time_end = round(time_end.replace(tzinfo=timezone.utc).timestamp())
    standup_start_v1(user_1['token'],public_channel_1,10)
    active_standup_info = standup_active_v1(user_1['token'],public_channel_1)
    assert(active_standup_info['is_active'])
    assert active_standup_info['time_finish'] == time_end
    time.sleep(15)
    standup_info = standup_active_v1(user_1['token'], public_channel_1)
    assert standup_info['is_active'] == False
    assert standup_info['time_finish'] == None

def test_standup_inactive(clear_data, user_1, public_channel_1):
    standup_info = standup_active_v1(user_1['token'], public_channel_1)
    assert standup_info['is_active'] == False
    assert standup_info['time_finish'] == None

################################################################################
# standup_send_v1 tests                                                        #
################################################################################

def test_standup_send_invalid_channel_id(clear_data,user_1,public_channel_1):
    with pytest.raises(InputError):
        standup_send_v1(user_1['token'],INVALID_CHANNEL_ID,'hi')

def test_standup_send_invalid_msg_length(clear_data,user_1,public_channel_1):
    standup_start_v1(user_1['token'],public_channel_1,20)
    with pytest.raises(InputError):
        standup_send_v1(user_1['token'],public_channel_1,"i"*1001)

def test_standup_send_not_active(clear_data,user_1,public_channel_1):
    with pytest.raises(InputError):
        standup_send_v1(user_1['token'],public_channel_1,'bye')

def test_standup_send_user_not_member(clear_data,user_1,user_2,public_channel_1):
    standup_start_v1(user_1['token'],public_channel_1,20)
    with pytest.raises(AccessError):
        standup_send_v1(user_2['token'],public_channel_1,'me')

def test_standup_send_invalid_token(clear_data, user_1, public_channel_1):
    with pytest.raises(AccessError):
        standup_send_v1(INVALID_TOKEN, public_channel_1,'ds')
    
def test_standup_send_successful_message(clear_data, user_1, user_2, public_channel_1):
    channel_join_v1(user_2['token'], public_channel_1)
    time_end = datetime.now() + timedelta(0, 5)
    time_end = round(time_end.replace(tzinfo=timezone.utc).timestamp())
    standup_start_v1(user_1['token'], public_channel_1, 5)
    standup_send_v1(user_1['token'], public_channel_1, 'Welcome to the standup!')
    standup_send_v1(user_2['token'], public_channel_1, 'Hi there!')
    time.sleep(6)
    chan_msg = channel_messages_v1(user_1['token'], public_channel_1, 0)['messages']
    assert len(chan_msg) == 1
    assert chan_msg[0]['message'] == 'johnsmith: Welcome to the standup!\nterrynguyen: Hi there!'
    assert chan_msg[0]['u_id'] == user_1['auth_user_id']
    assert chan_msg[0]['message_id'] == 1
    assert chan_msg[0]['time_created'] == time_end

