from src.database import data
from src.error import InputError, AccessError
import src.helper as helper

import pytest
import random
import string

MAX_STRING_LENGTH = 1000

# Helper fucntion that when given a key mapping to a list in a dictionary, empties that list. 
def delete(aspect):
    ((data.get(aspect)).clear())

def is_already_in_channel(u_id, channel_id):
    selected_channel = None
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            selected_channel = channel
            
    for member in selected_channel['all_members']:
        if member['u_id'] == u_id:
            return True
    return False
    
def is_already_in_dm(u_id, dm_id):
    selected_dm = None
    for dm in data['DM']:
        if dm['dm_id'] == dm_id:
            selected_dm = dm
            
    for member in selected_dm['dm_members']:
        if member['u_id'] == u_id:
            return True
    return False

def is_query_str_in_msg(query_str, message):
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
            message_match = {
                            'message_id': message['message_id'],
                            'u_id': message['u_id'],
                            'message': message['message'],
                            'time_created': message['time_created']
                        }
            search_matches['messages'].append(message_match)
    return search_matches