from src.helper import is_valid_uid
from src.error import AccessError, InputError
from src.database import data

def is_valid_dm_id(dm_id):
    for dm in data['DM']:
        if dm['dm_id'] == dm_id:
            return True
    return False

def is_dm_creator(u_id,dm_id):
    for dm in data['DM']:
        if dm['dm_id'] ==dm_id:
            if dm['dm_owner'] == u_id:
                return True
    return False

def dm_details_v1(token, u_id):
    return {}

def dm_list_v1(token):
    return {}

def dm_create_v1(token, u_id):
    return {}