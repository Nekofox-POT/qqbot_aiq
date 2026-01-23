#
# aiq/aie 引导创建程序
# 步骤2.1：配置大模型
#

########################################################################################################################
# 资源准备 #

###########
# 第三方库 #
##########
import subprocess
import shutil
import winreg
import os
import urllib.parse
import requests
import time

############
# 自创建模块 #
############

#########
# 变量池 #
########

########################################################################################################################

##############
# 环境变量刷新 #
#############
def refresh_system_env():

    user_env = {}
    system_env = {}

    ### 扫描变量 ###
    try:

        # 用户变量
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as key:
            i = 0
            while True:
                try:
                    name, value, reg_type = winreg.EnumValue(key, i)
                    user_env[name] = str(value)
                    i += 1
                except WindowsError:
                    break

        # 系统变量
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                            "SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment") as key:
            i = 0
            while True:
                try:
                    name, value, reg_type = winreg.EnumValue(key, i)
                    system_env[name] = str(value)
                    i += 1
                except WindowsError:
                    break

    except Exception as e:
        print(f"未知错误：{e}")

    ### 合并更新 ###
    env = {**os.environ}
    env.update(system_env)
    env.update(user_env)
    os.environ.clear()
    os.environ.update(env)

#########
# 下载器 #
########
def download_file(url):

    ### 解析 ###
    try:
        # 获取文件名
        parsed_url = urllib.parse.urlparse(url)
        filename = os.path.basename(parsed_url.path)
        if not filename:
            print("错误：无法从URL中提取文件名")
            raise ConnectionError
    except:
        print('失败：无法解析连接.')
        return None

    ### 下载 ###
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    try:
        with requests.get(url, stream=True, timeout=60) as response:
            # 获取文件总大小
            total_size = int(response.headers.get('Content-Length', 0))
            downloaded = 0

            # 下载的同时写入
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        print(f"\r下载进度: {(downloaded / total_size * 100):.2f}% ({downloaded}/{total_size} bytes)",
                              end='', flush=True)
            return file_path

    except Exception as e:
        print(f"下载时出现错误：{e}")
        # 删除不完整文件
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
        return None

####################
# ollama自动安装工具 #
###################
def ollama_install():

    while True:
        print('ollama下载链接：https://github.com/ollama/ollama/releases/latest')
        print('代理下载连接：https://hk.gh-proxy.org/https://github.com/ollama/ollama/releases/latest/download/OllamaSetup.exe')
        print('安装完后点击Enter检测ollama是否存在.')
        input('>|')
        # 刷新变量
        refresh_system_env()
        if shutil.which('ollama'):
            print('ollama已安装.')
            break
        else:
            print('未检测到ollama.')

######################################################################################################################
# 主程序 #
########
def main():

    print('----------------------------')

    ### ollama检测 ###
    print('检测ollama是否存在...')
    while True:
        # 刷新环境
        refresh_system_env()
        if shutil.which('ollama'):
            print('ollama存在.')
            break
        else:
            print('ollama不存在，请先安装ollama.')
            print('本地推理基于ollama构建运行，所以需要安装ollama依赖')
            ollama_install()
            input('>|')

if __name__ == '__main__':
    main()