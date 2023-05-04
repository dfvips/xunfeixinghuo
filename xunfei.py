# This script was created by dreamfly
# author: dreamfly
# github: https://github.com/dfvips
import requests
import base64
import json
import copy
import sys
import userinfo

# 设置请求头
headers = {
    'Accept': 'text/event-stream',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Cookie': userinfo.cookie,
    'Origin': 'https://xinghuo.xfyun.cn',
    'Referer': 'https://xinghuo.xfyun.cn/desk',
    'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
}

# 生成会话ID，每次重新开始，会生成新的会话
def generate_chat_id():
    url = 'https://xinghuo.xfyun.cn/iflygpt/u/chat-list/v1/create-chat-list' # 请求会话地址
    chat_header = copy.copy(headers)
    chat_header['Accept'] = 'application/json, text/plain, */*'
    chat_header['Content-Type'] = 'application/json'
    chat_header['X-Requested-With'] = 'XMLHttpRequest' # 设置请求头
    payload = "{}" # 请求体
    response = requests.request("POST", url, headers=chat_header, data = payload) # 发起请求
    # 处理响应数据
    response_data = json.loads(response.text) 
    if response_data['code'] == 0:
        chat_list_id = response_data['data']['id']
        return chat_list_id
    else:
        return '0'

# 解密base64数据
def decode(text):
     try:
        decoded_data = base64.b64decode(text).decode('utf-8')
        # 返回处理解码后的数据
        return decoded_data
     except Exception as e:
        return  ''

# 请求提问接口
def ask_question(question,chat_id):
    url = "https://xinghuo.xfyun.cn/iflygpt/u/chat_message/chat"
    payload = {
        # 'fd': userinfo.fd, ## 用户FD，可省略
        'chatId': chat_id,
        'text': question, # 提交的问题
        # 'GtToken': userinfo.GtToken,  ## 用户GtToken，可省略
        'clientType': '1' # 默认值，网页
    }
    response = requests.request("POST", url, headers=headers, data = payload, stream=True)
    # 逐行响应
    for line in response.iter_lines():
        if line:
            encoded_data = line[len("data:"):]
            # 补全填充处理base64字符
            missing_padding = len(encoded_data) % 4
            if missing_padding != 0:
                encoded_data += b'=' * (4 - missing_padding)
            # 现在你可以处理解码后的数据
            if decode(encoded_data) != 'zw':
               sys.stdout.flush() # 实时回复
               print(decode(encoded_data), end='')
               
# Main入口
try:
    chat_id = generate_chat_id() # 生成会话
    # print(chat_id)
    # ask_question('介绍下自己') ## 因为每次都是介绍这句话，所以不请求了。
    print('您好，我是科大讯飞研发的认知智能大模型，我的名字叫讯飞星火认知大模型。我可以和人类进行自然交流，解答问题，高效完成各领域认知 智能需求。') 
    while True:
        question = input("\n\n请输入您的问题：")
        if question == 'exit':
            break
        ask_question(question,chat_id) # 发起提问
except KeyboardInterrupt:
    print("\n\n感谢您使用讯飞星火认知大模型，欢迎再次使用！")