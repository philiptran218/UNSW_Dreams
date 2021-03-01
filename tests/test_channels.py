from src.channels import channels_create_v1
from src.auth import auth_register_v1
import pytest
from src.error import InputError
from src.channels import channels_list_v1
from src.channels import channels_listall_v1
from src.other import clear_v1

@pytest.fixture
def clear():
    clear_v1

@pytest.fixture
def test_user():
    userid = auth_register_v1("validemail@g.com", "validpass", "validname","validname")
    return userid

def test_channels_list_v1_valid():
    clear()
    userid = test_user()
    assert(channels_list_v1(userid) == {"channels"})

def test_channels_list_v1_invalid():
    clear()
    inv_userid = test_user()
    with pytest.raises(InputError):
        assert(channels_list_v1(inv_userid) == {"channels"})

def test_channels_listall_v1_valid():
    clear()
    userid = test_user()
    assert(channels_listall_v1(userid) == {"channels"})

def test_channels_listall_v1_invalid():
    clear()
    inv_userid = test_user()
    with pytest.raises(InputError):
        assert channels_listall_v1(inv_userid) == {"channels"}