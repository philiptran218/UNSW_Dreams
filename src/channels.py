from src.error import InputError, AccessError
from src.database import data
from src.helper import is_valid_uid,get_first_name, get_last_name, get_email, get_handle

def channels_listall_v1(auth_user_id):
    """ 
    Code takes input auth_user_id and sends it through helper function is_valid_id. If id is valid,  
    then function loops through channel list inside data dictionary (inside database.py) and takes 
    the channel_id and channel_name of all channels. It then appends them into a dictionary inside  
    a new list, which is the data that is returned. 

    Not all of data[channels] is returned as additional components have been added in for  
    functionality. These are long and not needed in output (see assumptions.md for more info) 

    If id is false, AccessError exception is thrown as per specification. 
    """ 
    channel_list = []
    if is_valid_uid(auth_user_id) == True:
        for channel in data["channels"]:
            output = {
                "channel_id": channel["channel_id"],
                "name": channel["name"]
            }
            channel_list.append(output)
        return {'channels': channel_list}
    else:
        raise AccessError("Please enter a valid user id")

def channels_list_v1(auth_user_id): 
    """ 
    Code takes input auth_user_id and sends it through helper function is_valid_id. Very similar 
    functionality to channels_listall, except for the looping through of all_members list.  
    This checks to see if a user is actually inside the channel (assuming the id is valid. Once 
    user is verified to be inside the channel, the channel_id and channel_name is taken and  
    appended into dictionary inside a new list, which is the returned data type.    

    Not all of data[channels] is returned as additional components have been added in for  
    functionality. These are long and not needed in output (see assumptions.md for more info) 

    If id is false, AccessError exception is thrown as per specification. 
    """ 
    channel_list = []
    if is_valid_uid(auth_user_id) == True:
        for channel in data["channels"]:
            for member in channel["all_members"]:
                if member["u_id"]== auth_user_id:
                    output = {
                        "channel_id": channel["channel_id"],
                        "name":channel["name"]
                    }
                    channel_list.append(output)
        return {'channels': channel_list}
    else:
        raise AccessError("Please enter a valid user id")

def channels_create_v1(auth_user_id, name, is_public):
    '''
    channels_create_v1 - a function that creates a new channel with a given name that is either a public or private channel.

    Arguments:
        <auth_user_id> (int)    - <a unique id number given to a user on regestration>
        <name> (string)    - <the name of the channel that the user wants to create>
        <is_public> (Bool)    - <boolean value corresponding to a  public or private channel>
        ...

    Exceptions:
        InputError  - Occurs when the name given for the channel is more than 20 characters long
        AccessError - Occurs when the user trying to create a channel is not registred on the app

    Return Value:
        Returns <{channel_id}
    '''

    if len(name) > 20:
        raise InputError('channel name must be less than 20 characters')

    if not is_valid_uid(auth_user_id,):
        raise AccessError('user_id is invalid')
    
    channel_id = len(data['channels'])+1
    new_chan = {
        'channel_id': channel_id,
        'name':name,
        'all_members':[
            {
                'u_id':auth_user_id,
                'name_first':get_first_name(auth_user_id),
                'name_last' :get_last_name(auth_user_id),
                'email': get_email(auth_user_id),
                'handle_str': get_handle(auth_user_id),
            },
        ],
        'owner_members':[
            {
                'u_id':auth_user_id,
                'name_first':get_first_name(auth_user_id),
                'name_last' :get_last_name(auth_user_id),
                'email': get_email(auth_user_id),
                'handle_str': get_handle(auth_user_id),
            },
        ],
        'is_public': is_public,
    }
    data['channels'].append(new_chan)
    return {
        'channel_id': channel_id,
    }

