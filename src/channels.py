from src.data import channels

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
    print(f"{channels}")


def channels_create_v1(auth_user_id, name, is_public):
    return {
        'channel_id': 1,
    }

if __name__ == "__main__":
    auth_user_id = 1
    channels_listall_v1(1)