from src.error import AccessError, InputError
from src.database import data, update_data
from src.helper import is_valid_token, detoken

OWNER = 1
MEMBER = 2

# Checks the permissions of the user making the changes, given that token is valid.
def check_permissions(token):
    token_u_id = detoken(token)
    for user in data['users']:
        if user['u_id'] == token_u_id:
            perm = user['perm_id'] 
    return perm

def admin_user_remove_v1(token, u_id):
    """
    Function:
        Function removes the user from Dreams. 

    Arguments:
        token(str) - token of the registered user removing the user.
        u_id(int) - u_id of the person who is being removed.

    Exceptions:
        AccessError - If token is invalid
                    - If permission_id of remover is not owner (shown through token)
        InputError - If u_id of person being removed is invalid
                   - If there is only one user in Dreams.

    Return Type:
        Function produces no output
    """

    if is_valid_token(token):

        changer_perm = check_permissions(token)

        if changer_perm != OWNER:
            raise AccessError(description='Only owners can change permissions in Dreams')

        user_count = 0
        user_validator = False

        for user in data['users']:
            if user['u_id'] == u_id:
                user_validator = True
            user_count += 1

        if user_count < 2:
            raise InputError(description='Cannot delete as you are only user in Dreams')
        
        if not user_validator:
            raise InputError(description='entered u_id is invalid')

        for message in data['messages']:
            if message['u_id'] == u_id:
                message.update({'message': 'Removed user'})

        for user in data['users']:
            if user['u_id'] == u_id:
                user['name_first'] = 'Removed'
                user['name_last'] = 'user'
    else:
        raise AccessError(description='Invalid Token')

    update_data()
    return {}

def admin_userpermission_change_v1(token, u_id, permission_id):
    """
    Function:
        Function changes the permission of a specified user. 

    Arguments:
        token(str) - token of the registered user making the change
        u_id(int) - u_id of the person who is being changed.
        permission_id(int) - id representing the permissions of the user. 1 = Owner and 2 = Member

    Exceptions:
        AccessError - If token is invalid
                    - If permission_id of changer is not owner (shown through token)
        InputError - If u_id is invalid
                   - If permission_id is invalid (not owner or member)

    Return Type:
        Function produces no output

    """ 

    if not is_valid_token(token):
        raise AccessError(description='Invalid Token')

    if not (permission_id == OWNER or permission_id == MEMBER):
        raise InputError(description='Permission id is invalid.')
    
    if not check_permissions(token) == OWNER:
        raise AccessError(description='Only owners can change permissions in Dreams')
    validator = False
    for user in data['users']:
        if user['u_id'] == u_id:
            validator = True
            user['perm_id'] = permission_id

    if not validator:
        raise InputError (description='Inputted u_id is invalid')
    
    update_data()
    return {}
