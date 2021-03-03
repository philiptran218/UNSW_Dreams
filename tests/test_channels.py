from src.channels import channels_create_v1
from src.auth import auth_register_v1
import pytest
from src.error import InputError
from src.channels import channels_list_v1
from src.channels import channels_listall_v1
from src.other import clear_v1
from src.data import data

@pytest.fixture
def clear():
    clear_v1

@pytest.fixture
def test_user():
    userid = auth_register_v1("validemail@g.com", "validpass", "validname","validname")
    return userid

def test_channels_list_v1():
    clear
    userid = test_user
    assert(channels_list_v1(userid) == data["channels"])

def test_channels_listall_v1():
    clear
    userid = test_user
    assert(channels_listall_v1(userid) == data["channels"])

