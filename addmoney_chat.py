#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:SunXiuWen
# make_time:2018/11/27
"""
整体逻辑是：
1. 录音让百度语言识别api，翻译成文本
2. 将文本与设定好的问题，交给百度，让其进行文本语义判断，根据得分进行相应逻辑
3. 拿到百度自然语言api处理的得分，如果符合要求，将设定好的答案，交给百度语因合成接口，处理成语音，然后调用播放器播放
4. 如果所提出的问题，答案库里没有，就调用图灵机器人接口处理，
5. 将图灵返回的结果，交给百度合成接口，转义成语音，然后播放
"""
import os
import uuid
import requests
from aip import AipSpeech
from aip import AipNlp

"""调用图灵api和百度语言实现问题对话"""
tu_ling_api_url = "http://openapi.tuling123.com/openapi/api/v2"

data = {
    "reqType": 0,
    "perception": {
        "inputText": {
            "text": "附近的酒店"
        },
    },
    "userInfo": {
        "apiKey": "94806283c6714684ab8c7803ca4948eb",
        "userId": "1"
    }
}


def go_to_tu_ling(question, uid):
    """
    封装成函数，让其它应用调用，
    注意图灵上下文管理，如问天气，其会记住这句话，接着问位置，最后会回答你要的结果！！！
    图灵api要求请求方式为post，格式为json，返回也为json

    requests模块发送json数据，参数用json存data
    接收json数据，用res.json()反序

    :param question: 用户提的问题
    :param uid: 用户的uid，区分不同的人
    :return:
    """
    data['perception']['inputText']['text'] = question
    data['userInfo']['userId'] = uid
    response = requests.post(tu_ling_api_url, json=data)  # 注意点发json数据，使用的是json而非data
    result = response.json().get('results')[0]['values']['text']
    return result


"""百度语音合成和语音识别"""

APP_ID = "14951495"
API_KEY = 'IUpYavuVCL2LDrxfofL3gGQN'
SECRET_KEY = 'qWq4ukxMF9cnfGs6H88vqN4qpnG5RgMB'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

client_nlp = AipNlp(APP_ID, API_KEY, SECRET_KEY)  # 对话的判断，词义等


def text_to_audio(text):
    """文本转换成音频：百度语言合成
    接口文本限制在1024个字节内

    生成一个音频文件
    """
    audio_file_name = uuid.uuid4()  # 宇宙唯一
    result = client.synthesis(text, 'zh', 1, {
        'spd': 4,  # 语速
        'pit': 9,  # 音调
        'vol': 5,  # 音量
        'per': 0  # 发音人
    })
    if not isinstance(result, dict):
        with open(f'./static/media/temp_save/{audio_file_name}.mp3', 'wb') as f:
            f.write(result)
    # win中调用播放器播放
    # os.system(fr'D:\Django\Flask_project_dir\人工智能\static\media\temp_save\{audio_file_name}.mp3')
    return f'{audio_file_name}.mp3'


def audio_to_pcm(filepath):
    """转换成pcm音频格式"""
    pcm_filename = "{}.pcm".format(filepath.split(".")[0])
    cmd = f"ffmpeg -y  -i {filepath}  -acodec pcm_s16le -f s16le -ac 1 -ar 16000 {pcm_filename}"
    os.system(cmd)
    return pcm_filename


def audio_to_text(filepath):
    """音频转换成文字：百度语言识别，时长限制在60s内"""
    pcm_filename = audio_to_pcm(filepath)
    with open(pcm_filename, 'rb') as f:
        res = client.asr(f.read(), 'pcm', 16000, {
            'dev_pid': 1537,
        })
        print(res)
        if res.get('result', "") is not None:
            return res.get('result')[0]
        else:
            return res.get('err_msg')


def check_nlp(text, uid):
    """
    输入文本，对短文本相似度判断得分，进行相应处理,语言播放出来
    文本可以是录音通过百度语音识别实现转换成的
    接入百度自然语言api,返回答案语音
    """
    if client_nlp.simnet("你叫什么名字", text).get('score') >= 0.7:
        """如果相识大于70%，返回text"""
        return text_to_audio(text)
    if client_nlp.simnet("你今年多大了", text).get('score') >= 0.7:
        return text_to_audio("我今年30岁了")
    else:
        return text_to_audio(go_to_tu_ling(text, uid))


if __name__ == '__main__':
    """将录音转换成文本，然后去识别和调用图灵
    
    # 谷歌只支持本地录音，火狐支持远程！！！！
    # 发现通过os找static和templates里的文件的绝对路劲，都显示是根目录下的文件，而没有static，templates目录
    """
    text = audio_to_text('./static/media/799a077d-05f8-4e7c-831a-b9f2b8754613.mp3')

    check_nlp(text, 3)
