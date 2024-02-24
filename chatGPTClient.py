# imports
import datetime  # for measuring time duration of API calls
from openai import OpenAI
import openai
import os

class OpenAIChatClient:
    daily_limit = 100  # 设置每日请求次数限制
    request_count = 99  # 初始化请求计数
    last_reset_date = datetime.date.today()  # 记录最后一次重置计数的日期

    def __init__(self, http_proxy=None, https_proxy=None):
        # 配置代理
        if http_proxy:
            os.environ["HTTP_PROXY"] = http_proxy
        if https_proxy:
            os.environ["HTTPS_PROXY"] = https_proxy
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "<your OpenAI API key if not set as env var>"))
        self.conversation_history = []  # 初始化对话历史记录

    @classmethod
    def check_and_reset_limit(cls):
        # 如果当前日期不是最后一次重置的日期，则重置计数和日期
        today = datetime.date.today()
        if cls.last_reset_date < today:
            cls.request_count = 0
            cls.last_reset_date = today

    def get_response_session(self, user_message):
        self.check_and_reset_limit()  # 检查是否需要重置计数
        if self.request_count >= self.daily_limit:
            return "我累了，请让我休息一下吧。 (为了防止恶意攻击，所以设置了每日最大请求chat次数，我的朋友，请您见谅)"
        try:
            # 发送ChatCompletion请求
            response = self.client.chat.completions.create(
                model='gpt-4-0125-preview',
                messages=user_message,
                temperature=0,
                stream=True  # 启用流式响应
            )

            # 从响应中获取完整消息并返回
            full_response = self.get_fullRecived_fromResponse(response)
            
        except Exception as e:
            # 处理其他所有未知错误
            full_response = ""

        OpenAIChatClient.request_count += 1  # 增加请求计数
        return full_response
    
    def get_response(self, user_message):
        self.check_and_reset_limit()  # 检查是否需要重置计数
        if self.request_count >= self.daily_limit:
            return "我累了，请让我休息一下吧。 (为了防止恶意攻击，所以设置了每日最大请求chat次数，我的朋友，请您见谅)"
        # 将用户消息添加到对话历史
        self.conversation_history.append({'role': 'user', 'content': user_message})

        try:
            # 发送ChatCompletion请求
            response = self.client.chat.completions.create(
                model='gpt-4-0125-preview',
                messages=self.conversation_history,
                temperature=0,
                stream=True  # 启用流式响应
            )

            # 从响应中获取完整消息并返回
            full_response = self.get_fullRecived_fromResponse(response)
            
        except Exception as e:
            # 处理其他所有未知错误
            full_response = ""

        # 将模型的回复也添加到对话历史中
        self.conversation_history.append({'role': 'assistant', 'content': full_response})

        OpenAIChatClient.request_count += 1  # 增加请求计数
        return full_response
    
    def get_fullRecived_fromResponse(self, response):
        collected_messages = []
        for chunk in response:
            chunk_message = chunk.choices[0].delta.content  # extract the message
            collected_messages.append(chunk_message)  # save the message
        collected_messages = [m for m in collected_messages if m is not None]
        return ''.join([m for m in collected_messages])


    def printRecived_stream(self, response):
        for chunk in response:
            content = chunk.choices[0].delta.content
            if content:  # 确保内容不是None
                print(content, end='')  # 不换行打印内容
    
    def get_personalized_message(self, name, city, weather_info,temp):
        current_time = datetime.datetime.now()
        time_str = current_time.strftime('%Y-%m-%d %H:%M:%S')
        hour = current_time.hour
        # part_of_day = "晚上" if 18 <= hour <= 23 or 0 <= hour <= 6 else "白天"
        prompt = f"请你作为'{name}'的朋友，根据当前时间'{time_str}'，地点'{city}'、天气'{weather_info}'和温度'{temp}'℃，同时随机给出一个当日运势，提供一句寄语（100字左右，要求中文回答）。"
        response = self.get_response(prompt)
        return response

        
#使用示例
if __name__ == "__main__":
    chat = OpenAIChatClient(http_proxy="127.0.0.1:7890", https_proxy="127.0.0.1:7890")  # 确保替换成你的API密钥
    messages = [
        {'role': 'user', 'content': "Count to 100, with a comma between each number and no newlines. E.g., 1, 2, 3, ..."}
    ]

    print(chat.get_personalized_message(name="谢宁", city="沈阳", weather_info="大雪",temp="4摄氏度"))

    # # 第一轮对话
    # user_message_1 = "Count to 100, with a comma between each number and no newlines. E.g., 1, 2, 3, ..."
    # print(chat.get_response(user_message_1))
    
    # # 第二轮对话，可以引用上下文
    # user_message_2 = "What did you just do?"
    # print(chat.get_response(user_message_2))

    # print(chat.get_fullRecived_fromResponse(response))
    # chat.printRecived_stream(response)