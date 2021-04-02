import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src.error import InputError
from src import config

from src.auth import auth_register_v1
from src.channel import channel_invite_v1, channel_details_v1, channel_removeowner_v1, channel_addowner_v1, channel_leave_v1
from src.channels import channels_create_v1, channels_list_v1, channels_listall_v1
import src.message
import src.user
import src.users
from src.other import clear_v1
from src.dm import dm_create_v1, dm_details_v1, dm_list_v1
import src.database
from src.admin import admin_user_remove_v1, admin_userpermission_change_v1

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
#   auth_register route                                                       #
################################################################################

@APP.route("/auth/register/v2", methods=['POST'])
def auth_register():
    register_info = request.get_json()
    output = auth_register_v1(register_info['email'], register_info['password'], register_info['name_first'], register_info['name_last'])
    return dumps(output)

################################################################################
#   channel_invite route                                                       #
################################################################################

@APP.route("/channel/invite/v2", methods=['POST'])
def channel_invite():
    invite_info = request.get_json()
    output = channel_invite_v1(invite_info['token'], invite_info['channel_id'], invite_info['u_id'])
    return dumps(output)

################################################################################
#   channel_details route                                                      #
################################################################################

@APP.route("/channel/details/v2", methods=['GET'])
def channel_details():
    details_info = request.get_json()
    output = channel_details_v1(details_info['token'], details_info['channel_id'])
    return dumps(output)

################################################################################
#   channel_addowner route                                                     #
################################################################################

@APP.route("/channel/addowner/v1", methods=['POST'])
def channel_addowner():
    addowner_info = request.get_json()
    output = channel_addowner_v1(addowner_info['token'], addowner_info['channel_id'], addowner_info['u_id'])
    return dumps(output)

################################################################################
#   channel_removeowner route                                                  #
################################################################################

@APP.route("/channel/removeowner/v1", methods=['POST'])
def channel_removeowner():
    removeowner_info = request.get_json()
    output = channel_removeowner_v1(removeowner_info['token'], removeowner_info['channel_id'], removeowner_info['u_id'])
    return dumps(output)

################################################################################
#   channel_leave route                                                        #
################################################################################

@APP.route("/channel/leave/v1", methods=['POST'])
def channel_leave():
    leave_info = request.get_json()
    output = channel_leave_v1(leave_info['token'], leave_info['channel_id'])
    return dumps(output)

################################################################################
#   channels_create route                                                      #
################################################################################

@APP.route("/channels/create/v2", methods=['POST'])
def channels_create():
    create_info = request.get_json()
    output = channels_create_v1(create_info['token'], create_info['name'], create_info['is_public'])
    return dumps(output)

################################################################################
#   channels_listall route                                                     #
################################################################################

@APP.route("/channels/listall/v2", methods=['GET'])
def channels_listall():
    listall = request.get_json()
    output = channels_list_v1(listall['token'])
    return dumps(output)

################################################################################
#   channels_list route                                                        #
################################################################################

@APP.route("/channels/list/v2", methods=['GET'])
def channels_list():
    list_info = request.get_json()
    output = channels_list_v1(list_info['token'])
    return dumps(output)

################################################################################
#   clear route                                                                #
################################################################################

@APP.route("/clear/v1", methods=['DELETE'])
def clear():
    output = clear_v1()
    return output

################################################################################
#   admin_user_remove route                                                    #
################################################################################

@APP.route("/admin/user/remove/v1", methods=['DELETE'])
def admin_user_remove():
    user_remove_info = request.get_json()
    output = admin_user_remove_v1(user_remove_info['token'], user_remove_info['u_id'])
    return dumps(output)

################################################################################
#   admin_userpermission_change route                                          #
################################################################################

@APP.route("/admin/userpermission/chnage/v1", methods=['POST'])
def admin_userpermission_change():
    change_perm = request.get_json()
    output = admin_userpermission_change_v1(change_perm['token'], change_perm['u_id'], change_perm['permission_id'])
    return dumps(output)

################################################################################
#   dm_details route                                                           #
################################################################################

@APP.route("/dm/details/v1", methods=['GET'])
def dm_details():
    details = request.get_json()
    output = dm_details_v1(details['token'], details['dm_id'])
    return dumps(output)

################################################################################
#   dm_list route                                                              #
################################################################################

@APP.route("/dm/list/v1", methods=['GET'])
def dm_list():
    list_info = request.get_json()
    output = dm_list_v1(list_info['token'])
    return dumps(output)

################################################################################
#   dm_create route                                                            #
################################################################################

@APP.route("/dm/create/v1", methods=['POST'])
def dm_create():
    create_info = request.get_json()
    output = dm_create_v1(create_info['token'], [create_info['u_ids']])
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

