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
import time
import winreg
import os
import urllib.parse
import requests
import ctypes

############
# 自创建模块 #
############

#########
# 变量池 #
########
pull_mf = (
    'FROM ./Qwen3-14B-Q6_K.gguf\n'
    'TEMPLATE """\n'
    '{{- if .System }}{{ .System }}{{ end }}\n'
    '{{- range $i, $_ := .Messages }}\n'
    '{{- $last := eq (len (slice $.Messages $i)) 1}}\n'
    '{{- if eq .Role "user" }}<｜User｜>{{ .Content }}\n'
    '{{- else if eq .Role "assistant" }}<｜Assistant｜>{{ .Content }}{{- if not $last }}<｜end▁of▁sentence｜>{{- end }}\n'
    '{{- end }}\n'
    '{{- if and $last (ne .Role "assistant") }}<｜Assistant｜>{{- end }}\n'
    '{{- end }}"""\n'
    'PARAMETER stop "<｜begin▁of▁sentence｜>"\n'
    'PARAMETER stop "<｜end▁of▁sentence｜>"    \n'
    'PARAMETER stop "<｜User｜>"    \n'
    'PARAMETER stop "<｜Assistant｜>"   \n'
)
pull_doi_mf = (
    'FROM ./Tifa-Deepsex-14b-CoT-Q4_K_M.gguf\n'
    'TEMPLATE """\n'
    '{{- if .System }}{{ .System }}{{ end }}\n'
    '{{- range $i, $_ := .Messages }}\n'
    '{{- $last := eq (len (slice $.Messages $i)) 1}}\n'
    '{{- if eq .Role "user" }}<｜User｜>{{ .Content }}\n'
    '{{- else if eq .Role "assistant" }}<｜Assistant｜>{{ .Content }}{{- if not $last }}<｜end▁of▁sentence｜>{{- end }}\n'
    '{{- end }}\n'
    '{{- if and $last (ne .Role "assistant") }}<｜Assistant｜>{{- end }}\n'
    '{{- end }}"""\n'
    'PARAMETER stop "<｜begin▁of▁sentence｜>"\n'
    'PARAMETER stop "<｜end▁of▁sentence｜>"    \n'
    'PARAMETER stop "<｜User｜>"    \n'
    'PARAMETER stop "<｜Assistant｜>"   \n'
)

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
    file_path = f'{os.getcwd()}\\{filename}'
    try:
        with requests.get(url, stream=True, timeout=60) as response:
            # 获取文件总大小
            total_size = int(response.headers.get('Content-Length', 0))
            downloaded = 0

            # 下载的同时写入
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=131072):
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

#################
# ollama安装工具 #
################
def ollama_set():

    ### 检测安装 ###
    while True:
        # 刷新变量
        refresh_system_env()
        try:
            subprocess.run(['ollama', '--version'])
            print('ollama已安装.')
            break
        except:
            print('未检测到ollama.')
            print('ollama下载链接：https://github.com/ollama/ollama/releases/latest')
            print(
                '代理下载连接：https://hk.gh-proxy.org/https://github.com/ollama/ollama/releases/latest/download/OllamaSetup.exe')
            print('安装完后点击Enter检测ollama是否存在.')
            input('>|')

    ### 注册环境 ###
    print('请输入ollama默认通信端口（默认：11434）')
    while True:
        try:
            tmp = str(input('>'))
            if tmp == '':
                port = 11434
                print(f'输入了: "{port}"')
                break
            else:
                tmp = int(tmp)
                if tmp < 0 or tmp > 65535:
                    raise ValueError
                else:
                    port = tmp
                    print(f'输入了: "{port}"')
                    break
        except:
            print('请输入正确的端口.')
    # 关闭ollama
    os.system('taskkill /f /im "ollama app.exe"')
    os.system('taskkill /f /im "ollama.exe"')
    # 配置环境
    try:
        reg_key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment",
            0,
            winreg.KEY_READ | winreg.KEY_WRITE | winreg.KEY_WOW64_64KEY
        )
        winreg.SetValueEx(reg_key, "OLLAMA_HOST", 0, winreg.REG_SZ, f"0.0.0.0:{port}")
        winreg.CloseKey(reg_key)

        # 广播
        HWND_BROADCAST = 0xFFFF
        WM_SETTINGCHANGE = 0x001A
        SMTO_ABORTIFHUNG = 0x0002

        ctypes.windll.user32.SendMessageTimeoutW(
            HWND_BROADCAST, WM_SETTINGCHANGE, 0, "Environment",
            SMTO_ABORTIFHUNG, 5000, None
        )
        print('环境注册完成。')
    except WindowsError as e:
        print(f"操作注册表时出错: {e}")
    # 启动
    subprocess.run(['ollama', '--version'])

    return port


######################################################################################################################
# 主程序 #
########
def main():

    print('----------------------------')

    ### ollama检测 ###
    print('检测ollama是否存在...')
    ollama_port = ollama_set()

    ### 模型安装 ###
    print('检测模型是否存在')
    ollama_list = subprocess.run(["ollama", "list"], capture_output=True, text=True).stdout.splitlines()
    check = False
    for i in ollama_list:
        if 'qwen3-14b-q6-k' in i:
            print('模型存在.')
            check = True
            break
    # 不存在就创建模型
    if not check:
        print('下载本地模型...')
        print('模型选用：Qwen3-14B-Q6_K')
        while True:
            if 'Qwen3-14B-Q6_K.gguf' in os.listdir():
                tmp_model = 'Qwen3-14B-Q6_K.gguf'
            else:
                tmp_model = download_file('https://www.modelscope.cn/models/Qwen/Qwen3-14B-GGUF/resolve/master/Qwen3-14B-Q6_K.gguf')
            if tmp_model:
                # 安装
                with open('install.mf', 'w', encoding='utf-8') as f:
                    f.write(pull_mf)
                subprocess.run(['ollama', 'create', 'qwen3-14b-q6-k', '-f', 'install.mf'])
                os.remove('install.mf')
                print('模型安装完成.')
                break
            else:
                print('下载失败，请检查网络设置.')
                print('要重试吗？还是自行下载？')
                print('1.重试 2.自己下载（默认：1.重试）')
                while True:
                    tmp = str(input('>'))
                    if tmp == '' or tmp == '1':
                        break
                    elif tmp == '2':
                        print('模型下载链接：https://www.modelscope.cn/models/Qwen/Qwen3-14B-GGUF/resolve/master/Qwen3-14B-Q6_K.gguf')
                        print('模型下载完成后将此模型放置到程序目录下.')

    ### （可选）是否允许doi ###
    print('是否开启doi模式？')
    print('doi模式会生成可能会被风险控制的特定词语')
    print('请根据实际情况选择❤~')
    print('1.是 2.否（默认：1.是）')
    while True:
        tmp = str(input('>'))
        if tmp == '' or tmp == '1':
            ### 模型安装 ###
            print('检测模型是否存在')
            ollama_list = subprocess.run(["ollama", "list"], capture_output=True, text=True).stdout.splitlines()
            check = False
            for i in ollama_list:
                if 'deep-sex' in i:
                    print('模型存在.')
                    check = True
                    break
            # 不存在就创建模型
            if not check:
                print('下载本地模型...')
                while True:
                    if 'Tifa-Deepsex-14b-CoT-Q4_K_M.gguf' in os.listdir():
                        tmp_model = 'Tifa-Deepsex-14b-CoT-Q4_K_M.gguf'
                    else:
                        tmp_model = download_file('https://www.modelscope.cn/models/cjc1887415157/Tifa-Deepsex-14b-CoT-GGUF-Q4/resolve/master/Tifa-Deepsex-14b-CoT-Q4_K_M.gguf')
                    if tmp_model:
                        # 安装
                        with open('install.mf', 'w', encoding='utf-8') as f:
                            f.write(pull_doi_mf)
                        subprocess.run(['ollama', 'create', 'deep-sex', '-f', 'install.mf'])
                        os.remove('install.mf')
                        print('模型安装完成.')
                        break
                    else:
                        print('下载失败，请检查网络设置.')
                        print('要重试吗？还是自行下载？')
                        print('1.重试 2.自己下载（默认：1.重试）')
                        while True:
                            tmp = str(input('>'))
                            if tmp == '' or tmp == '1':
                                break
                            elif tmp == '2':
                                print('模型下载链接：https://www.modelscope.cn/models/cjc1887415157/Tifa-Deepsex-14b-CoT-GGUF-Q4/resolve/master/Tifa-Deepsex-14b-CoT-Q4_K_M.gguf')
                                print('模型下载完成后将此模型放置到程序目录下.')
            allow_doi = True
            print('启用成功❤~')
            break
        elif tmp == '2':
            allow_doi = False
            print('不启用.')
            break
        else:
            print('请输入正确的选项.')

    ### 展示所有信息 ###
    print('')
    print('##########################')
    print(f'ollama端口号：{ollama_port}')
    print(f'是否启用doi：{allow_doi}')
    print('##########################')
    print('')
    out = {
        'ollama_port': ollama_port,
        'allow_doi': allow_doi,
    }
    print('----------------------------')
    return out
