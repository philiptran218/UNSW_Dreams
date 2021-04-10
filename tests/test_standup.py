import pytest
from src.error import AccessError, InputError
from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.other import clear_v1
from src.database import data
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
def create_long_msg():
    msg = ''
    for i in range(0,400):
        msg += str(i)
    return msg


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

def test_user_not_in_channel(clear_data,user1,user2,public_channel_1):
    with pytest.raises(AccessError):
        standup_start_v1(user_2['token'],public_channel_1,20)

def test_standup_start_invalid_token(clear_data,user_1,public_channel_1):
    with pytest.raises(AccessError):
        standup_start_v1(INVALID_TOKEN,public_channel_1,20)

def test_standup_start(clear_data,user_1,public_channel_1):
    standup_start_v1(user_1['token'],public_channel_1,20)
    assert(bool(data['standups']))


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
    standup_start_v1(user_1['token'],public_channel_1,20)
    active_standup_info = standup_active_v1(user_1['token'],public_channel_1)
    assert(active_standup_info['is_active'])


################################################################################
# standup_send_v1 tests                                                        #
################################################################################

def test_standup_send_invalid_channel_id(clear_data,user_1,public_channel_1):
    with pytest.raises(InputError):
        standup_send_v1(user_1['token'],INVALID_CHANNEL_ID,'hi')

def test_standup_send_invalid_msg_length(clear_data,user_1,public_channel_1,create_long_msg):
    standup_start_v1(user_1['token'],public_channel_1,20)
    with pytest.raises(InputError):
        standup_send_v1(user_1['token'],public_channel_1,create_long_msg)

def test_standup_send_not_active(clear_data,user_1,public_channel_1):
    with pytest.raises(InputError):
        standup_send_v1(user_1['token'],public_channel_1,'bye')

def test_standup_send_user_not_member(clear_data,user_1,user_2,public_channel_1):
    standup_start_v1(user_1['token'],public_channel_1,20)
    with pytest.raises(AccessError):
        standup_send_v1(user_2['token'],public_channel_1,'me')
#add one mroe to test








