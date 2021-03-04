from src.error import InputError, AccessError
from src.data import data
#helperfucntion that return first name given user auth id
def get_first_name(auth_user_id):
    for user in data['users']:
        if(user.get('u_id')) == auth_user_id:
            first_name = (user.get('name_first'))
            return first_name
    

#helperfucntion that return last name given user auth id
def get_last_name(auth_user_id):
    for user in data['users']:
        if(user.get('u_id')) == auth_user_id:
            last_name = (user.get('name_last'))
            return last_name
    



def channels_list_v1(auth_user_id):
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }

def channels_listall_v1(auth_user_id):
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }


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
    #if not any ((user.get('auth_user_id')) == auth_user_id for user in data['users']):
        #raise AccessError('user_id is invalid')
    
    channel_id = len(data['channels'])+1
    new_chan = {
        'channel_id': channel_id,
        'name':name,
        'all members':[
            {
                'u_id':auth_user_id,
                'name_first':get_first_name(auth_user_id),
                'name_last' :get_last_name(auth_user_id),
            },
        ],
        'owner members':[
            {
                'u_id':auth_user_id,
                'name_first':get_first_name(auth_user_id),
                'name_last' :get_last_name(auth_user_id),

            },
        ],
        'is_public': is_public,
    }
    data['channels'].append(new_chan)
    return {
        'channel_id': channel_id,
    }


