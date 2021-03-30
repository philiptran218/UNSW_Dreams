from src.auth import auth_login_v1, auth_register_v1
from src.error import InputError
import pytest
from src.other import clear_v1

@pytest.fixture
def clear_data():
    clear_v1()

def test_pass(clear_data):
    # Testing if a single user can register and login
    assert auth_register_v1('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')['auth_user_id'] == 1
    assert auth_login_v1('validemail@gmail.com', '123abc!@#')['auth_user_id'] == 1

def test_valid_users(clear_data):
    # Testing if multiple users can register and login
    assert auth_register_v1('jsmith@gmail.com', 'password', 'John', 'Smith')['auth_user_id'] == 1
    assert auth_register_v1('anotheremail@gmail.com', 'stevenses', 'Steve', 'Steve')['auth_user_id'] == 2
    assert auth_register_v1('jasonbourne@gmail.com', 'itsjasonbourne', 'Jason', 'Bourne')['auth_user_id'] == 3
    assert auth_login_v1('jsmith@gmail.com', 'password')['auth_user_id'] == 1
    assert auth_login_v1('anotheremail@gmail.com', 'stevenses')['auth_user_id'] == 2
    assert auth_login_v1('jasonbourne@gmail.com', 'itsjasonbourne')['auth_user_id'] == 3

def test_unregistered_email(clear_data):
    # Testing login with an unregistered email
    auth_register_v1('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    with pytest.raises(InputError):
        auth_login_v1('didntusethis@gmail.com', '123abcd!@#')

def test_incorrect_pw(clear_data):
    # Testing login with incorrect password
    auth_register_v1('validemail@gmail.com', 'abcd1234!', 'Kevin', 'Tran')
    with pytest.raises(InputError):
        auth_login_v1('validemail@gmail.com', 'abc123!')

def test_duplicate_email(clear_data):
    # Testing registering with a used email
    auth_register_v1('validemail@gmail.com', 'abcd1234!', 'James', 'Nguyen')
    with pytest.raises(InputError):
        auth_register_v1('validemail@gmail.com', 'abc123!', 'Jack', 'Tran')

def test_invalid_email_format(clear_data):
    # Testing an email with invalid format
    with pytest.raises(InputError):
        auth_register_v1('invalidemail.com', 'goodpassword', 'John', 'Smith')
        
def test_invalid_password_length(clear_data):
    # Testing a password with less than 6 characters
    with pytest.raises(InputError):
        auth_register_v1('anewemail@gmail.com', 'passw', 'John', 'Smith')
        
def test_no_first_name(clear_data):
    # Testing first name with 0 characters
    with pytest.raises(InputError):
        auth_register_v1('anewemail@gmail.com', 'password', '', 'Smith')

def test_no_last_name(clear_data):
    # Testing last name with 0 characters
    with pytest.raises(InputError):
        auth_register_v1('anewemail@gmail.com', 'password', 'John', '')
        
def test_long_first_name(clear_data):
    # Testing first name with > 50 characters
    with pytest.raises(InputError):
        auth_register_v1('anewemail@gmail.com', 'password', 'Johnhasasuperduperreallylongnamethatjustdoesntmakeanysense', 'Smith')
    
def test_long_last_name(clear_data):
    # Testing last name with > 50 characters
    with pytest.raises(InputError):
        auth_register_v1('anewemail@gmail.com', 'password', 'John', 'Smithhasasuperduperreallylongnamethatjustdoesntmakeanysense')  
