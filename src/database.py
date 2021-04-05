from json import dumps, load

DATA = {
    'users': [],
    'channels': [],
    'messages': [],
    'DM': [],
    'notifications': [],
    'sessions': [],
    'session_ids': [],
}

def data_storage():
    try: 
        with open('src/persitent_data.json', 'r') as file:
            pass
    except FileNotFoundError:
        with open('src/persitent_data.json', 'w+') as file:
            file.write(dumps(DATA))
    with open ('src/persitent_data.json', 'r') as fp:
        python_data = load(fp)
        fp.close()
    return python_data

data = data_storage()
