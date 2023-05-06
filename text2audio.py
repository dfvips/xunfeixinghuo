# -*- coding: utf-8 -*-
# This script was created by dreamfly
# author: dreamfly
# github: https://github.com/dfvips
import websocket
import json
import base64
import requests
import struct
import random
import re
import userinfo
from langdetect import detect 

question = '' # 提问
choice = '' # 选择AI助手

# 选择AI助手，默认随机
def get_assist(text):
    oth = "x4_lingxiaoyao x4_lingxiaoxuan x4_lingxiaolu x4_lingxiaoying x4_lingxiaoxuan_chat x4_mingge x4_lingxiaoqi_casualnews x4_yiyi x4_lingfeihan_document x4_mingze x4_lingxiaoqi_cts x4_matengHF x4_wangjianHF x4_lingxiaoqi_gentle x4_lingxiaoyao_assist x4_lingxiaolu_assist x4_lingxiaoying_assist x4_lingxiaoxuan_gentle x4_lingxiaoxuan_assist x4_lingxiaowan_assist x4_lingxiaoyao_anime x4_lingxiaoqi_assist x4_lingxiaoqi_en x4_lingxiaoyao_en x4_lingxiaolu_en x4_lingxiaoying_en x4_lingxiaoxuan_en x4_lingxiaoxuan_en_v2 x4_lingxiaowan_en x4_lingxiaoqi_en_v2 x4_lingxiaoyao_comic x4_lingxiaoying_em_v2 x4_lingxiaoyao_em x4_lingxiaolu_em_v2 x4_lingxiaoqi_em_v2 x4_lingxiaoxuan_em_v2 x4_lingxiaoying_emo x4_lingxiaoqi_emo x4_lingxiaolu_emo x4_lingxiaoxuan_emo x4_lingxiaoyao_emo"
    chi = "x4_lingxiaoqi x4_lingfeizhe x4_lingfeichen"
    en = "x4_EnUs_Luna x4_EnUs_Gavin"
    if (is_english(text)):
        array = list(set(en.split()))
    else:
        array = list(set(chi.split()))   
    choice = random.choice(array)
    return choice

# 判断是否是英文，是，则使用英文助手朗读
def is_english(text):
    language = detect(text)
    # print(language)
    if language == 'zh-cn':
        return False
    else:
        return True

# 开始获取音频
def get_audio(resp,text):
    if "url" in resp:  # 检查 url 是否存在
    # resp = {"authorization":"YXBpX2tleT0iZDg0YjlkNzgwYjQ4OGNmOTE5YzUyNzM2ODZlZTRlMWEiLCBhbGdvcml0aG09ImhtYWMtc2hhMjU2IiwgaGVhZGVycz0iaG9zdCBkYXRlIHJlcXVlc3QtbGluZSIsIHNpZ25hdHVyZT0iakdFaEtXVXdxYllqajRONHhNVGhBemlZNjliVm1OcXA4ckZJUEtUVTFHcz0i","url":"https://cn-global.xf-yun.com/v1/private/s62f75860?authorization=YXBpX2tleT0iZDg0YjlkNzgwYjQ4OGNmOTE5YzUyNzM2ODZlZTRlMWEiLCBhbGdvcml0aG09ImhtYWMtc2hhMjU2IiwgaGVhZGVycz0iaG9zdCBkYXRlIHJlcXVlc3QtbGluZSIsIHNpZ25hdHVyZT0iakdFaEtXVXdxYllqajRONHhNVGhBemlZNjliVm1OcXA4ckZJUEtUVTFHcz0i&date=Fri%2C 05 May 2023 11%3A42%3A33 GMT&host=cn-global.xf-yun.com","appId":"12a0a7e2"}
        appId = resp.get("appId", "e71f355f")
        # print(appId)
        url = resp["url"].replace("https://", "wss://")
        connect_websocket(url, appId, text) # 建立wss连接
    else:
        print('语音接口异常')
        print(resp) # 抛出异常

# wss连接方法
def connect_websocket(url, appId, text):
    websocket.enableTrace(False) # 不打印连接内容
    ws = websocket.WebSocketApp(url,
    on_open=on_open,
    on_message=on_message,
    on_error=on_error,
    on_close=on_close)
    ws.app_id = appId # 朗读的版本，鉴权接口提供
    ws.voiceName = choice # 朗读的Ai助手
    ws.text = text # 朗读的文本
    ws.playState = "playing" # 与wss的握手的playState
    ws.audioDatas = list() # 将音频缓存列表初始化为空列表
    ws.run_forever() # 开始建立永久链接，除非对方中断

# wss连接建立时
def on_open(ws):
    print("\nwebsocket建立连接")
    if ws.playState == "unTTS":
        pass
    else:
        data = {
        "header": {
        "app_id": ws.app_id,
        "uid": "39769795890", # js中提供的固定id
        "did": "SR082321940000200", # js中提供的固定did
        "imei": "8664020318693660", # js中提供的固定imei
        "imsi": "4600264952729100",# js中提供的固定imsi
        "mac": "6c:92:bf:65:c6:14",# js中提供的固定mac
        "net_type": "wifi",# js中提供的固定type
        "net_isp": "CMCC",# js中提供的固定isp
        "status": 2,
        "request_id": None,
        "res_id": ""
        },
        "parameter": {
        "tts": {
        "vcn": ws.voiceName, # 朗读的AI助手
        "speed": 50, # 默认语速
        "volume": 50, # 默认音量
        "pitch": 50, 
        "bgs": 0,
        "reg": 0,
        "rdn": 0,
        "rhy": 0,
        "scn": 0,
        "style": "assistant",
        "audio": {
        "encoding": "raw",
        "sample_rate": 16000, # wav的sample_rate
        "channels": 1, # wav的声道
        "bit_depth": 16, # wav的位深度
        "frame_size": 0
        },
        "pybuf": { # 二进制流传输
        "encoding": "utf8",
        "compress": "raw",
        "format": "plain"
        }
        }
        },
        "payload": {
        "text": {
        "encoding": "utf8",
        "compress": "raw",
        "format": "plain",
        "status": 2,
        "seq": 0,
        "text": base64.b64encode(ws.text.encode("utf-8")).decode("utf-8")  # 请求的文本
        }
        }
        }
        ws.send(json.dumps(data))

# wss连接传输时
def on_message(ws, message):
    messageData = json.loads(message) # 解析wss的json数据
    audioData = None
    if messageData and messageData.get("payload") and messageData["payload"].get("audio"):
        audioData = messageData["payload"]["audio"]["audio"] # 解析wss的中音频的base64文本
        print('-', end='')
        # print('seq' + str(messageData["payload"]["audio"]["seq"]))
        # print('id' + str(messageData["payload"]["audio"]["id"]))
        audioBinaryData = base64.b64decode(audioData) # 转回二进制流
        ws.audioDatas.append(audioBinaryData) # 将每次接收到的音频数据保存到列表中

        # 判断是否为最后一帧音频数据
        if messageData['payload']['audio']['status'] == 2:
            # 拼接所有音频数据
            all_audio_data = b''.join(ws.audioDatas)
            with open("讯飞星火 - " + question + ".wav", "wb") as f:
                # 构造WAV文件头部信息
                ced = int(messageData["payload"]["audio"]["ced"])
                nchannels = 1 #声道
                sampwidth = 2 # 16位
                framerate = int(messageData["payload"]["audio"]["sample_rate"])
                nframes = len(all_audio_data) // (nchannels * sampwidth)
                comptype = "NONE"
                compname = "not compressed"
                # 写入wav头部
                header = struct.pack('<4sI4s4sIHHIIHH4sI', b'RIFF', 36 + len(all_audio_data), b'WAVE', b'fmt ',
                                     16, 1, nchannels, framerate, nchannels*sampwidth*framerate, nchannels*sampwidth,
                                     sampwidth*8, b'data', len(all_audio_data))
                # 导出流
                f.write(header)
                f.write(all_audio_data)
            # 清空音频缓存列表
            ws.audioDatas = []
            print('已输出到"讯飞星火 - ' + question + '.wav"')

# wss连接出错
def on_error(ws, error):
    print(error)

# wss连接关闭
def on_close(ws,p1,p2):
    print("100%",end='')

# 执行文本转语音
def done(text,ques):
    global choice
    global question
    question = ques
    choice = get_assist(text)
    url = "https://xinghuo.xfyun.cn/iflygpt/api/tts_sign"
    payload = {'text': text,
    'tts': choice}
    files=[
    ]
    headers = {
        'Origin': 'https://xinghuo.xfyun.cn/desk',
        'Referer': 'https://xinghuo.xfyun.cn/desk',
        'Accept-Encoding': 'gzip, deflate, br',
        'Cookie': userinfo.cookie,
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_1_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Mobile/15E148 Safari/604.1',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'X-Requested-With': 'XMLHttpRequest'
    }
    # print(url)
    # print(headers)
    # print(payload)
    response = requests.request("POST", url, headers=headers, data=payload, files=files) # 发起请求
    # print(response.text)
    get_audio(json.loads(response.text)['data'],text) # 获得响应体

# Main入口，当只执行当前脚本时使用
if __name__ == '__main__':
    try:
        print('您好，我是科大讯飞研发的认知智能大模型，我的名字叫讯飞星火认知大模型。我可以和人类进行自然交流，解答问题，高效完成各领域认知智能需求。') 
        while True:
            a_text = input("\n请输入生成Ai语音的文本：")
            if a_text == 'exit':
                break
            elif a_text != '':
                done(a_text,a_text[:15])
            else:
                pass    
        # 加载会话日志，如果存在则直接读取    
    except KeyboardInterrupt:
        # 保存会话日志并退出程序
        pass
    print("\n感谢您使用讯飞星火认知大模型，欢迎再次使用！")    
