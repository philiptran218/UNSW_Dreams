# Test file for the auth function

from src.auth import auth_login_v1, auth_register_v1
from src.error import InputError
import pytest
from src.other import clear_v1
@pytest.fixture
def clear_data():
    clear_v1()

def test_pass(clear_data):
    auth_register_v1('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    auth_login_v1('validemail@gmail.com', '123abc!@#')

def test_unregistered_email(clear_data):
    auth_register_v1('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    with pytest.raises(InputError):
        auth_login_v1('didntusethis@gmail.com', '123abcd!@#')

def test_incorrect_pw(clear_data):
    auth_register_v1('validemail@gmail.com', 'abcd1234!', 'Kevin', 'Tran')
    with pytest.raises(InputError):
        auth_login_v1('validemail@gmail.com', 'abc123!')

def test_duplicate_email(clear_data):
    auth_register_v1('validemail@gmail.com', 'abcd1234!', 'James', 'Nguyen')
    with pytest.raises(InputError):
        auth_register_v1('validemail@gmail.com', 'abc123!', 'Jack', 'Tran')


        



# Cases to test
# valid email /
# invalid email
# incorrect pw
# Duplicate email
# invalid pw?   
