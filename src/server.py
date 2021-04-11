import sys
from json import dumps, loads
from flask import Flask, request
from flask_cors import CORS
from src.error import InputError
from src import config

from src.dm import dm_invite_v1, dm_leave_v1, dm_messages_v1, dm_remove_v1, dm_create_v1, dm_details_v1, dm_list_v1, dm_messages_v1
from src.channels import channels_create_v1, channels_listall_v1,channels_list_v1
from src.auth import auth_register_v1, auth_login_v1, auth_logout_v1
from src.other import clear_v1
from src.channel import channel_invite_v1, channel_details_v1, channel_removeowner_v1, channel_addowner_v1, channel_leave_v1, channel_join_v1, channel_messages_v1
from src.message import message_senddm_v1, message_send_v1, message_edit_v1, message_remove_v1, message_share_v1, message_react_v1, message_sendlater_v1, message_sendlaterdm_v1
from src.user import user_profile_v1, user_profile_setemail_v1, user_profile_sethandle_v1, user_profile_setname_v1
from src.users import users_all_v1
from src.other import clear_v1, search_v1, notifications_get_v1
from src.admin import admin_user_remove_v1, admin_userpermission_change_v1

from src.database import data

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

################################################################################
#   auth_register route                                                        #
################################################################################

@APP.route("/auth/register/v2", methods=['POST'])
def auth_register():
    register_info = request.get_json()
    output = auth_register_v1(register_info['email'], register_info['password'], register_info['name_first'], register_info['name_last'])
    return dumps(output)

################################################################################
#   auth_login route                                                           #
################################################################################

@APP.route('/auth/login/v2', methods=['POST'])
def auth_login():
    user_info = request.get_json()
    output = auth_login_v1(user_info['email'],user_info['password'])

    return dumps(output)
    
################################################################################
#   auth_logout route                                                          #
################################################################################

@APP.route('/auth/logout/v1', methods=['POST'])
def auth_logout():
    logout_info = request.get_json()
    output = auth_logout_v1(logout_info['token'])
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
    details_info = request.args
    output = channel_details_v1(details_info['token'], int(details_info['channel_id']))
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
#   channel_join route                                                         #
################################################################################

@APP.route("/channel/join/v2", methods=['POST'])
def channel_join():
    join_info = request.get_json()
    output = channel_join_v1(join_info['token'], join_info['channel_id'])
    return dumps(output)

################################################################################
#   channel_messages route                                                     #
################################################################################

@APP.route("/channel/messages/v2", methods=['GET'])
def channel_messages():
    messages_info = request.args
    output = channel_messages_v1(messages_info['token'], int(messages_info['channel_id']), int(messages_info['start']))
    return dumps(output)

################################################################################
#   channels_create route                                                      #
################################################################################

@APP.route('/channels/create/v2', methods=['POST'])
def create_channel():
    channel_info = request.get_json()
    output = channels_create_v1(channel_info['token'],channel_info['name'],channel_info['is_public'])
    return dumps(output)

################################################################################
#   channels_listall route                                                     #
################################################################################

@APP.route("/channels/listall/v2", methods=['GET'])
def channels_listall():
    listall = request.args
    output = channels_listall_v1(listall['token'])
    return dumps(output)

################################################################################
#   channels_list route                                                        #
################################################################################

@APP.route("/channels/list/v2", methods=['GET'])
def channels_list():
    list_channels = request.args
    output = channels_list_v1(list_channels['token'])
    return dumps(output)

################################################################################
#   dm_remove route                                                            #
################################################################################

@APP.route('/dm/remove/v1', methods=['DELETE'])
def dm_remove():
    remove_info = request.get_json()
    output = dm_remove_v1(remove_info['token'],remove_info['dm_id'])
    return dumps(output)


################################################################################
#   dm_leave route                                                             #
################################################################################

@APP.route('/dm/leave/v1', methods=['POST'])
def dm_leave():
    leave_info = request.get_json()
    output = dm_leave_v1(leave_info['token'],leave_info['dm_id'])
    return dumps(output)

################################################################################
#   dm_details route                                                           #
################################################################################

@APP.route("/dm/details/v1", methods=['GET'])
def dm_details():
    details = request.args
    output = dm_details_v1(details['token'], int(details['dm_id']))
    return dumps(output)

################################################################################
#   dm_list route                                                              #
################################################################################

@APP.route("/dm/list/v1", methods=['GET'])
def dm_list():
    list_info = request.args
    output = dm_list_v1(list_info['token'])
    return dumps(output)

################################################################################
#   dm_create route                                                            #
################################################################################

@APP.route("/dm/create/v1", methods=['POST'])
def dm_create():
    create_info = request.get_json()
    output = dm_create_v1(create_info['token'], create_info['u_ids'])
    return dumps(output)
    
################################################################################
#   dm_invite route                                                            #
################################################################################    
    
@APP.route("/dm/invite/v1", methods=['POST'])
def dm_invite():
    invite_info = request.get_json()
    output = dm_invite_v1(invite_info['token'], invite_info['dm_id'], invite_info['u_id'])
    return dumps(output)
    
################################################################################
#   dm_messages route                                                          #
################################################################################    
    
@APP.route("/dm/messages/v1", methods=['GET'])
def dm_messages():
    message_info = request.args
    output = dm_messages_v1(message_info['token'], int(message_info['dm_id']), int(message_info['start']))
    return dumps(output)

################################################################################
#   message_senddm route                                                       #
################################################################################

@APP.route("/message/senddm/v1", methods=['POST'])
def message_senddm():
    message_info = request.get_json()
    output = message_senddm_v1(message_info['token'], message_info['dm_id'], message_info['message'])
    return dumps(output)

################################################################################
#   message_send route                                                         #
################################################################################

@APP.route("/message/send/v2", methods=['POST'])
def message_send():
    message_info = request.get_json()
    output = message_send_v1(message_info['token'], message_info['channel_id'], message_info['message'])
    return dumps(output)

################################################################################
#   message_edit route                                                         #
################################################################################

@APP.route("/message/edit/v2", methods=['PUT'])
def message_edit():
    message_info = request.get_json()
    output = message_edit_v1(message_info['token'], message_info['message_id'], message_info['message'])
    return dumps(output)

################################################################################
#   message_remove route                                                       #
################################################################################

@APP.route("/message/remove/v1", methods=['DELETE'])
def message_remove():
    message_info = request.get_json()
    output = message_remove_v1(message_info['token'], message_info['message_id'])
    return dumps(output)

################################################################################
#   message_share route                                                        #
################################################################################

@APP.route("/message/share/v1", methods=['POST'])
def message_share():
    message_info = request.get_json()
    output = message_share_v1(message_info['token'], message_info['og_message_id'], message_info['message'], message_info['channel_id'], message_info['dm_id'])
    return dumps(output)

################################################################################
#   message_sendlater route                                                    #
################################################################################

@APP.route("/message/sendlater/v1", methods=['POST'])
def message_sendlater():
    message_info = request.get_json()
    output = message_sendlater_v1(message_info['token'], message_info['channel_id'], message_info['message'], message_info['time_sent'])
    return dumps(output)

################################################################################
#   message_sendlaterdm route                                                  #
################################################################################

@APP.route("/message/sendlaterdm/v1", methods=['POST'])
def message_sendlaterdm():
    message_info = request.get_json()
    output = message_sendlaterdm_v1(message_info['token'], message_info['dm_id'], message_info['message'], message_info['time_sent'])
    return dumps(output)

################################################################################
#   search route                                                               #
################################################################################

@APP.route("/search/v2", methods=['GET'])
def search():
    search_info = request.args
    output = search_v1(search_info['token'], search_info['query_str'])
    return dumps(output)

################################################################################
#   clear route                                                                #
################################################################################

@APP.route("/clear/v1", methods=['DELETE'])
def clear():
    return clear_v1()
   
################################################################################
#   notifications_get route                                                    #
################################################################################

@APP.route("/notifications/get/v1", methods=['GET'])
def notifications_get():
    notif_info = request.args
    output = notifications_get_v1(notif_info['token'])
    return dumps(output)

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

@APP.route("/admin/userpermission/change/v1", methods=['POST'])
def admin_userpermission_change():
    change_perm = request.get_json()
    output = admin_userpermission_change_v1(change_perm['token'], change_perm['u_id'], change_perm['permission_id'])
    return dumps(output)

################################################################################
#   user_profile route                                                         #
################################################################################

@APP.route("/user/profile/v2", methods=['GET'])
def user_profile():
    profile_info = request.args
    output = user_profile_v1(profile_info['token'], int(profile_info['u_id']))
    return dumps(output)

################################################################################
#   user_set_name route                                                        #
################################################################################

@APP.route("/user/profile/setname/v2", methods=['PUT'])
def profile_setname():
    setname_info = request.get_json()
    output = user_profile_setname_v1(setname_info['token'], setname_info['name_first'], setname_info['name_last'])
    return dumps(output)

################################################################################
#   user_set_email route                                                       #
################################################################################

@APP.route("/user/profile/setemail/v2", methods=['PUT'])
def profile_setemail():
    setemail_info = request.get_json()
    output = user_profile_setemail_v1(setemail_info['token'], setemail_info['email'])
    return dumps(output)

################################################################################
#   user_set_handle route                                                      #
################################################################################

@APP.route("/user/profile/sethandle/v1", methods=['PUT'])
def profile_sethandle():
    sethandle_info = request.get_json()
    output = user_profile_sethandle_v1(sethandle_info['token'], sethandle_info['handle_str'])
    return dumps(output)

################################################################################
#   users_all route                                                            #
################################################################################

@APP.route("/users/all/v1", methods=['GET'])
def users_all():
    userall_info = request.args
    output = users_all_v1(userall_info['token'])
    return dumps(output)

################################################################################
#   message_react route                                                        #
################################################################################

@APP.route("/message/react/v1", methods=['POST'])
def message_react():
    message_info = request.get_json()
    output = message_react_v1(message_info['token'], message_info['message_id'], message_info['react_id'])
    return dumps(output)
    
################################################################################
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

