from src.database import data
from src.error import InputError, AccessError
import src.helper as helper


from src.auth import auth_register_v1, auth_login_v1
from src.channel import channel_messages_v1, channel_invite_v1
from src.channels import channels_create_v1, channels_listall_v1
from src.user import user_profile_v1
from src.database import data
from src.error import InputError, AccessError
from src.message import message_send_v1, message_senddm_v1
from src.dm import dm_create_v1
MIXED_QUERY_STR = "1. How's it going?"

import pytest
import random
import string

MAX_STRING_LENGTH = 1000

# Helper fucntion that when given a key mapping to a list in a dicionary, empties that list. 
def delete(aspect):
    ((data.get(aspect)).clear())

def is_already_in_channel(u_id, channel_id):
    selected_channel = None
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            selected_channel = channel
            break
            
    for member in selected_channel['all_members']:
        if member['u_id'] == u_id:
            return True
    return False
    
def is_already_in_dm(u_id, dm_id):
    selected_dm = None
    for dm in data['DM']:
        if dm['dm_id'] == dm_id:
            selected_dm = dm
            break
            
    for member in selected_dm['dm_members']:
        if member['u_id'] == u_id:
            return True
    return False

def is_query_str_in_msg(query_str, message):
    #print(query_str)
    #print(message)
    if query_str in message['message']:
        return True
    return False

def clear_v1():
    '''
    Function:
        Resets the internal data of the application to it's initial stateerases all information 
        about the users, erases all the channels and the messages.

    Arguments:
        This fucntion doesn't take any arguments.

    Exceptions:
        This function doesn't throw any excpetions.

    Return Value:
        This function doesn't return any value.
    '''
    delete('users')
    delete('channels')
    delete('messages')
    delete('DM')
    delete('sessions')
    delete('session_ids')


def search_v1(token, query_str):
    if not helper.is_valid_token(token):
        raise AccessError(description="Please enter a valid token")
    auth_user_id = helper.detoken(token)
    search_matches = {'messages': []}
    # Get len of string
    if len(query_str) > MAX_STRING_LENGTH:
        raise InputError(description="Query String is beyond 1000 characters")
    # Error check
    if query_str.isspace() or query_str == "":
        return search_matches
    for message in data['messages']:
        user_found = False
        if message['channel_id'] != -1:
            user_found = is_already_in_channel(auth_user_id, message['channel_id'])
        else:
            user_found = is_already_in_dm(auth_user_id, message['dm_id'])
        #print(user_found)
        #print(is_query_str_in_msg(query_str, message))
        if user_found == True and is_query_str_in_msg(query_str, message):
            search_matches['messages'].append(message)
    return search_matches