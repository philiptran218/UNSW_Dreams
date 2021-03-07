from src.error import InputError, AccessError
from src.database import data
from src.helper import is_valid_uid
from src.helper import get_first_name, get_last_name

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


