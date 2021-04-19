from src.error import InputError, AccessError
from src.database import data, update_data
from src.helper import is_valid_token
from email.mime.text import MIMEText
from datetime import timezone, datetime
from src import config

import urllib.request
import os
import hashlib
import jwt
import smtplib
import secrets
import re

DEFAULT_IMG_URL = "https://t4.ftcdn.net/jpg/00/64/67/63/360_F_64676383_LdbmhiNM6Ypzb3FM4PPuFP9rHe7ri8Ju.jpg" 

# To test whether the email is valid
REGEX = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
SECRET = 'COMP1531PROJECT'
EMAIL_SENDER = 'compw09b@gmail.com'
EMAIL_PASSWORD = 'Computing1531'


def generate_handle(name_first, name_last):
    handle = name_first + name_last
    handle = handle.lower()
    handle = handle.replace("@", "")
    handle = handle.replace(" ", "")
    handle = handle.replace("\n", "")
    handle = handle.replace("\t", "")

    if len(handle) > 20:
        handle = handle[:20]
    else:
        pass
    handle_num = 0

    while is_handle_taken(handle):
        if len(handle) == 20:
            handle = handle[:len(handle) - len(str(handle_num))]
        elif len(str(handle_num)) != len(str(handle_num - 1)) and handle_num > 0:
            handle = handle[:len(handle) - len(str(handle_num - 1))]  
        elif handle_num >= 1:
             handle = handle[:len(handle) - len(str(handle_num))]
        handle += str(handle_num)
        handle_num += 1
    return handle

def is_handle_taken(handle):
    for user in data['users']:
        if user['handle_str'] == handle:
            return True
    return False
    
def generate_session_id():
    new_session_id = len(data['session_ids']) + 1
    data['session_ids'].append(new_session_id)
    return new_session_id

def auth_login_v1(email, password):
    '''
    Function:
        Allows existing users to login using their registered email and password.
        
    Arguments:
        email(char) - The email used to sign in
        password(char) - The password used to sign in
    
    Exceptions:
        InputError when any of:
            - The email used is not in the form of a real email
            - The email used has not yet been registered
            - The password entered is incorrect

    
    Return Values:
        This function returns u_id and token of the user    
    '''
    # invalid email entered
    if not re.search(REGEX, email):
        raise InputError("Invalid Email")

    # Check whether the email used is registered with the site
    user_not_found = True
    for user in data['users']:
        if user.get('email') == email:
            user_not_found = False
            break
    
    if user_not_found:
        raise InputError("User not found")
    
    incorrect_password = True
    enc_password = hashlib.sha256(password.encode()).hexdigest()
    # Check if enter password matches the password used to register
    for user in data['users']:
        if user.get('email') == email and user.get('password') == enc_password:
            incorrect_password = False
            break

    if incorrect_password:
        raise InputError("Invalid Password")
    # Payload for token generation
    payload = {
        'u_id': user['u_id'],
        'session_id': generate_session_id()
    }   
    token = jwt.encode(payload, SECRET, algorithm='HS256')
    session = {
        'u_id': payload['u_id'],
        'session_id': payload['session_id'],
        'token': token,
    }
    # Append the session information to sessions list in data
    data['sessions'].append(session) 
    update_data()   
    return {
        'token': token,
        'auth_user_id': user['u_id']
    }

def auth_register_v1(email, password, name_first, name_last):
    '''
    Function:
        Allows new users to register
        
    Arguments:
        email(char) - The email used to sign up
        password(char) - The password used to sign up
        name_first - The user's first name
        name_last - The user's last name
    
    Exceptions:
        InputError when any of:
            - The email entered is not in the form of a real email
            - The email entered has been taken
            - The password entered is invalid
            - The first name is zero characters or more than 50 characters
            - The last name is zero characters or more than 50 characters

    Return Values:
        This function returns u_id and token of the user    
    '''
    for user in data['users']:
        if user.get("email") == email:
            raise InputError("Email is already taken")
    # check if email entered has the correct format
    if not re.search(REGEX, email):
        raise InputError("Invalid Email")
    
    # Check whether the password is valid
    if len(password) < 6:
        raise InputError("Invalid Password")
    
    # Check whether the first name is valid
    if len(name_first) == 0 or len(name_first) > 50:
        raise InputError("Invalid First Name")

    # Check whether the last name is valid
    if len(name_last) == 0 or len(name_last) > 50:
        raise InputError("Invalid Last Name")
    
    # Check the number of registered users 
    number_users = len(data['users'])

    # Assign a permissions_id to users. The first user is defaulted as perm_id 1 and everyone else is perm_id 2
    if (number_users == 0):
        perm_id = 1
    else:
        perm_id = 2

    # Checking the time, useful for the stats log.

    time = datetime.now()
    time = time.timestamp()
    time_issued = int(time)

    urllib.request.urlretrieve(DEFAULT_IMG_URL, f"src/static/{number_users + 1}.jpg")

    user = {
        'u_id': number_users + 1,
        'name_first': name_first,
        'name_last': name_last,
        'perm_id': perm_id,
        'password': hashlib.sha256(password.encode()).hexdigest(),
        'email': email,
        'handle_str': generate_handle(name_first, name_last),
        'profile_img_url': config.url + f"static/{number_users + 1}.jpg",
        'stats_log': 
            {
                'channels_joined': [{'num_channels_joined': 0, 'time_stamp': time_issued}],
                'dms_joined': [{'num_dms_joined': 0, 'time_stamp': time_issued}],
                'messages_sent': [{'num_messages_sent': 0, 'time_stamp': time_issued}],
                'involvement_rate': 0.0,
            }
    }
    
    data['users'].append(user)
    update_data()
    return auth_login_v1(email, password)

def auth_logout_v1(token):
    '''
    Function:
        Allows logged in users to log out
        
    Arguments:
        token(str) - this is the token of a registered user during their session
    
    Exceptions:
        AccessError - When the token is invalid

    Return Values:
        This function will return "is_sucess" when successful
    '''
    
    if not is_valid_token(token):
        raise AccessError(description='Please enter a valid token')
   
    for sesh in data['sessions']:
        if sesh.get('token') == token:
            data['sessions'].remove(sesh)
    update_data()
    return {
        'is_success': True,
    }
    
def is_valid_email(email):
    valid_email = False
    for user in data['users']:
        if user['email'] == email:
            valid_email = True
    return valid_email
    
def already_requested(email):
    requested = False
    for request in data['password_resets']:
        if request['email'] == email:
            requested = True
    return requested
    
def send_reset_code(email, reset_code):
    email_msg = MIMEText(f'Your unique code to reset your password is {reset_code}')
    email_msg['From'] = EMAIL_SENDER
    email_msg['To'] = email
    email_msg['Subject'] = 'Code to reset password in Dreams'
   
    email_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    email_server.login(EMAIL_SENDER, EMAIL_PASSWORD)
    email_server.sendmail(EMAIL_SENDER, email, email_msg.as_string())
    email_server.quit()

def auth_passwordreset_request_v1(email):
    '''
    Function:
        Given an email address, if the user is a registered user, sends them an 
        email containing a specific secret code, that when entered in 
        auth_passwordreset_reset, shows that the user trying to reset the 
        password is the one who got sent this email.
        
    Arguments: 
        email (str) - the email of the user requesting to change their password 
        
    Exceptions:
        InputError when any of:
            - email does not belong to a registered user
            - email is not in the correct format
            
    Return Values:
        Returns an empty dictionary {}
    '''
    # Invalid email format entered
    if not re.search(REGEX, email):
        raise InputError(description="Invalid email")
    # Checks if email belongs to a registered user
    if not is_valid_email(email):
        raise InputError(description="Email does not belong to a registered user")

    # Creates a base64 encoded string which may be longer than 10 characters
    reset_code = secrets.token_urlsafe(10)
    
    # If user requests another reset code, their old reset code is updated to 
    # the new one
    if already_requested(email):
        for request in data['password_resets']:
            if request['email'] == email:
                request.update({'reset_code': reset_code})
    # Otherwise a new request is appended to the password_resets list 
    else:
        new_request = {
            'email': email,
            'reset_code': reset_code
        }
        data['password_resets'].append(new_request)   
    send_reset_code(email, reset_code)    
    update_data()
    return {}
    
def is_valid_reset_code(reset_code):
    code_found = False
    for request in data['password_resets']:
        if request['reset_code'] == reset_code:
            code_found = True
    return code_found
    
def get_request_email(reset_code):
    # Returns the email associated with the reset_code
    # Assumes that the reset_code passed in is valid
    email = None
    for request in data['password_resets']:
        if request['reset_code'] == reset_code:
            email = request['email']
    return email

def auth_passwordreset_reset_v1(reset_code, new_password):    
    '''
    Function:
        Given a reset code for a user, set that user's new password to the 
        password provided
        
    Arguments: 
        reset_code (str) - the code which allows the user to reset their password
        new_password (str) - this is the user's new chosen password
        
    Exceptions:
        InputError when any of:
            - reset_code is not a valid reset code 
            - password entered is less than 6 characters long
            
    Return Values:
        Returns an empty dictionary {}
    '''
    # Check if the reset code is a valid code
    if not is_valid_reset_code(reset_code):
        raise InputError(description="Invalid password reset code")
    # Check if the password is longer than 6 characters
    if len(new_password) < 6:
        raise InputError(description="Invalid password")

    user_email = get_request_email(reset_code)
    # Updating the password of the user
    for user in data['users']:
        if user['email'] == user_email:
            user.update({'password': hashlib.sha256(new_password.encode()).hexdigest()})
    
    # The request is removed once password is updated  
    for request in data['password_resets']:
        if request['reset_code'] == reset_code:
            data['password_resets'].remove(request)
    update_data()
    return {}

