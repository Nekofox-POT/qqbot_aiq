#
# aiq/aie 引导创建程序
#

########################################################################################################################
# 资源准备 #

###########
# 第三方库 #
##########
import os
import pickle
import ctypes
import sys
import time

############
# 自创建模块 #
############
from first_start_guide_child import set_prompt, set_ai, set_llbot_port, set_local_model

#########
# 变量池 #
########

########################################################################################################################
# 主程序 #
########
def guide():

    config = {}

    ### 清屏 ###
    os.system('cls')

    ### 检测管理员权限 ###
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print('请以管理员身份运行此脚本.')
        print('按Enter键退出')
        input('>|')
        sys.exit(1)

    ### 展示页 ###
    print('----------------------------')
    print('aie配置程序')
    with open('version.ppp', 'rb') as f:
        tmp = pickle.load(f)
    print(f'当前版本: {tmp}')
    print('----------------------------')

    ### 步骤1：配置llbot端口 ###
    time.sleep(1)
    os.system('cls')
    print('步骤1/3：配置llbot')
    config.update(set_llbot_port.main())

    ### 步骤2：配置ai ###
    time.sleep(1)
    os.system('cls')
    print('步骤2/3：配置大模型')
    config.update(set_ai.main())

    ### 步骤2.1（可选）：配置本地ai ###
    if config['local_model']:
        print('步骤2/3：配置本地ai')
        config.update(set_local_model.main())

    ### 步骤3：配置提示词 ###
    time.sleep(1)
    os.system('cls')
    print('步骤3/3：配置提示词')
    config.update(set_prompt.main())

    print('配置完成！')

    ### 写入 ###
    print('写入配置文件')
    with open('config.ppp', 'wb') as f:
        pickle.dump(config, f)
    print('写入成功！')

    print('文件创建完成，即将进入初始化...')
    return config