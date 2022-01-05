import os
import re
import requests
from bs4 import BeautifulSoup


def askUrl(aimUrl):
    headers = {
        "User-Agent": "加入自己UA",
        "referer": "https://www.bilibili.com/",
        "cookie": "加入自己cookie"
    }
    response = requests.get(aimUrl, headers=headers)
    print("do askaimUrl")
    return response


def askAVUrl(aimUrl, refUrl):
    headers = {
        "User-Agent": "加入自己UA",
        "referer": refUrl,
        "cookie": "加入自己cookie"
    }
    response = requests.get(aimUrl, headers=headers)
    print("do askAVUrl")
    return response


def solveUrl(response):
    bsobj = BeautifulSoup(response.text, "lxml")  # 解析为beautifulsoup对象
    htmlresponse = str(bsobj)  # html类型为byte 正则匹配的是字符串，必须要类型转换
    print("do solveUrl")
    return htmlresponse


def saveAndMix(videoUrl, audioUrl, title):
    # 请求音视频资源
    mp3resp = askAVUrl(audioUrl, aimUrl)
    mp4resp = askAVUrl(videoUrl, aimUrl)
    #获取到内容
    videoData = mp4resp.content
    audioData = mp3resp.content
    # 保存合成正确文件与删除未合成文件
    titlenew = title + "!"
    with open(f'{titlenew}.mp3', "wb") as f:
        f.write(audioData)
    with open(f'{titlenew}.mp4', "wb") as f:
        f.write(videoData)
    os.system(f'ffmpeg -i "{titlenew}.mp4" -i "{titlenew}.mp3" -c copy "{title}.mp4"')
    os.remove(f'{titlenew}.mp4')
    os.remove(f'{titlenew}.mp3')
    print("mission success")


if __name__ == '__main__':
    aimUrl = input("输入指定url")  # 输入网址
    response = askUrl(aimUrl)  # 为视频页发送请求
    htmlresponse = solveUrl(response)  # 收到的响应解析成string类型的对象
    scriptset = re.findall(re.compile(r"<script>(.*?)</script>"), htmlresponse)[0]  # 正则找到script，音视频的url在script标签中
    videoUrl = re.findall(r'"video":\[{"id":\d+,"baseUrl":"(.*?)",', scriptset)[0]  # 解析出视频url
    audioUrl = re.findall(r'"audio":\[{"id":\d+,"baseUrl":"(.*?)",', scriptset)[0]  # 解析出音频url
    title = re.findall(re.compile(r'<h1 class="video-title" title="(.*?)"'), htmlresponse)[0]#找出视频标题
    saveAndMix(videoUrl, audioUrl, title)
