data = {
    'users': [],
    'channels': [],
    'messages': [],
    'DM': [],
    'sessions_info': {
        'session_num': 0,
        'sessions': [],
    },
}
''' initialise empty lists for data fields '''
''' what information each list should have '''

'''
users = [
    {
        'u_id': 1,
        'name_first': 'John',
        'name_last': 'Smith', 
        'perm_id': 1,
        'password': 'Goodpass',
        'email': 'johnsmith@gmail.com'
    }
]

channels = [
    {
        'channel_id': 1,
        'name': channel1,
        'all_members': [
            {
                'u_id': 1,
                'name_first': 'John',
                'name_last': 'Smith',
                'email':
                'handle_str':
            },
        ], 
        'owner_members': [
            {
                'u_id': 1,
                'name_first': 'John',
                'name_last': 'Smith',
                'email':
                'handle_str':
            }
        ],
        'is_public': True
    }
]

messages = [
    {
        'message_id': 1,
        'u_id': 1,
        'channel_id': 1,
        'dm_id': -1, 
        'message': 'Hello world',
        'time_created': 1582426789,
    }
]

DM = [
    {
        'dm_id': 1,
        'dm_owner_id': (u_id of owner),
        'dm_name': name should be automatically generated based on the user(s) that is in this dm. The name should be an alphabetically-sorted,        
        comma-separated list of user handles, e.g. 'handle1, handle2, handle3'.
        'dm_members': [
            {
                'u_id': 1,
                'name_first': 'John',
                'name_last': 'Smith',
                'email':
                'handle_str':
            },
        ], 
    }
]

notifications = [
    {
        'auth_user_id': Id of person sending the invite/creating the dm
        'u_id': Id of person being invited
        'channel_id': Id of channel, if in dm set channel_id to -1
        'dm_id': Id of dm, if in channel set dm_id to -1
        'time_created': round(time)
        
        Note: To get time
            time = datetime.today()
            time = time.replace(tzinfo=timezone.utc).timestamp()

    }
]
'''
