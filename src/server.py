import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src.error import InputError
from src import config
from src.dm import dm_invite_v1, dm_leave_v1, dm_messages_v1, dm_remove_v1
from src.channels import channels_create_v1
import src.database

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

def getData():
    return src.database.data

################################################################################
# dm_remove route                                                              #
################################################################################

@APP.route('/dm/remove/v1', methods=['DELETE'])
def dm_remove():
    remove_info = request.get_json()
    output = dm_remove_v1(remove_info['token'],remove_info['dm_id'])
    return dumps(output)

################################################################################
# dm_invite route                                                              #
################################################################################
@APP.route('/dm/invite/v1', methods=['POST'])
def dm_invite():
    invite_info = request.get_json()
    output = dm_invite_v1(invite_info['token'],invite_info['dm_id'],invite_info['u_id'])
    return dumps(output)

################################################################################
# dm_leave route                                                               #
################################################################################
@APP.route('/dm/leave/v1', methods=['POST'])
def dm_leave():
    leave_info = request.get_json()
    output = dm_leave_v1(leave_info['token'],leave_info['dm_id'])
    return dumps(output)

################################################################################
# dm_messages_v1 route                                                         #
################################################################################
@APP.route('/dm/messages/v1', methods=['GET'])
def dm_messages():
    message_info = request.get_json()
    output = dm_messages_v1(message_info['token'],message_info['dm_id'],message_info['start'])
    return dumps(output)

################################################################################
# channel_create_v1 route                                                      #
################################################################################
@APP.route('/channels/create/v2', methods=['POST'])
def create_channel():
    channel_info = request.get_json()
    output = channels_create_v1(channel_info['token'],channel_info['name'],channel_info['is_public'])
    return dumps(output)



# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
   	    raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })

if __name__ == "__main__":
    APP.run(port=config.port) # Do not edit this port
