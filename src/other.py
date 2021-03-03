from src.data import data
#helper fucntion that when given a key mapping to a list in a dicionary, empties that list. 
def delete(aspect):
    ((data.get(aspect)).clear())




#clear_v1 - a fucntion that resets the internal data of the application to it's initial state
#erases all information about the users, erases all the channels and the messages

def clear_v1():
    '''
clear_v1 - a fucntion that resets the internal data of the application to it's initial state
erases all information about the users, erases all the channels and the messages
Arguments:
    </>  - <fucntion doesnt take any arguments>

Exceptions:
function doesnt throw any excpetions

Return Value:
fucntion doesnt return any value
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


