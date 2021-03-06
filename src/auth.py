#import database
import pytest

registered_users = []

# To test whether the email is valid
REGEX = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

def auth_login_v1(email, password):

    # invalid email entered
    if not re.search(REGEX, email):
        raise error.InputError(description="Invalid Email")

    # Check whether the email used is registered with the site
    user_not_found = True
    for user in registered_users:
        if user.get('email') == email:
            u_id = user.get("u_id")
            user_not_found = False
            break

    if user_not_found:
        raise error.InputError(description="User not found")

    incorrect_password = True

    # Check if enter password matches the password used to register
    for user in users:
        if user.get('email') == email:
            if user.get('password') == password:
                incorrect_password = False

    if incorrect_password:
        raise error.InputError(description="Invalid Password")
 
    return {}

def auth_register_v1(email, password, name_first, name_last):
    if len(users) == 0:
        pass
    else:
        for data in users:
            if data.get("email") == email:
                raise error.InputError(description="Email is already taken")
    # check if email entered has the correct format
    if not re.search(REGEX, email):
        raise error.InputError(description="Invalid Email")
    
    # Check whether the password is valid
    if len(password) < 6:
        raise error.InputError(description="Invalid Password")
    
    # Check whether the first name is valid
    if len(name_first == 0 or name_first > 50):
        raise error.InputError(description="Invalid First Name")

    # Check whether the last name is valid
    if len(name_last == 0 or name_last >50):
        raise error.InputError(description="Invalid Last Name")
    
    # Check the number of registered users 
    number_users = len(data['users'])

    # Assign a permissions_id to users. The first user is defaulted as perm_id 1 and everyone else is perm_id 2
    if (number_users == 0):
        perm_id = 1
    else:
        perm_id = 2

    user = {
        'u_id': number_users + 1,
        'name_first': name_first,
        'name_last': name_last,
        'perm_id': perm_id,
        'password': password,
        'email': email
    }
    
    data['users'].append(user)
    return {}
