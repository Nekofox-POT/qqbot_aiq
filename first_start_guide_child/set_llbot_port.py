#
# aiq/aie 引导创建程序
# 步骤1：配置llbot端口
#

########################################################################################################################
# 资源准备 #

###########
# 第三方库 #
##########
import json
import requests

############
# 自创建模块 #
############

#########
# 变量池 #
########

########################################################################################################################
# 主程序 #
########
def main():

    print('----------------------------')

    # 信息重写回滚
    while True:

        ### 选择地址 ###
        print('选择监听地址。')
        print('请选择aie监听的地址（默认："127.0.0.1"）：')
        print('1. 127.0.0.1')
        print('2. 0.0.0.0')
        while True:
            tmp = str(input('>'))
            if tmp == '' or tmp == '1':
                host = '127.0.0.1'
                print(f'选择了: "{host}"')
                break
            elif tmp == '2':
                host = '0.0.0.0'
                print(f'选择了: "{host}"')
                break
            else:
                print('请输入正确的选项.')

        ### 选择端口 ###
        print('请输入aie监听的端口（默认：8412）：')
        while True:
            tmp = str(input('>'))
            if tmp == '':
                port = 8412
                print(f'输入了: "{port}"')
                break
            elif tmp.isdigit():
                try:
                    port = int(tmp)
                    print(f'输入了: "{port}"')
                    break
                except:
                    print('请输入正确的端口.')
            else:
                print('请输入正确的端口.')

        ### llbot通信地址 ###
        print('请输入llbot监听的地址：')
        while True:
            post_addres = str(input('>'))
            # 检测后面是否有 "/"
            try:
                if post_addres[-1] != '/':
                    post_addres += '/'
            except:
                pass
            print(f'输入了: "{post_addres}"')
            # 验证
            print('验证地址是否有效...')
            try:
                r = json.loads(requests.post(url=f'{post_addres}get_status', data={}, timeout=3).text)
                if r['data']['online'] == True:
                    print('验证成功.')
                    break
                else:
                    print('llbot不在线，请检查账号状态.')
                    print('验证失败')

            except:
                print('验证失败，请检查地址是否正确。')

        ### 是否开启心跳包 ###
        print('是否开启心跳包检查（默认：是）：')
        print('1. 是')
        print('2. 否')
        while True:
            tmp = str(input('>'))
            if tmp == '' or tmp == '1':
                heart_check = True
                print(f'选择了: "是"')
                break
            elif tmp == '2':
                heart_check = False
                print(f'选择了: "否"')
                break
            else:
                print('请输入正确的选项.')

        ### 目标用户 ###
        print('请输入对象的QQ号：')
        while True:
            tmp = str(input('>'))
            if tmp.isdigit():
                target_account = int(tmp)
                print(f'输入了: "{target_account}"')
                print('测试...')
                try:
                    r = json.loads(requests.post('http://192.168.91.128:8312/send_private_msg', data={
                        'user_id': target_account,
                        'message': '你好吖~（突然冒出！）',
                    }).text)
                    if r['status'] == 'ok':
                        print('测试成功.')
                        break
                    else:
                        print('测试失败，请检查账号是否被风控或账号密码错误')
                except:
                    print('测试失败，请检查账号是否被风控或账号密码错误')
            else:
                print('请输入正确的QQ号.')

        ### 确认所有信息 ###
        print('')
        print('请确认所有信息（确认后不可修改）')
        print('##########################')
        print(f'监听地址：{host}')
        print(f'监听端口：{port}')
        print(f'llbot地址：{post_addres}')
        print(f'是否开启心跳包检查：{heart_check}')
        print(f'对象QQ号：{target_account}')
        print('##########################')
        print('')
        print('1.确认 2.重新填写 （默认：1）')
        while True:
            tmp = str(input('>'))
            if tmp == '' or tmp == '1':
                print('确认！')
                out = {
                        'host': host,
                        'port': port,
                        'post_addres': post_addres,
                        'heart_check': heart_check,
                        'target_account': target_account,
                    }
                print('')
                print('----------------------------')
                return out
            elif tmp == '2':
                print('重新填写...')
                break
            else:
                print('请输入正确的选项.')