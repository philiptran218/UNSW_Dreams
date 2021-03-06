from src.database import data, update_data
from src.error import InputError, AccessError
import src.helper as helper

import pytest
import random
import string
import os

MAX_STRING_LENGTH = 1000
TAG = 1
INVITE = 2
REACT = 3

# Helper function that when given a key mapping to a list in a dictionary, empties that list. 
def delete(aspect):
    ((data.get(aspect)).clear())

def is_query_str_in_msg(query_str, message):
    if query_str in message['message']:
        return True
    return False

# channel_id and dm_id must be validated before running this function.
def get_channel_dm_name(channel_id, dm_id):
    name = None
    if channel_id == -1:
        for dm in data['DM']:  
            if dm['dm_id'] == dm_id:
                name = dm['dm_name']
    else:
        for channel in data['channels']:
            if channel['channel_id'] == channel_id:
                name = channel['name']
    return name

def clear_v1():
    '''
    Function:
        Resets the internal data of the application to it's initial state, erases all information 
        about the users, channels, messages, DMs, notifications, sessions, stats and standups.

    Arguments:
        This fucntion doesn't take any arguments.

    Exceptions:
        This function doesn't throw any excpetions.

    Return Value:
        This function doesn't return any value.
    '''
    # Deletes all data currently stored in the database.
    delete('users')
    delete('channels')
    delete('messages')
    delete('DM')
    delete('notifications')
    delete('sessions')
    delete('session_ids')
    delete('stats_log')
    delete('standups')
    delete('password_resets')

    # Deletes all the profile images that are stored in the folder "static"
    imgs = os.listdir("src/static")
    for img in imgs:
        if img != "description.txt":
            os.remove(f"src/static/{img}")

    update_data()
    return {}


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
            user_found = helper.is_already_in_channel(auth_user_id, message['channel_id'])
        else:
            user_found = helper.is_already_in_dm(auth_user_id, message['dm_id'])
        if user_found and is_query_str_in_msg(query_str, message):
            message_match = {
                            'message_id': message['message_id'],
                            'u_id': message['u_id'],
                            'message': message['message'],
                            'time_created': message['time_created'],
                            'reacts': helper.get_reacts(auth_user_id, message['reacts']),
                            'is_pinned': message['is_pinned'],
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
    notif_count = 0
    # Searches for user's notifications in data['notifications']
    for notif in notif_list:
        chan_dm_name = get_channel_dm_name(notif['channel_id'], notif['dm_id'])
        user_handle = helper.get_handle(notif['auth_user_id'])
        if notif['u_id'] == auth_user_id and notif_count < 20:
            # If the notification is a tag
            if notif['type'] == TAG:
                notif_msg = user_handle + ' tagged you in ' + chan_dm_name + ': ' + notif['message'][:20]
            # If the notification is an invite
            elif notif['type'] == INVITE:
                notif_msg = user_handle + ' added you to ' + chan_dm_name 
            # Else the notification must be a react
            else:
                notif_msg = user_handle + ' reacted to your message in ' + chan_dm_name
            notif_dict = {
                'channel_id': notif['channel_id'],
                'dm_id': notif['dm_id'],
                'notification_message': notif_msg
            }
            recent_notifs.append(notif_dict)
            notif_count += 1
    return {'notifications': recent_notifs}

