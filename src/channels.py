
from src.error import InputError, AccessError
from src.database import data
from src.helper import is_valid_uid
from src.helper import get_first_name, get_last_name

def channels_listall_v1(auth_user_id):
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


