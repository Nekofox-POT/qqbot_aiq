#
# aiq/aie 引导创建程序
# 步骤2：配置大模型
#

########################################################################################################################
# 资源准备 #

###########
# 第三方库 #
##########
import openai

############
# 自创建模块 #
############

#########
# 变量池 #
########

########################################################################################################################
# 模型添加函数 #
#############
def add_model():

    while True:

        print('请输入模型地址：')
        api = str(input('>'))
        print(f'输入了: "{api}"')
        print('请输入使用的模型：')
        model = str(input('>'))
        print(f'输入了: "{model}"')
        print('请输入api_key：')
        key = str(input('>'))
        print(f'输入了: "{key}"')

        # 测试
        try:
            openai.OpenAI(
                api_key=key,
                base_url=api
            ).chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Hello"}
                ],
                stream=False
            )
            print('测试成功.')
            return [api, model, key]
        except Exception as e:
            print('测试失败，请检查api_key是否正确或模型地址是否正确')
            print(f'失败原因：{e}')
            print('1.重新写入 2.取消写入')
            while True:
                tmp = str(input('>'))
                if tmp == '1':
                    print('重新写入...')
                    break
                elif tmp == '2':
                    print('取消写入.')
                    return None
                else:
                    print('请输入正确的选项.')

########################################################################################################################
# 主程序 #
########
def main():

    model_list = [] # 已添加的大模型列表

    print('----------------------------')

    ### 大模型添加 ###
    while True:

        ### 展示 ###
        print('当前大模型列表')
        print('')
        if len(model_list) == 0:
            print('0. 空')
        else:
            for i in range(len(model_list)):
                print(f'{i + 1}. 模型名称："{model_list[i][1]}" 模型地址："{model_list[i][0]}" api_key："{model_list[i][2]}"')
        print('')

        ### 添加 ###
        print('1.添加 2.重新添加 3.就用这么多')
        tmp = str(input('>'))
        if tmp == '1':

            ### 添加模型 ###
            tmp = add_model()
            if tmp:
                model_list.append(tmp)

        elif tmp == '2':
            print('确定要全部重写吗？')
            print('1.确定 2：取消')
            tmp = str(input('>'))
            if tmp == '1':
                model_list = []
                print('已重置.')
            if tmp == '2':
                print('已取消.')
            else:
                print('请输入正确的选项.')
        elif tmp == '3':
            break
        else:
            print('请输入正确的选项.')

    ### 模型随机 ###
    print('是否随机选择模型？')
    print('此功能将使llbot在每次对话中随机选择一个模型进行对话。（随机模式）')
    print('若不使用，则按照载入顺序来尝试对话。（主备模式）')
    print('1.是 2.否 (默认值：是)')
    while True:
        tmp = str(input('>'))
        if tmp == '' or tmp == '1':
            mode_random = True
            print(f'选择了: "是"')
            break
        elif tmp == '2':
            mode_random = False
            print(f'选择了: "否"')
            break
        else:
            print('请输入正确的选项.')

    ### 本地模型 ###
    print('是否使用本地模型？')
    print('当远程模型不可用时（欠费等情况）')
    print('将使用本地模型进行对话。')
    print('! (注意！若想使用 爱爱❤~ 功能则必须选择 "是" ) !')
    print('1.是 2.否 (默认值：是)')
    while True:
        tmp = str(input('>'))
        if tmp == '' or tmp == '1':
            local_mode = True
            print(f'选择了: "是"')
            break
        elif tmp == '2':
            local_mode = False
            print(f'选择了: "否"')
            break
        else:
            print('请输入正确的选项.')

    ### 展示所有信息 ###
    print('')
    print('##########################')
    print(f'已添加的模型：')
    for i in range(len(model_list)):
       print(f'    {i + 1}. 模型名称："{model_list[i][1]}" 模型地址："{model_list[i][0]}" api_key："{model_list[i][2]}"')
    print(f'是否使用随机模式：{mode_random}')
    print(f'是否使用本地模型推理：{local_mode}')
    print('##########################')
    print('')
    out = {
        'model_list': model_list,
        'mode_random': mode_random,
        'local_mode': local_mode,
    }
    print('----------------------------')
    return out