from src.data import data

def channels_listall_v1(auth_user_id):
    channel_list = []
    for i in data["channels"]:
        output = {
            "channel_id": i["channel_id"],
            "channel_name": i["channel_name"]
        }
        channel_list.append(output)
    return channel_list

def channels_list_v1(auth_user_id):   
    channel_list = []
    for i in data["channels"]:
        for j in i["all_members"]:
            if j["u_id"]== auth_user_id:
                output = {
                    "channel_id": i["channel_id"],
                    "channel_name": i["channel_name"]
                }
                channel_list.append(output)
    return channel_list


def channels_create_v1(auth_user_id, name, is_public):
    return {
        'channel_id': 1,
    }
"""
if __name__ == "__main__":
    auth_user_id = 1
    listall = channels_listall_v1(1)
    lis = channels_list_v1(1)
    print(listall)
    print(lis)
"""