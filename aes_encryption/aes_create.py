#
# 加密函数创建
#

########################################################################################################################
# 资源准备 #

###########
# 第三方库 #
##########
import Crypto.Random
import base64
import random

############
# 自创建模块 #
############

#########
# 变量池 #
########

########################################################################################################################
# 开始程序 #
##########
if __name__ == '__main__':
    aes_key = base64.b64encode(Crypto.Random.get_random_bytes(32)).decode('utf-8')
    xor_key = random.randint(0, 255)
    print(f"aes密钥：{aes_key}")
    print(f"xor密钥：{xor_key}")
    print('写入...')
    with open('aes_encryption.py', 'w', encoding='utf-8') as f:
        f.write(
            "#\n"
            "# 加密器\n"
            "#\n"
            "\n"
            "########################################################################################################################\n"
            "# 资源准备\n"
            "\n"
            "###########\n"
            "# 第三方库 #\n"
            "##########\n"
            "import Crypto.Cipher.AES\n"
            "import Crypto.Random\n"
            "import Crypto.Util.Padding\n"
            "import base64\n"
            "\n"
            "############\n"
            "# 自创建模块 #\n"
            "###########\n"
            "\n"
            "#########\n"
            "# 变量池 #\n"
            "########\n"
            "\n"
            "########################################################################################################################\n"
            "# 加解密函数\n"
            "\n"
            "########\n"
            "# 加密 #\n"
            "#######\n"
            "def encrypt(text):\n"
            "\n"
            "    ### 密钥 ###\n"
            f"    aes_key = '{aes_key}'\n"
            f"    xor_key = {xor_key}\n"
            "\n"
            "    ### key解码 ###\n"
            "    key = base64.b64decode(aes_key.encode('utf-8'))\n"
            "\n"
            "    ### AES加密 ###\n"
            "    iv = Crypto.Random.get_random_bytes(Crypto.Cipher.AES.block_size)\n"
            "    tmp = iv + Crypto.Cipher.AES.new(key, Crypto.Cipher.AES.MODE_CBC, iv).encrypt(\n"
            "        Crypto.Util.Padding.pad(text, Crypto.Cipher.AES.block_size)\n"
            "    )\n"
            "\n"
            "    ### XOR加密 ###\n"
            "    result = bytes([b ^ xor_key for b in tmp])\n"
            "\n"
            "    ### 输出 ###\n"
            "    return result\n"
            "\n"
            "########\n"
            "# 解密 #\n"
            "######\n"
            "def decrypt(text):\n"
            "\n"
            "    ### 密钥 ###\n"
            f"    aes_key = '{aes_key}'\n"
            f"    xor_key = {xor_key}\n"
            "\n"
            "    ### key解码 ###\n"
            "    key = base64.b64decode(aes_key.encode('utf-8'))\n"
            "\n"
            "    ### XOR解密 ###\n"
            "    tmp = bytes([b ^ xor_key for b in text])\n"
            "\n"
            "    ### AES解密 ###\n"
            "    result = Crypto.Util.Padding.unpad(\n"
            "        Crypto.Cipher.AES.new(\n"
            "            key,\n"
            "            Crypto.Cipher.AES.MODE_CBC,\n"
            "            tmp[:Crypto.Cipher.AES.block_size]\n"
            "        ).decrypt(\n"
            "            tmp[Crypto.Cipher.AES.block_size:]\n"
            "        ),\n"
            "        Crypto.Cipher.AES.block_size\n"
            "    )\n"
            "\n"
            "    ### 输出 ###\n"
            "    return result\n"
        )
    print('创建完成！')