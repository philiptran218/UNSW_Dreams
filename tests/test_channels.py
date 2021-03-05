from src.channels import channels_create_v1
from src.auth import auth_register_v1
import pytest
from src.error import AccessError, InputError
from src.channels import channels_list_v1
from src.channels import channels_listall_v1
from src.other import clear_v1
from src.data import data
from src.helper import is_valid_uid

@pytest.fixture
def clear():
    clear_v1

@pytest.fixture
def test_user():
    userid = auth_register_v1("validemail@g.com", "validpass", "validname","validname")
    return userid["auth_user_id"]

def test_channels_list_v1_valid(clear, test_user):
    assert(channels_list_v1(test_user) == data["channels"])

def test_channels_listall_v1_valid(clear, test_user):
    assert(channels_listall_v1(test_user) == data["channels"])

def test_channels_list_v1_invalid(clear, test_user):
    with pytest.raises(AccessError):
        channels_list_v1(test_user)

def test_channels_listall_v1_invalid(clear, test_user):
    with pytest.raises(AccessError):
        channels_listall_v1(test_user)



