import requests
import re
import os
from bs4 import BeautifulSoup
import subprocess


# 获取当前目录下的所有M4A文件列表
m4a_files = [file for file in os.listdir() if file.endswith(".m4a")]

# 遍历M4A文件列表
for file_path in m4a_files:
        
    # 获取用户输入的文件路径
   # file_path = input("请输入文件路径：")
    # 获取文件名（不包括扩展名）
    file_name = os.path.basename(file_path)
    # 找到文件名中第一个横杠的位置
    first_hyphen_index = file_name.find("-")
    # 如果文件名中存在横杠，则截取横杠后的部分作为变量
    if first_hyphen_index != -1:
        a = file_name[first_hyphen_index + 1:file_name.rfind(".")]
    else:
        a = file_name
    print(f"提取的变量为：{a}")
    # 获取用户输入的关键词
    keyword = a
    # 构建URL
    url = f'https://www.kugeci.com/search?q={keyword}'
    # 发送请求获取网页源代码
    response = requests.get(url)
    if response.status_code == 200:
        html_code = response.text
        # 使用正则表达式来匹配关键词和链接
        pattern = r'<a\s+href="([^"]*)"\s*>(.*?)' + keyword
        match = re.search(pattern, html_code)
        if match:
            link = match.group(1)
            print("找到链接：", link)
            response = requests.get(link)
        #    print(response.text)
            html_code = response.text
            pattern = r'\[\d{2}:\d{2}\.\d{2}\].*?<br\s*/>'
            # 使用正则表达式匹配每一个[00:01.08]格式的行
            matches = re.findall(pattern, html_code, re.DOTALL)
            # 将匹配结果写入文件
            with open("temp.lrc", "w", encoding="utf-8") as file:
                for match in matches:
                    # 去除<br />标签
                    match = match.replace("<br />", "")
                    file.write(match + "\n")
            print(file_path)
            command = ["AtomicParsley", file_path, "--lyricsFile", "temp.lrc"]
            # 运行命令
            subprocess.run(command)
            os.remove(file_path)
        else:
            print("未找到关键词对应的链接")
    else:
        print("请求失败，状态码：", response.status_code)

      

