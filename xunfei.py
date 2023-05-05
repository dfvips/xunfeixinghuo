import requests
import base64
import json
import copy
import sys
import user

# 定义全局变量
chat_id = None
is_new_session = True
log_file_name = "session_log.json"

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

chat_header = copy.copy(headers)
chat_header['Accept'] = 'application/json, text/plain, */*'
chat_header['Content-Type'] = 'application/json'
chat_header['X-Requested-With'] = 'XMLHttpRequest'

# 加载会话日志
def load_session_log():
    global chat_id
    try:
        with open(log_file_name, "r", encoding='utf-8') as f:
            log_data = json.load(f)
            chat_id = log_data["chat_id"]
        return True
    except:
        return False

# 保存会话日志
def save_session_log():
    global chat_id
    session_log = {"chat_id": chat_id}
    with open(log_file_name, "w", encoding='utf-8') as f:
        json.dump(session_log, f, ensure_ascii=False, indent=4)

# 生成会话ID，每次重新开始，会生成新的会话
def generate_chat_id():
    url = 'https://xinghuo.xfyun.cn/iflygpt/u/chat-list/v1/create-chat-list'
    payload = "{}"
    response = requests.request("POST", url, headers=chat_header, data=payload)
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
        return decoded_data
     except Exception as e:
        return ''

# 请求提问接口
def ask_question(question, chat_id):
    url = "https://xinghuo.xfyun.cn/iflygpt/u/chat_message/chat"
    payload = {
        'fd': userinfo.fd,
        'chatId': chat_id,
        'text': question,
        'GtToken': userinfo.GtToken,
        'clientType': '1'
    }
    response = requests.request("POST", url, headers=headers, data=payload, stream=True)
    response_text = ''
    for line in response.iter_lines():
        if line:
            encoded_data = line[len("data:"):]
            missing_padding = len(encoded_data) % 4
            if missing_padding != 0:
                encoded_data += b'=' * (4 - missing_padding)
            if decode(encoded_data) != 'zw':
                sys.stdout.flush()
                answer = decode(encoded_data).replace('\n\n', '\n')
                response_text += answer
                print(answer, end='')
    # 记录会话日志
    with open(f"{chat_id}.json", "a", encoding='utf-8') as f:
        log_data = {"chat_id":chat_id, "question": question, "answer": response_text}
        json.dump(log_data, f, ensure_ascii=False)
        f.write("\n")

# 重命名会话
def set_name(question, chat_id):
    url = "https://xinghuo.xfyun.cn/iflygpt/u/chat-list/v1/rename-chat-list"
    question = question[:15]
    payload = {
        'chatListId': chat_id,
        'chatListName': question,
    }
    response = requests.request("POST", url, headers=chat_header, data=json.dumps(payload))
    response_data = json.loads(response.text)
    if response_data['code'] != 0:
        print('\n初始化会话名称失败')

try:
    # 加载会话日志，如果存在则直接读取
    if not load_session_log():
        is_new_session = True
        chat_id = generate_chat_id() # 生成新的会话ID
        set_name("新会话", chat_id) # 设置会话名称
    else:
        # 提示是否载入上次的会话
        while True:
            answer = input("是否载入上次的会话？(Y/N): ")
            if answer.upper() == "Y":
                is_new_session = False
                break
            elif answer.upper() == "N":
                is_new_session = True
                chat_id = generate_chat_id() # 生成新的会话ID
                break
            else:
                print("请输入正确的选项！")
    count = 0
    print('您好，我是科大讯飞研发的认知智能大模型，我的名字叫讯飞星火认知大模型。我可以和人类进行自然交流，解答问题，高效完成各领域认知智能需求。') 
    while True:
        count += 1
        question = input("\n请输入您的问题：")
        if question == 'exit':
            break
        ask_question(question, chat_id)
        if is_new_session == True &  count == 1:
            set_name(question, chat_id) # 设置会话名称
    # 保存会话日志
    save_session_log()
except KeyboardInterrupt:
    # 保存会话日志并退出程序
    save_session_log()
print("\n感谢您使用讯飞星火认知大模型，欢迎再次使用！")
