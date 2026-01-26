#
# 名称
#

########################################################################################################################
# 资源准备

###########
# 第三方库 #
##########
import json
import requests

############
# 自创建模块 #
###########

#########
# 变量池 #
########

########################################################################################################################
# 函数集

##############
# 发送私聊消息 #
#############
def send_private_msg(host, user_id, msg):
    try:
        r = json.loads(requests.post(f'{host}send_private_msg', data={
            'user_id': user_id,
            'message': msg,
        }).text)
        if r['status'] != 'ok':
            return r
    except Exception as e:
        return e
    else:
        return None

##############
# 获取消息文本 #
#############
def get_msg(host, message_id):
    try:
        r = json.loads(requests.post(f'{host}get_msg', data={
            'message_id': message_id,
        }).text)
        if r['status'] == 'ok':
            return r['message']
        else:
            return None
    except Exception as e:
        print(e)
        return None