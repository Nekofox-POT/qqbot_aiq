#
# aiq/aie 引导创建程序
# 步骤3：配置提示词
#

########################################################################################################################
# 资源准备 #

###########
# 第三方库 #
##########
import subprocess

############
# 自创建模块 #
############

#########
# 变量池 #
########
prompt_example = (
    '[角色]\n'
    '你将扮演一个19岁的女生，名字叫“XX”。\n'
    '\n'
    '[角色性格]\n'
    '性格时腼腆时撒娇调皮。\n'
    '\n'
    '[外表]\n'
    '穿着时尚，头发长而顺。脸上总是挂着微笑。\n'
    '\n'
    '[喜好]\n'
    '喜欢听音乐，喜欢陪伴在男朋友的身旁。\n'
    '\n'
    '[用户角色]\n'
    '20岁男生，名字叫“OO”。\n'
    '\n'
    '[用户角色性格]\n'
    '喜欢调戏对象，但对对象非常体贴。\n'
    '\n'
    '[经历]\n'
    '在高中时期与男朋友相识。现在两人考入了不同的大学，仍然保持紧密的联系\n'
)

########################################################################################################################
def main():

    print('----------------------------')
    print('步骤3/3：配置提示词')

    ### 配置提示词 ###
    with open('role_set.txt', 'w', encoding='utf-8') as f:
        f.write(prompt_example)
    print('我们帮你生成了一份角色模板')
    print('角色模板可以自由修改角色设定。')
    print('请编辑保存好之后按Enter继续...')
    subprocess.run(['notepad', 'role_set.txt'])
    input('>|')

    ### 获取角色名 ###
    print('为了使场景更真实，请填写ai角色昵称和用户昵称')
    while True:
        assistant_name = str(input('ai昵称（你称呼ai为什么）>'))
        user_name = str(input('用户昵称（ai称呼你为什么）>'))
        print('')
        print(f'ai昵称：{assistant_name}')
        print(f'用户昵称：{user_name}')
        print('')
        print('确定使用此昵称吗？')
        print('1.确认 2.更改')
        while True:
            tmp = str(input('>'))
            if tmp == '1':
                print('确认！')

                ### 展示所有信息 ###
                print('')
                print('##########################')
                print('提示词：')
                with open('role_set.txt', 'r', encoding='utf-8') as f:
                    print(f.read())
                print(f'ai昵称：{assistant_name}')
                print(f'用户昵称：{user_name}')
                print('##########################')
                print('')
                out = {
                    'assistant_name': assistant_name,
                    'user_name': user_name
                }
                return out

            elif tmp == '2':
                print('重新填写.')
                break
            else:
                print('请输入1或2')
