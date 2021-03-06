# Test file for the auth function

from auth import auth_login_v1, auth_register_v1
import pytest

def test_pass():
    auth_register_v1('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    auth_login_v1('validemail@gmail.com', '123abc!@#')

def test_unregistered_email():
    auth_register_v1('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    with pytest.raises(InputError) as e:
        auth_login_v1('didntusethis@gmail.com', '123abcd!@#')

def test_incorrect_pw():
    auth_register_v1('validemail@gmail.com', 'abcd1234!', 'Kevin', 'Tran')
    with pytest.raises(InputError) as e:
        auth_login_v1('validemail@gmail.com', 'abc123!')

def test_duplicate_email():
    auth_register_v1('validemail@gmail.com', 'abcd1234!', 'James', 'Nguyen')
    with pytest.raises(InputError) as e:
        auth_register_v1('validemail@gmail.com', 'abc123!', 'Jack', 'Tran')


        



# Cases to test
# valid email /
# invalid email
# incorrect pw
# Duplicate email
# invalid pw?   
