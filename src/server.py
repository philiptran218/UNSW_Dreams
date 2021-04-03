import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src.error import InputError
from src import config

from src.auth import auth_register_v1, auth_login_v1, auth_logout_v1
from src.user import user_profile_setemail_v1, user_profile_sethandle_v1, user_profile_setname_v1, user_profile_v1
from src.users import users_all_v1
from src.other import clear_v1
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
#   auth_register route                                                        #
################################################################################

@APP.route("/auth/register/v2", methods=['POST'])
def auth_register():
    register_info = request.get_json()
    output = auth_register_v1(register_info['email'], register_info['password'], register_info['name_first'], register_info['name_last'])
    return dumps(output)

################################################################################
#   auth_login route                                                        #
################################################################################

@APP.route("/auth/login/v2", methods=['POST'])
def auth_login():
    login_info = request.get_json()
    output = auth_login_v1(login_info['email'], login_info['password'])
    return dumps(output)

################################################################################
#   auth_logout route                                                        #
################################################################################

@APP.route("/auth/logout/v1", methods=['POST'])
def auth_logout():
    logout_info = request.get_json()
    output = auth_logout_v1(logout_info['token'])
    return dumps(output)


################################################################################
#   clear route                                                                #
################################################################################

@APP.route("/clear/v1", methods=['DELETE'])
def clear():
    return clear_v1()
    
################################################################################
#   user_profile route                                                         #
################################################################################

@APP.route("/user/profile/v2", methods=['GET'])
def user_profile():
    profile_info = request.get_json()
    output = user_profile_v1(profile_info['token'], profile_info['u_id'])
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
#   users_all route                                                             #
################################################################################

@APP.route("/users/all/v1", methods=['GET'])
def users_all():
    userall_info = request.get_json()
    output = users_all_v1(userall_info['token'])
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
