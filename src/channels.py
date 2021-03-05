from src.data import data
from src.helper import is_valid_uid
from src.error import AccessError

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
    return {
        'channel_id': 1,
    }
"""
if __name__ == "__main__":
    auth_user_id = 1
    listall = channels_listall_v1(auth_user_id)
    lis = channels_list_v1(auth_user_id)
    print(listall)
    print(lis)

    auth_user_id = 10000
    listall = channels_listall_v1(auth_user_id)
    lis = channels_list_v1(auth_user_id)
    print(listall)
    print(lis)
    
"""
