from database import data

def uid_listall():
'''
This function returns a list of all the u_id's of registered accounts
'''
    list_of_uid = []
    for user in data['users']
        list_of_uid.append(user['u_id'])
    return list_of_uid

def add_uid_to_channel(u_id, channel_id):
'''
This function appends a user to a channel
'''
    first_name = None
    last_name = None
    for user in data.users:
        if user['u_id'] == u_id:
            first_name = user['name_first']
            last_name = user['name_last']
    new_member = {
                'u_id': u_id,
                'name_first': first_name,
                'name_last': last_name,
                }   
    for channel in data.channels:
        if channel['channel_id'] == channel_id:
            channel['all_members'].append(new_member)

def channel_name(channel_id):
'''
Given the channel_id, this function returns the channel's name (string)
'''
    name = None
    for channel in data.channels:
        if channel['channel_id'] == channel_id:
            name = channel['name']
    return name

def channel_members(channel_id):
'''
Given the channel_id, this function returns a list of all the memebers in the 
channel. (List of dictionaries where each dictionary has u_id, first name and 
last name)
'''
    list_of_members = []
    for channel in data.channels:
        if channel['channel_id'] == channel_id:
            list_of_members = channel['all_members']
    return list_of_members

def channel_owners(channel_id):
'''
Given the channel_id, this function returns a list of all the owners in the 
channel (List of dictionaries where each dictionary has u_id, first name and 
last name)
'''
    list_of_owners = []
    for channel in data.channels:
        if channel['channel_id'] == channel_id:
            list_of_owners = channel['all_owners']
    return list_of_owners