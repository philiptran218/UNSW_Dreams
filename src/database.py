data = {
    'users': [],
    'channels': [],
    'messages': [],
}
''' initialise empty lists for data fields '''
''' what information each list should have '''

'''
users = [
    {
        'u_id': 1,
        'first_name': 'John',
        'last_name': 'Smith', 
        'perm_id': 1,
        'password': 'Goodpass',
        'email': 'johnsmith@gmail.com'
    }
]

channels = [
    {
        'channel_id': 1,
        'name': 'channel1',
        'all_members': [
            {
                'u_id': 1,
                'name_first': 'John',
                'name_last': 'Smith',
            },
        ], 
        'owner_members': [
            {
                'u_id': 1,
                'name_first': 'John',
                'name_last': 'Smith',
            }
        ],
        'is_public': True
    }
]

messages = [
    {
        'message_id': 1,
        'channel_id': 1,
        'u_id': 1, 
        'message': 'Hello world',
        'time_created': 1582426789,
    }
]
'''