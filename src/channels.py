from src.error import InputError, AccessError
from src.database import data
from src.helper import is_valid_uid,get_first_name, get_last_name, get_email, get_handle, detoken, is_valid_token, add_to_notifications

def channels_listall_v1(token):
    """
    Function:
        Id is authenticated, then list of all channels is returned. Note that only channel id and 
        name is returned. This is done by looping through entire list of channels and taking the 
        name and id.

    Arguments:
        Code takes in input auth_user_id through the helper function is_valid_id.

    Exceptions:
        AccessError - If id is false or invalid, exception is thrown as per specification.

    Return Type:
        Channels datatype is returned. This is a dictionary with channel id and name.
    """ 
    validator = is_valid_token(token)
    channel_list = []
    if validator == True:
        for channel in data["channels"]:
            output = {
                "channel_id": channel["channel_id"],
                "name": channel["name"]
            }
            channel_list.append(output)
        return {'channels': channel_list}
    else:
        raise AccessError(description="Invalid token")


def channels_list_v1(token): 
    """
    Function:
        Id is authenticated, then list of channels the user is in is returned. Note that only channel 
        id and name is returned. This is done by looping through entire list of channels and taking 
        the name and id. To test if the user is in the channel, the code loops through the user list 
        of the channel and checks if the user is inside the channel.

    Arguments:
        Code takes in input auth_user_id through the helper function is_valid_id.

    Exceptions:
        AccessError - If id is false or invalid, exception is thrown as per specification.

    Return Type:
        Channels datatype is returned. This is a dictionary with channel id and name.
    """ 
    channel_list = []
    validator = is_valid_token(token)
    if validator == True:
        token_u_id = detoken(token)
        for channel in data["channels"]:
            for member in channel["all_members"]:
                if member["u_id"]== token_u_id:
                    output = {
                        "channel_id": channel["channel_id"],
                        "name":channel["name"]
                    }
                    channel_list.append(output)
        return {'channels': channel_list}
    else:
        raise AccessError(description="Invalid token")


def channels_create_v1(token, name, is_public):
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
    if not is_valid_token(token) :
        raise AccessError("token is invalid")
    
    auth_user_id = detoken(token)
    if len(name) > 20:
        raise InputError('channel name must be less than 20 characters')

    
    channel_id = len(data['channels']) + 1
    new_chan = {
        'channel_id': channel_id,
        'name':name,
        'all_members':[
            {
                'u_id':auth_user_id,
                'name_first':helper.get_first_name(auth_user_id),
                'name_last' :helper.get_last_name(auth_user_id),
                'email': helper.get_email(auth_user_id),
                'handle_str': helper.get_handle(auth_user_id),
            },
        ],
        'owner_members':[
            {
                'u_id':auth_user_id,
                'name_first':helper.get_first_name(auth_user_id),
                'name_last' :helper.get_last_name(auth_user_id),
                'email': helper.get_email(auth_user_id),
                'handle_str': helper.get_handle(auth_user_id),
            },
        ],
        'is_public': is_public,
    }
    data['channels'].append(new_chan)
    return {
        'channel_id': channel_id,
    }


