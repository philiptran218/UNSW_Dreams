from src.user import user_profile, user_profile_setname, user_profile_setemail_v2, user_profile_sethandle_v2
from src.auth import auth_login_v1, auth_register_v1
from src.error import InputError, AccessError
import pytest
from src.other import clear_v1


@pytest.fixture
def clear_data():
    clear_v1

#################################################################################
#                                                                               #
#                      user_profile_v1 testing functions                        #
#                                                                               #
#################################################################################

def test_valid_user_profile(clear_data):
    
    new_user = auth_register_v1("validemail@gmail.com", "Thisisagoodpassword123", "John", "Smith")
    user_setemail = user_profile(new_user.get('token'), new_user.get('u_id'))

    assert user_setemail.get('user').get('u_id') == new_user.get('u_id')
    assert user_setemail['user']['email'] == "validemail@gmail.com"
    assert user_setemail['user']['name_first'] == "John"
    assert user_setemail['user']['name_last'] == "Smith"
    assert user_setemail['user']['handle_str'] == "johnsmith"
    assert user_setemail == {
                            'user' : {
                                'u_id': new_user.get('u_id'),
                                'email': "validemail@gmail.com",
                                'name_first': "John",
                                'name_last': "Smith",
                                'handle_str': "johnsmith",
                            }
                        }


def test_profile_unregistered_user(clear_data):
    with pytest.raises(AccessError):
        user_profile('invalid_token', 'invalid_u_id')

    
def test_profile_invalid_u_id(clear_data):
    new_user = auth_register_v1("validemail@gmail.com", "Thisisagoodpassword123", "John", "Smith")
    with pytest.raises(InputError):
        user_profile(new_user.get('token'), 'invalid_u_id')




#################################################################################
#                                                                               #
#                      user_profile_setname_v2 testing functions                #
#                                                                               #
#################################################################################

def test_setname_first_pass(clear_data):
    new_user = auth_register_v1("validemail@gmail.com", "GoodPassword23", "Jason", "Bourne")
    user_token = new_user.get("token")
    user_id = new_user.get("u_id")
    return_user = user_profile_setname(user_token, "Jake", "Bourne")
    assert return_user == {}

def test_setname_last_pass(clear_data):
    new_user = auth_register_v1("validemail@gmail.com", "GoodPassword23", "Jason", "Bourne")
    user_token = new_user.get("token")
    user_id = new_user.get("u_id")
    return_user = user_profile_setname(user_token, "Jason", "Smith")
    assert return_user == {}

def test_setname_first_too_long(clear_data):
    new_user = auth_register_v1("validemail@gmail.com", "GoodPassword23", "Jason", "Bourne")
    user_token = new_user.get("token")
    user_id = new_user.get("u_id")
    
    with pytest.raises(InputError):
        user_profile_setname(user_token, "Thiscantpossiblybesomeonesnameasitistoolongandhardtoread", "Bourne")

def test_setname_first_too_short():
    new_user = auth_register_v1("validemail@gmail.com", "GoodPassword23", "Jason", "Bourne")    
    user_token = new_user.get("token")
    user_id = new_user.get("u_id")
    
    with pytest.raises(InputError):
        user_profile_setname(user_token, "", "Bourne")

def test_setname_last_too_long():
    new_user = auth_register_v1("validemail@gmail.com", "GoodPassword23", "Jason", "Bourne")    
    user_token = new_user.get("token")
    user_id = new_user.get("u_id")
    
    with pytest.raises(InputError):
        user_profile_setname(user_token, "Jason", "Thisisaverylonglonglonglonglonglonglonglonglastname")
def test_setname_last_too_short():
    new_user = auth_register_v1("validemail@gmail.com", "GoodPassword23", "Jason", "Bourne")    
    user_token = new_user.get("token")
    user_id = new_user.get("u_id")
    
    with pytest.raises(InputError):
        user_profile_setname(user_token, "Jason", "")

def test_setname_invalid_token():
    auth_register_v1("validemail@gmail.com", "GoodPassword23", "Jason", "Bourne")
    with pytest.raises(AccessError):
        user_profile_setname("invalid", "Not", "JasonBourne")
    


#################################################################################
#                                                                               #
#                      user_profile_setemail_v2 testing functions               #
#                                                                               #
#################################################################################

def test_setemail_pass(clear_data):
    new_user = auth_register_v1("validemail@gmail.com", "GoodPassword10", "Kevin", "Tran")
    user_token = new_user.get("token")
    user_profile_setemail_v2(user_token, "newemail@gmail.com")
    email = user_profile(user_token, new_user.get("u_id")).get("user").get("email")
    assert email == "newemail@gmail.com"

def test_invalid_email(clear_data):
    new_user = auth_register_v1("thisismyemail@gmail.com", "Thisisagoodpass12", "Alex", "Knight")
    with pytest.raises(InputError):
        user_profile_setemail_v2(new_user.get('token'), 'bademail')
    
def test_sameemail(clear_data):
    new_user = auth_register_v1("thisismyemail@gmail.com", "Thisisagoodpass12", "Alex", "Knight")
    with pytest.raises(InputError):
        user_profile_setemail_v2(new_user.get('token'), 'thisismyemail@gmail.com')

def test_email_taken(clear_data):
    new_user1 = auth_register_v1("thisismyemail@gmail.com", "Thisisagoodpass12", "Alex", "Knight")
    new_user2 = auth_register_v1("somethingcompletelyrandom@gmail.com", "Thisismyaccount24", "John", "Stone")

    with pytest.raises(InputError):
        user_profile_setemail_v2(new_user2.get('token'), 'thisismyemail@gmail.com')
    
def test_unregistered_user(clear_data):
    with pytest.raises(AccessError):
        user_profile('invalid_token', 'invalid_u_id')



#################################################################################
#                                                                               #
#                      user_profile_sethandle_v1 testing functions              #
#                                                                               #
#################################################################################

def test_handle_simple_pass(clear_data):
    new_user = auth_register_v1("myemail@gmail.com", "my12password", "Brad", "Lee")
    new_user_token = new_user.get("token")
    user_id = new_user.get("u_id")
    output = user_profile_sethandle_v2(user_token, "MyHandle")
    handle = output.get('user').get('handle_str')
    assert handle == "MyHandle"


def test_invalid_handle(clear_data):
    new_user = auth_register_v1("validemail@gmail.com", "PaSsWoRd321My", "Ash", "Ketchum")
    new_user_token = new_user.get("token")

    with pytest.raises(InputError):
        new_user.user_profile_sethandle(new_user_token, '')

def test_invalid_long_handle(clear_data):
    new_user = auth_register_v1("validemail@gmail.com", "PaSsWoRd321My", "Ash", "Ketchum")
    new_user_token = new_user.get("token")

    with pytest.raises(InputError):
        new_user.user_profile_sethandle(new_user_token, 'thisisaverylonghandlethatcantbeused')

def test_handle_taken(clear_data):
    new_user1 = auth_register_v1("validemail@gmail.com", "PaSsWoRd321My", "Ash", "Ketchum")
    new_user1_token = new_user1.get("token")
    user_profile_sethandle_v2(new_user1_token, "PokemonMaster")

    new_user2 = auth_register_v1("thisemail@gmail.com", "DifferentPassword", "Gary", "Oak")
    new_user2_token = new_user2.get("token")
    with pytest.raises(InputError):
        user_profile_sethandle_v2(new_user2_token, "PokemonMaster")

def test_sethandle_invalid_token(clear_data):
    auth_register_v1("thismyemail@gmail.com", "whatisapassword1", "Bill", "Gates")

    with pytest.raises(AccessError):
        user_profile_sethandle_v2("invalid", 'mycrosoft')
