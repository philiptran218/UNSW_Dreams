from src.error import InputError, AccessError
from src import config
import re
from json import dumps, load
from src.database import data, update_data
from src.helper import is_valid_token, is_valid_uid, detoken, is_already_in_channel
from datetime import timezone, datetime
import urllib.request
import urllib.error
import sys
from PIL import Image

REGEX = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

def get_involvement_rate(user_channels, user_dms, user_msg):

    num_messages = len(data['messages'])
    num_channels = len(data['channels'])
    num_dms = len(data['DM'])

    denom_sum = num_dms + num_messages + num_channels
    numer_sum = user_channels + user_dms + user_msg

    if denom_sum == 0:
        involve_rate = 0.0
    else:
        involve_rate = float(numer_sum/denom_sum)
        
    return involve_rate

def user_profile_v1(token, u_id):
    """
    Function:
        This function return information about the user, including their u_id, email, first and last name and their handle 

    Arguments:
        token(str) - token of the registered user.
        u_id(int) - u_id of the person whose information is being displayed 

    Exceptions:
        AccessError - If token is invalid
                    - If u_id is invalid

    Return Type:
        Function returns user's u_id, email, first name, last name and handle
    """

    
    if not is_valid_token(token):
        raise AccessError(description="Token invalid")

    if not is_valid_uid(u_id):
        raise InputError(description="Invalid u_id")
    
    for user in data['users']:
        if user['u_id'] == u_id:
            user_details = {
                'user': {
                    'u_id': user.get('u_id'),
                    'email': user.get('email'),
                    'name_first': user.get('name_first'),
                    'name_last': user.get('name_last'),
                    'handle_str': user.get('handle_str'),
                    'profile_img_url': user.get('profile_img_url')
                },
            }
    return user_details

        
def user_profile_setname_v1(token, name_first, name_last):
    """
    Function:
        This function allows users to change their first and/or last name

    Arguments:
        token(str) - token of the registered user.
        name_first - the first name that the user wants to change to
        name_last - the last name that the user wants to change to

    Exceptions:
        AccessError - If token is invalid
        
        InputError - If the name/s entered are zero or more than 50 characters long

    Return Type:
        Function does not return anything
    """
       
    if not is_valid_token(token):
        raise AccessError(description="Token invalid")
    auth_user_id = detoken(token)
    if (len(name_first) < 1) or (len(name_first) > 50):
        raise InputError(description="First name is invalid")
    
    if (len(name_last) < 1) or (len(name_last) > 50):
        raise InputError(description="Last name is invalid")

    for user in data['users']:
        if user['u_id'] == auth_user_id:
            user['name_first'] = name_first
            user['name_last'] = name_last
    update_data()
    return {}
        

def user_profile_setemail_v1(token, email):
    """
    Function:
        This function allows users to changed their email

    Arguments:
        token(str) - token of the registered user.
        email(str) - the new email

    Exceptions:
        AccessError - If token is invalid

        InputError - If the email is already taken
                   - If the email is invalid

    Return Type:
        Function does not return anything
    """
    if not is_valid_token(token):
        raise AccessError(description="Token invalid")
    auth_user_id = detoken(token)
    #test for invalid email
    for user in data['users']:
        if user.get("email") == email:
            raise InputError(description="Email is already taken")

    if not re.search(REGEX, email):
        raise InputError(description="Invalid Email")
   
    for user in data['users']:
        if user.get('u_id') == auth_user_id:
            user.update({'email': email})
    update_data()
    return {}

def user_profile_sethandle_v1(token, handle_str):
    """
    Function:
        This function allows users to change their handle

    Arguments:
        token(str) - token of the registered user.
        handle(str) - the new handle the user wants to change to

    Exceptions:
        AccessError - If token is invalid
        
        InputError - If the handle is less than 3 or more than 20 characters
                   - If the handle is already taken

    Return Type:
        Function does not return anything
    """


    if not is_valid_token(token):
        raise AccessError(description="Token invalid")
    auth_user_id = detoken(token)
    if len(handle_str) < 3 or len(handle_str) > 20:
        raise InputError(description="Handle_str invalid")
    
    for user in data['users']:
        if user['handle_str'] == handle_str:
            raise InputError(description="Handle taken")

    for user in data['users']:
        if user['u_id'] == auth_user_id:
            user.update({'handle_str': handle_str})
    update_data()
    return {}

def user_profile_uploadphoto_v1(token, img_url, x_start, y_start, x_end, y_end):
    '''
    Function:
       Function allows a user to update their profile picture to a picture of their choosing. 

    Arguments:
        token (str) - token of a registered user during their session
        img_url(str) - url of the image that you want to be placed through url
        x_start(int) - starting x coordinate of the image.
        x_end(int) - ending x coordinate of the image.
        y_start(int) - starting y coordinate of the image.
        y_end(int) - ending y coordinate of the image.

    Exceptions:     
        AccessError: - the user who calls the fucntion is not a valid user (invalid token).
        InputError when:
            - img_url returns a HTTP status other then 200
            - any of the coordinates are not in dimensions of image url
            - image uploaded is not a JPEG

    Return Type:
        This function has no return value. 
    ''' 
    if not is_valid_token(token):
        raise AccessError(description="Token invalid")
    u_id = detoken(token)

    if not img_url.endswith('.jpg'):
        raise InputError(description="Image is not of specified type")

    try:
        urllib.request.urlopen(img_url)
    except urllib.error.HTTPError:
        raise InputError(description="Url is not valid")

    urllib.request.urlretrieve(img_url, f"src/static/{u_id}.jpg")
    
    max_y = Image.open(f"src/static/{u_id}.jpg", 'r').height
    max_x = Image.open(f"src/static/{u_id}.jpg", 'r').width

    if x_start < 0 or x_end < 0 or y_start < 0 or y_end < 0:
        raise InputError(description="Coordinates not in dimensions of image")

    if x_start > max_x or x_end > max_x or y_start > max_y or y_end > max_y:
        raise InputError(description="Coordinates not in dimensions of image")

    if x_start > x_end or y_start > y_end:
        raise InputError(description="Coordinates are invalid")

    for user in data['users']:
        if user['u_id'] == u_id:
            user['profile_img_url'] = config.url + f"static/{u_id}.jpg"

    update_data()

    image_object = Image.open(f"src/static/{u_id}.jpg")
    cropped_image = image_object.crop((x_start, y_start, x_end, y_end))
    cropped_image.save(f"src/static/{u_id}.jpg")

    return {}

def user_stats_v1(token):
    '''
    Function:
       returns a dictionary of the user's personal stats, relating to their dreams usage.

    Arguments:
        token (str) - token of a registered user during their session

    Exceptions:     
        AccessError - the user who calls the fucntion is not a valid user (invalid token).

    Return Type:
        This function returns the users_stats data type; a dictionary with the stats and the time at which it was measured.
    ''' 

    if is_valid_token(token) == False:
        raise AccessError(description='token invalid')

    token_u_id = detoken(token)

    user_channels = 0
    user_dms = 0
    user_msg = 0

    for channel in data['channels']:
        if is_already_in_channel(token_u_id, channel['channel_id']) == True:
            user_channels += 1

    for dm in data['DM']:
        for member in dm['dm_members']:
            if member['u_id'] == token_u_id:
                user_dms += 1

    for msg in data['messages']:
        if msg['u_id'] == token_u_id:
            user_msg += 1

    involve_rate = get_involvement_rate(user_channels, user_dms, user_msg)

    time = datetime.today()
    time = time.replace(tzinfo=timezone.utc).timestamp()
    time_issued = round(time)

    stats_log = {
        'channels_joined': [{'num_channels_joined': user_channels, 'time_stamp': time_issued}],
        'dms_joined': [{'num_dms_joined': user_dms, 'time_stamp': time_issued}],
        'messages_sent': [{'num_messages_sent': user_msg, 'time_stamp': time_issued}],
        'involvement_rate': involve_rate,
    }

    for user in data['users']:
        if user['u_id'] == token_u_id:
            user['stats_log'].append(stats_log)
            update_data()
    
    return {'user_stats': stats_log}