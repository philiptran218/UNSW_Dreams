from src.database import data

# Helper fucntion that when given a key mapping to a list in a dicionary, empties that list. 
def delete(aspect):
    ((data.get(aspect)).clear())

def clear_v1():
    '''
    Function:
        Resets the internal data of the application to it's initial stateerases all information 
        about the users, erases all the channels and the messages.

    Arguments:
        This fucntion doesn't take any arguments.

    Exceptions:
        This function doesn't throw any excpetions.

    Return Value:
        This function doesn't return any value.
    '''
    delete('users')
    delete('channels')
    delete('messages')


def search_v1(auth_user_id, query_str):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
    }

