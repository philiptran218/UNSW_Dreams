from src.data import data

def is_valid_uid(u_id):
    for user in data['users']:
        if user['u_id'] == u_id:
            return True
    return False