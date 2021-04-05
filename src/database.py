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
        with open('src/persitent_data.json', 'r') as fp:
            fp.close()
    except FileNotFoundError:
        with open('src/persitent_data.json', 'w+') as fp:
            fp.write(dumps(DATA))
            fp.close()
    with open ('src/persitent_data.json', 'r') as fp:
        python_data = load(fp)
        fp.close()
    return python_data

data = data_storage()

def update_data():
    with open('src/persitent_data.json', 'w') as fp:
        fp.write(dumps(data))
        fp.close()