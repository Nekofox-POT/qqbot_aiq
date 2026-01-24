#
# 版本号管理器
#

########################################################################################################################
# 资源准备

###########
# 第三方库 #
##########

############
# 自创建模块 #
###########
from aes_encryption import aes_encryption
import pickle

#########
# 变量池 #
########

########################################################################################################################
# 开始程序 #
##########
def main():
    try:
        with open('version.ppp', 'rb') as f:
            a = pickle.loads(aes_encryption.decrypt(f.read()))
        print(f'当前版本号：{a}')
    except Exception as e:
        print(e)
    a = str(input('输入版本号>'))
    with open('version.ppp', 'wb') as f:
        f.write(aes_encryption.encrypt(pickle.dumps(a)))

if __name__ == '__main__':
    main()