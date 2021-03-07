from src.error import InputError, AccessError
from src.database import data
from src.helper import is_valid_uid,get_first_name, get_last_name, get_email, get_handle


def channels_listall_v1(auth_user_id):
    validator = is_valid_uid(auth_user_id)
    channel_list = []
    if validator == True:
        for i in data["channels"]:
            output = {
                "channel_id": i["channel_id"],
                "channel_name": i["channel_name"]
            }
            channel_list.append(output)
        return channel_list
    else:
        raise AccessError("Please enter a valid user id")


def channels_list_v1(auth_user_id):   
    validator = is_valid_uid(auth_user_id)
    channel_list = []
    if validator == True:
        for i in data["channels"]:
            for j in i["all_members"]:
                if j["u_id"]== auth_user_id:
                    output = {
                        "channel_id": i["channel_id"],
                        "channel_name": i["channel_name"]
                    }
                    channel_list.append(output)
        return channel_list
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

