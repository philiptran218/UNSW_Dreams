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

def dm_remove_v1(token,dm_id):
    u_id = detoken(token)# yet to be completed

    #checking if user who called fucntion has a valid u_id
    if not is_valid_uid(u_id):
        raise AccessError('user_id is invalid')
    #checking if the dm to be removed has a valid dm_id
    if not is_valid_dm_id(dm_id):
        raise InputError('dm_id is invalid')
    #checking if the user who called the fucntion is the original dm creator
    if not is_dm_creator(u_id,dm_id):
        raise AccessError('user is not original dm creator')
    
    for dm in data['DM']:
        if dm['dm_id'] == dm_id:
            del(dm)

    

'''an input error is raaised when the dm id is invalid

access error when the user is not the orgeinal creatoe



is Dm id valid ->>>> create based on u id
is the  token of the user calling the fuicntion similar to
             the token of the user who created
             it?
try to match u id from the token given to the owner firld inside dm'''

    
    