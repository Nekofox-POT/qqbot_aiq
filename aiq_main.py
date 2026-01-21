#
# AIQ 主程序
#

########################################################################################################################
# 资源准备 #

###########
# 第三方库 #
##########
import multiprocessing
import time
import json
import threading
import datetime
import requests

############
# 自创建模块 #
############
import msg_receive

#########
# 变量池 #
########
last_heart_post = int(time.time())  # 上一次心跳上报时间
msg_queue = multiprocessing.Queue() # fastapi接收队列
msg_list = []   # 消息列表
msg_list_lock = threading.RLock() # 消息工作锁

aiq_fastapi_port = 0    # fastapi端口
aiq_target_account = 0  # 目标账号
aiq_user_name = ''  # 使用者名字
aiq_assistant_name = '' # ai昵称

########################################################################################################################
#
# 小组件
#

###########
# 日志记录 #
##########
def log(msg):
    # 日志记录
    open('AIQ.log', 'a', encoding='utf-8').write(f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]{msg}\n')
    print(msg)

########################################################################################################################
# 信息处理 #

###########
# 信息储存 #
##########
def msg_store():

    global last_heart_post

    ###########
    ### 开启进程
    ps_fastapi = multiprocessing.Process(target=msg_receive.main, args=(aiq_fastapi_port, msg_queue))
    ps_fastapi.start()

    ###########
    ### 接收储存
    while True:
        try:

            ### 获取 ###
            tmp = msg_queue.get_nowait()

            ### 分类 ###
            # 如果是心跳
            if tmp.get('post_type') == 'meta_event':
                # 更新时间
                last_heart_post = int(time.time())
            # 如果是消息
            elif tmp.get('post_type') == 'message':
                # 如果是私聊 且 目标账号吻合
                if tmp.get('message_type') == 'private' and tmp.get('user_id') == aiq_target_account:
                    # 添加消息
                    msg_list.append({'role': 'user', 'msg': tmp['message'], 'raw_msg': tmp['raw_message'], 'time': f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'})

            ### 处理长度 ###
            # 如果上下文太长(大于16k)
            while len(json.dumps(msg_list).encode('utf-8')) > 16 * 1024:
                # 删除首项
                del msg_list[0]

        finally:

            ### 性能限制 ###
            time.sleep(0.1)

###########
# 信息获取 #
##########
def msg_get():

    ### 获取信息 ###
    with msg_list_lock:
        tmp = msg_list.copy()

    ### 处理 ###
    # 缓存池
    user_msg = ''
    # 遍历信息
    for i in tmp:

        # 如果为 system
        if i['role'] == 'system':
            pass

        # 如果为 assistant
        elif i['role'] == 'assistant':
            pass

        # 如果为 user
        elif i['role'] == 'user':

            # 标题
            user_msg += f'{i['time']} {aiq_user_name} :\n'

            # 分段讨论
            if len(i['msg']) == 1:
                # 如果是纯文字
                if i['raw_msg'][0] != '[':
                    log(f'用户输入: {i['msg']}')
            elif len(i['msg']) == 2:
                # 如果是回复
                if i['raw_msg'][0].get('type') == 'reply' and i['raw_msg'][1].get('type') == 'text':
                    pass
            elif len(i['msg']) == 3:
                pass


        # 添加分割符
        user_msg += '\n'

########################################################################################################################
# 主程序 #
########
def main():

    ##################
    ### Windows安全声明
    multiprocessing.freeze_support()

    ################
    ### 开启信息接收器
    ps_msg_store = threading.Thread(target=msg_store)
    ps_msg_store.start()

    while True:
        try:
            msg = msg_queue.get(False)
            print(msg)
        except:
            time.sleep(0.1)

########################################################################################################################
if __name__ == '__main__':
    main()