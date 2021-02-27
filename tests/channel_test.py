'''
Required Tests:
    - Test if channel_id is valid. (InputError)
        + Try passing in valid channel_id.
        + Try passing in invalid channel_id.
    - Test if u_id is valid. (InputError)
        + Try passing in valid u_id.
        + Try passing in invalid u_id.
    - Test if auth_user_id is member of channel. (AccessError)
        + Try passing an auth_user_id that is a member of channel.
        + Try passing an auth_user_id that is not a member of channel.
    - Ensure once invited the user is added to the channel immediately.
        + Check if user is in channel.
    - 
    Note: Have not add, commit, push yet
'''