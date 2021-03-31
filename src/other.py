from src.database import data
from src.error import InputError, AccessError
import src.helper as helper

import pytest
import random
import string

MAX_STRING_LENGTH = 1000
TAG = 1
INVITE = 2

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
    
def get_channel_dm_name(channel_id, dm_id):
    if channel_id == -1:
        for dm in data['DM']:   # pragma: no branch
            if dm['dm_id'] == dm_id:
                return dm['dm_name']
    else:
        for channel in data['channels']:    # pragma: no branch
            if channel['channel_id'] == channel_id:
                return channel['name']

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
    delete('notifications')
    delete('sessions')
    delete('session_ids')


def search_v1(token, query_str):
    '''
    Function:
        Given a query string, return a collection of messages in all of the 
        channels/DMs that the user has joined that match the query
        
    Arguments:
        token (str) - this is the token of a registered user during their
                      session
        query_str (str) - this is the query that the user is searching for in 
                          the channels/DMs they are a member of
        
    Exceptions:
        InputError - occurs when the query_str is longer than 1000 characters
        AccessError - occurs when the user's token is not a valid token
        
    Return value:
        Returns a dictionary with key 'messages', which is a list of
        dictionaries of type {message}
    '''
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
        if user_found == True and is_query_str_in_msg(query_str, message):
            message_match = {
                            'message_id': message['message_id'],
                            'u_id': message['u_id'],
                            'message': message['message'],
                            'time_created': message['time_created']
                        }
            search_matches['messages'].append(message_match)
    return search_matches


def notifications_get_v1(token):
    '''
    Function:
        Returns the user's most recent 20 notifications
        
    Arguments:
        token (str) - this is the token of a registered user during their
                      session
                   
    Exceptions:
        AccessError - occurs when the user's token is not a valid token
        
    Return value:
        Returns a list of dictionaries containing types {channel_id, dm_id,
        notification_message}
    '''
    # Checks if token is valid
    if not helper.is_valid_token(token):
        raise AccessError(description="Please enter a valid token")
    auth_user_id = helper.detoken(token)
    notif_list = list(reversed(data['notifications']))
    recent_notifs = []
    # Searches for user's notifications in data['notifications']
    for notif in notif_list:
        chan_dm_name = get_channel_dm_name(notif['channel_id'], notif['dm_id'])
        if notif['u_id'] == auth_user_id:
            # If the notification is a tag
            if notif['type'] == TAG:
                notif_msg = helper.get_handle(notif['auth_user_id']) + ' tagged you in '
                notif_msg = notif_msg + chan_dm_name + ': ' + notif['message'][:20]
            # Else the notification is an invite (for iteration 2)
            else:
                notif_msg = helper.get_handle(notif['auth_user_id']) + ' added you to ' + chan_dm_name   
            notif_dict = {
                'channel_id': notif['channel_id'],
                'dm_id': notif['dm_id'],
                'notification_message': notif_msg
            }
            recent_notifs.append(notif_dict)
    return recent_notifs
