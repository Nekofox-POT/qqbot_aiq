#
# 信息收集器
#

########################################################################################################################
# 资源准备 #

###########
# 第三方库 #
##########
import fastapi
import uvicorn
import json
import time
import datetime

############
# 自创建模块 #
############

#########
# 变量池 #
########
app = fastapi.FastAPI() # fastapi初始化
user_id = ''    # user_id初始化

########################################################################################################################
# fastapi接口 #
##############

@app.post("/aiq")
async def index(request: fastapi.Request):
    try:

        ### 接收 ###
        tmp = await request.body()
        tmp = json.loads(tmp.decode('utf-8'))

        ### 解析 ###
        msg_queue.put(tmp)
        # 心跳
        if tmp.get('post_type') == 'meta_event':
            msg_queue.put({'role': 'heart', 'time': int(time.time())})
        # 消息
        elif tmp.get('post_type') == 'message':
            # 私聊 且 目标符合
            if tmp.get('message_type') == 'private' and tmp.get('user_id') == user_id:
                msg_queue.put({'role': 'user', 'msg': tmp['message'], 'raw_msg': tmp['raw_message'], 'time': f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]'})

    except:
        pass
    return ''

########################################################################################################################
# 主函数 #
########
def main(port, que, qid):
    global msg_queue
    global user_id
    user_id = qid
    msg_queue = que
    uvicorn.run(app, host="0.0.0.0", port=port)