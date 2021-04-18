from src.auth import auth_login_v1, auth_register_v1, auth_logout_v1
from src.auth import auth_passwordreset_request_v1, auth_passwordreset_reset_v1
from src.error import InputError, AccessError
import pytest
from src.other import clear_v1

INVALID_RESET_CODE = -1

@pytest.fixture
def clear_data():
    clear_v1()

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

################################################################################
# auth_login_v1 tests                                                          #
################################################################################

def test_pass(clear_data):
    # Testing if a single user can register and login
    assert auth_register_v1('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')['auth_user_id'] == 1
    assert auth_login_v1('validemail@gmail.com', '123abc!@#')['auth_user_id'] == 1

def test_multiple_valid_users(clear_data):
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

def test_login_invalid_email(clear_data):
    # Testing login with invalid email
    with pytest.raises(InputError):
        auth_login_v1("wrong_format.com", "password")

################################################################################
# auth_register_v1 tests                                                       #
################################################################################

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

def test_repeat_long_handle(clear_data):
    # Creating handles longer than 20 characters, and tests adding multiple users
    # Also tests multiple users with same name
    i = 0
    j = 1
    while i < 12:
        user_info = auth_register_v1(str(i) + 'anewemail@gmail.com', 'password', 'John', 'Smith')
        assert user_info['auth_user_id'] == j
        i += 1
        j += 1
    while i < 14:
        user_info = auth_register_v1(str(i) + 'anothernewemail@gmail.com', 'password', 'Johnsmithus', 'Smithjohnus')
        assert user_info['auth_user_id'] == j
        i += 1
        j += 1

################################################################################
#   auth_logout_v1 testing functions                                           #
################################################################################

def test_valid_logout_token(clear_data):
    # Testing the logout function when a valid token is used
    user = auth_register_v1("test@gmail.com", "validpassword123","Firstname", "Lastname")
    assert auth_logout_v1(user.get('token')).get('is_success') == True

def test_invalid_logout(clear_data):
    # Testing the logout function when an invalid token is used
    user = auth_register_v1("test@gmail.com", "validpassword123","Firstname", "Lastname")
    with pytest.raises(AccessError):
        auth_logout_v1(user.get('invalid_token')).get('is_success')
        

################################################################################
# auth_passwordreset_request tests                                             #
################################################################################

def test_password_request_invalid_email(clear_data, user_1):
    with pytest.raises(InputError):
        auth_passwordreset_request_v1("johnsmithy@gmail.com")

def test_password_request_invalid_email_format(clear_data, user_1):
    with pytest.raises(InputError):
        auth_passwordreset_request_v1("john")
        
'''
Our group did not write valid pytests for auth_passwordreset_request_v1 as they
could not be tested in a black box manner. However, these cases were tested 
using the frontend.
'''
################################################################################
# auth_passwordreset_reset tests                                               #
################################################################################

def test_password_reset_invalid_code(clear_data, user_1):
    auth_login_v1("johnsmith@gmail.com", "password")
    auth_passwordreset_request_v1("johnsmith@gmail.com")
    with pytest.raises(InputError):
        auth_passwordreset_reset_v1(INVALID_RESET_CODE, 'newpassword')
        
'''
Our group did not write valid pytests for auth_passwordreset_reset_v1 as they
could not be tested in a black box manner. Testing for an invalid password was
also unable to be done as it required the reset_code. However, these cases were 
tested using the frontend.
'''

