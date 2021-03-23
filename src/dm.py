


def dm_invite_v1(token, dm_id, u_id):
    '''
    Function:
        Inviting a user to an existing dm

    Arguments:
        token (str) - token of a registered user during their session
        dm_id (int) - this is the ID of the dm that the user is invited to
        u_id (int) - this is the ID of a user to be invited

    Exceptions:
        InputError  - dm_id does not refer to a existing dm.
                    - u_id does not refer to a valid user.
        AccessError when any of: 
                    - the authorised user is not already a member of the DM.

    Return Type:
        This function doesn't return any data.
    ''' 
    token_u_id = detoken(token)
    
    if not is_valid_dm_id(dm_id) :
        raise InputError("dm_id does not refer to an existing dm")
    
    if not is_already_in_dm(token_u_id, dm_id):
        raise AccessError("Authorised user is not a member of the dm")
    
    if not helper.is_valid_uid(u_id) :
        raise InputError("Please enter a valid u_id")
    
    if is_already_in_dm(u_id, dm_id):
        return {}
    
    invited_member = {
                    'u_id': u_id,
                    'name_first': helper.get_first_name(u_id),
                    'name_last': helper.get_last_name(u_id),
                    'email': helper.get_email(u_id),
                    'handle_str': helper.get_handle(u_id),
                     }
    for dm in data['DM']:
        if dm['dm_id'] == dm_id:
            dm['dm_members'].append(invited_member)
            return{}

