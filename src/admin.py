from src.error import AccessError, InputError
from src.database import data
from src.user import user_profile_setname_v1
from src.message import message_edit_v1

OWNER = 1
MEMBER = 2

# Checks the permissions of the user making the changes. Useful for authorising
# and checking for errors.

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

    token_u_id = detoken(token)

    user_count = 0
    for user in data['users']:
        if 

    if user_count < 2:
        raise InputError('Cannot delete as you are only user in Dreams')
    

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
    token_u_id = detoken(token)

    if permission_id != OWNER or permission_id != MEMBER:
        raise InputError('Permission id is invalid.')

    for user in data['users']:
        if user['u_id'] == u_id:
            user['perm_id'] = permission_id
        elif user['u_id'] == token_u_id:
            if user['perm_id'] != OWNER:
                raise AccessError('Only owners can change the permissions of users')
        else:
            raise InputError ('Inputted u_id is invalid')

