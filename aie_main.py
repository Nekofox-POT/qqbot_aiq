#
# AIQ / AIE 主程序
#

########################################################################################################################
# 资源准备

###########
# 第三方库 #
##########
import multiprocessing
import time
import json
import threading
import datetime
import os
import signal
import random

############
# 自创建模块 #
############
import msg_receive
from chat import chat_api, chat_local, chat_doi
import send_api

#########
# 变量池 #
########
power = True    # 电源
last_heart_post = int(time.time())  # 上一次心跳上报时间
msg_queue = multiprocessing.Queue() # fastapi队列
cmd_queue = multiprocessing.Queue() # 命令队列
msg_list = []   # 消息列表
msg_list_lock = threading.RLock()   # 消息工作锁
last_action_time = int(time.time()) # 最后一次空闲时间
action_free_status = True   # 空闲状态
last_user_time = 0  # 用户最后一次发言时间
doi_mode = False    # doi模式
last_doi_list_range = 0   # 最后一个激活爱爱的语句指针

### 读取提示词 ###
try:
    with open('role_set.txt', 'r', encoding='utf-8') as f:
        prompt = f.read()
except:
    print('文件读取出错，请检查文件完整性.')

########################################################################################################################
# 小组件

###########
# 日志记录 #
##########
def log(msg):
    print(msg)
    # 读取文件
    try:
        with open('aie_log.txt', 'r', encoding='utf-8') as f:
            tmp = f.readlines()
    except:
        with open('aie_log.txt', 'w', encoding='utf-8') as f:
            f.close()
        with open('aie_log.txt', 'r', encoding='utf-8') as f:
            tmp = f.readlines()
    if len(tmp) > 65536:
        tmp = tmp[1:]
    # 写入
    tmp.append(f'{datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")} {msg}\n')
    with open('aie_log.txt', 'w', encoding='utf-8') as f:
        f.writelines(tmp)
        f.close()

########################################################################################################################
# 信息处理

###########
# 信息储存 #
##########
def msg_store():

    global last_heart_post, doi_mode, last_doi_list_range

    ### 启动fastapi ###
    log('启动fastapi.')
    ps_fastapi = multiprocessing.Process(target=msg_receive.main, args=(config['port'], msg_queue, cmd_queue, config['user_id']))
    ps_fastapi.start()

    while power:
        try:

            ### 获取 ###
            tmp = msg_queue.get_nowait()

            ### 解码 ###
            with msg_list_lock:

                # 心跳
                if tmp['type'] == 'heart':
                    last_heart_post = int(time.time())

                # 用户
                elif tmp['type'] == 'user':

                    print(f'收到消息：{tmp["msg"]}')
                    # 遍历处理消息
                    msg = ''
                    for i in tmp['msg']:
                        ### 文本 ###
                        if i['type'] == 'text':
                            msg += i['data']['text']
                            msg += '\n'
                        ### 回复 ###
                        if i['type'] == 'reply':
                            # 获取原信息
                            text = send_api.get_msg(config['post_addres'], i['data']['id'])
                            msg += f'(回复 "{config['assistant_name']}" : {text})'
                            msg += '\n'
                    msg = msg[:-1]
                    # 添加
                    if msg:
                        log(f'收到消息：{tmp['raw_msg']}')
                        msg_list.append({
                            'type': 'user',
                            'msg': msg,
                            'msg_id': tmp['msg_id'],
                            'time': tmp['time'],
                        })

                # 撤回
                elif tmp['type'] == 'recall':
                    for i in range(len(msg_list)):
                        if msg_list[i].get('msg_id') == tmp['msg_id']:
                            log(f'消息撤回：{msg_list.pop(i)}')
                            break

                # ai
                elif tmp['type'] == 'assistant':
                    log(f'回复: {tmp['msg']}')
                    # 爱爱
                    if tmp['msg'] == 'use_doi':
                        log('爱爱❤~')
                        doi_mode = True
                        # 初始化最后用户发言的指针
                        e = False
                        for i in range(len(msg_list)):
                            # 如果是用户/系统
                            print(len(msg_list) - 1 - i)
                            print(msg_list[len(msg_list) - 1 - i])
                            if msg_list[len(msg_list) - 1 - i]['type'] == 'user' or msg_list[len(msg_list) - 1 - i]['type'] == 'system':
                                # 头为0则直接添加
                                if len(msg_list) - 1 - i == 0:
                                    last_doi_list_range = 0
                                else:
                                    # 标记
                                    e = True
                            # 如果不是
                            else:
                                if e:
                                    last_doi_list_range = len(msg_list) - i
                                    print('用户最后发言指针：')
                                    print('----------------------')
                                    try:
                                        print(msg_list[last_doi_list_range - 1])
                                    except:
                                        pass
                                    print(f'{msg_list[last_doi_list_range]} ←--')
                                    try:
                                        print(msg_list[last_doi_list_range + 1])
                                    except:
                                        pass
                                    print('----------------------')
                                    break
                    # 普通消息
                    else:
                        # 发送
                        r = send_api.send_private_msg(config['post_addres'], config['user_id'], tmp['msg'])
                        if r:
                            log(f'发送失败：{r}')
                            continue
                        msg_list.append(tmp)

                # 系统消息
                elif tmp['type'] == 'system':
                    log(f'[{tmp['msg']}]')
                    msg_list.append(tmp)

        except:

            ### 溢出检测(大于4k) ###
            #↑# doi模式不删除 #↑#
            if len(str(msg_list)) > 4 * 1024 and not doi_mode:
                del msg_list[0]

        # 性能限制
        time.sleep(0.1)

    ### 关机 ###
    os.kill(ps_fastapi.pid, signal.SIGTERM)

###########
# 信息获取 #
##########
def msg_get():

    global last_user_time, last_doi_list_range

    # 普通模式
    if not doi_mode:
        with msg_list_lock:
            ### 新消息提醒 ###
            new_msg = False
            try:
                if msg_list[-1]['type'] == 'user':
                    new_msg = True
                elif msg_list[-1]['type'] == 'system':
                    if msg_list[-1]['notice']:
                        new_msg = True
                    else:
                        if msg_list[-2]['type'] == 'user':
                            new_msg = True
            except:
                pass
            msg = f'\n当前时间：{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n\n'

            ### 格式化 ###
            for i in msg_list:

                # 用户信息
                if i['type'] == 'user':
                    msg += f'{i['time']} {config['user_name']} :\n'
                    msg += i['msg']
                    last_user_time = i['time']

                # ai信息
                elif i['type'] == 'assistant':
                    msg += f'{i['time']} {config['assistant_name']} :\n'
                    msg += i['msg']

                # 系统信息
                elif i['type'] == 'system':
                    pass

                msg += '\n'

    # 爱爱模式
    else:

        with msg_list_lock:
            ### 新消息提醒 ###
            new_msg = False
            try:
                if msg_list[-1]['type'] == 'user':
                    new_msg = True
                elif msg_list[-1]['type'] == 'system':
                    if msg_list[-1]['notice']:
                        new_msg = True
                    else:
                        if msg_list[-2]['type'] == 'user':
                            new_msg = True
            except:
                pass
            msg = f'\n当前时间：{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n\n'

            ### 格式化 ###
            # 从指针处开始遍历
            for i in msg_list[last_doi_list_range:]:
                # 用户信息
                if i['type'] == 'user':
                    msg += f'{i['time']} {config['user_name']} :\n'
                    msg += i['msg']
                    last_user_time = i['time']

                # ai信息
                elif i['type'] == 'assistant':
                    msg += f'{i['time']} {config['assistant_name']} :\n'
                    msg += i['msg']

                # 系统信息
                elif i['type'] == 'system':
                    pass

                msg += '\n'

    print('---------------------')
    print(msg)
    print('---------------------')

    return [new_msg, msg, last_user_time]

########################################################################################################################
# ai模块

#########
# 动作流 #
#########
def action(jump = False):

    if not jump:

        global last_action_time

        # 暂停15s
        time.sleep(10)

        # 记录
        last_action_time = int(time.time())

#############
# ai运行核心 #
############
def assistant_core():

    re_generate = False

    ### 启动 ###
    log('启动ai模块.')
    while power:

        ### 普通模式 ###
        if not doi_mode:

            ### 执行动作流 ###
            if re_generate:
                action(True)
                re_generate = False
            else:
                action()

            ### 读取信息 ###
            tmp = msg_get()
            # 如果没有新的消息就不管
            if not tmp[0]:
                continue
            # 记录最后信息
            last_time = tmp[2]

            ### 生成(在线ai) ###
            result = []
            for i in range(1, 4):
                # 生成
                result = chat_api.main(config['model_list'], config['model_random'], config['allow_doi'], prompt, tmp[1])
                try:
                    result = json.loads(result)
                    break
                except:
                    log(f'json格式错误，尝试重新生成 ({i} / 3)')
                    result = []
                    continue

            ### 没有则本地生成 ###
            if not result:
                for i in range(1, 4):
                    result = chat_local.main(config['allow_doi//'], prompt, tmp[1])
                    try:
                        result = json.loads(result)
                        break
                    except:
                        log(f'json格式错误，尝试重新生成 ({i} / 3)')
                        result = []
                        continue

            ### 还是没有 ###
            if not result:
                log('生成失败.')
                continue

            ###  若生成后有新的信息，则重新生成 ###
            tmp = msg_get()
            print(tmp)
            if tmp[2] != last_time:
                log('有新消息，重新生成...')
                re_generate = True
                continue

            ### 回复 ###
            for i in result:
                # 添加消息队列
                for e in i:
                    time.sleep(random.uniform(0.2, 1.2))
                msg_queue.put({
                    'type': 'assistant',
                    'msg': i,
                    'time': datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]'),
                })

            ### 如果是爱爱则需要等待切换 ###
            if result == ['use_doi']:
                while not doi_mode:
                    time.sleep(0.1)

        ### doi模式 ###
        else:

            ### 等待读取 ###
            while True:
                # 获取新信息
                tmp = msg_get()
                time.sleep(30)
                # 有更新则重新等
                if msg_get()[2] != tmp[2]:
                    continue
                break

            # 如果没有新的消息就不管
            if not tmp[0]:
                continue

            ###  生成(本地ai) ###
            result = []
            for i in range(1, 4):
                result = chat_doi.main(prompt, tmp[1])
                try:
                    result = json.loads(result)
                    break
                except:
                    log(f'json格式错误，尝试重新生成 ({i} / 3)')
                    result = []
                    continue

            ### 还是没有 ###
            if not result:
                log('生成失败.')
                continue

            ### 回复 ###
            for i in result:
                # 添加消息队列
                msg_queue.put({
                    'type': 'assistant',
                    'msg': i,
                    'time': datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]'),
                })


########################################################################################################################
# 主程序 #
########
def main(input_config):

    log('aie启动.')

    ### 配置变量 ###
    global config
    config = input_config

    ### Windows安全声明 ###
    multiprocessing.freeze_support()

    ### 开启信息接收器 ###
    ps_msg_store = threading.Thread(target=msg_store)
    ps_msg_store.start()

    ### 开启ai模块 ###
    ps_assistant_core = threading.Thread(target=assistant_core)
    ps_assistant_core.start()
    ps_assistant_core.join()

########################################################################################################################
if __name__ == '__main__':
    import start
    start.aiq_start()