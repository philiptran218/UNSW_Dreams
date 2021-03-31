from src.auth import auth_login_v1, auth_register_v1
from src.users import users_all_v1
from src.error import InputError, AccessError
import pytest
from src.other import clear_v1

INVALID_VALUE = -1

################################################################################
# Fixtures                                                                     #
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
def clear_data():
    clear_v1()

################################################################################
# users_all_v1 tests                                                           #
################################################################################

def expected_output_1():
    return  { 'users':
                [{
                'u_id': 1,
                'email': 'johnsmith@gmail.com',
                'name_first': 'John',
                'name_last': 'Smith',
                'handle_str': 'johnsmith',
                }]
            }

def expected_output_2():
    return  { 'users':
                [{
                'u_id': 1,
                'email': 'johnsmith@gmail.com',
                'name_first': 'John',
                'name_last': 'Smith',
                'handle_str': 'johnsmith',
                },
                {
                'u_id': 2,
                'name_first': 'Terry',
                'name_last': 'Nguyen',
                'email': 'terrynguyen@gmail.com',
                'handle_str': 'terrynguyen',
                },
                {
                'u_id': 3,
                'name_first': 'Phil',
                'name_last': 'Tran',
                'email': 'philt@gmail.com',
                'handle_str': 'philtran',
                }]
            }

def test_users_all_invalid_token(clear_data):
    with pytest.raises(AccessError):
        users_all_v1(INVALID_VALUE)

def test_users_all_valid_token(clear_data, user_1):
    assert users_all_v1(user_1['token']) == expected_output_1()

def test_users_all_multiple_users(clear_data, user_1, user_2, user_3):
    assert users_all_v1(user_1['token']) == expected_output_2()