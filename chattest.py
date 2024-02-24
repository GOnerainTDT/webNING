import openai
import os
import json

class OpenAIChatClient:
    def __init__(self, api_key_path, http_proxy=None, https_proxy=None):
        # 配置代理
        if http_proxy:
            os.environ["HTTP_PROXY"] = http_proxy
        if https_proxy:
            os.environ["HTTPS_PROXY"] = https_proxy
        
        # 设置API密钥
        self.api_key = self.get_api_key(api_key_path)
        openai.api_key = self.api_key

    def get_api_key(self, api_key_path):
        # 从文件中读取API密钥
        with open(api_key_path, 'r', encoding='utf-8') as f:
            openai_key = json.loads(f.read())
        return openai_key['api']

    def query(self, model, messages):
        # 发送请求并获取回复
        completion = openai.ChatCompletion.create(
            model=model,
            messages=messages
        )
        return completion.choices[0].message

# 使用示例
if __name__ == "__main__":
    api_key_path = '../envs/openai_key'  # API密钥文件路径
    client = OpenAIChatClient(api_key_path, "http://127.0.0.1:7890", "http://127.0.0.1:7890")
    
    messages = [
        {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
        {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
    ]
    
    response = client.query("gpt-3.5-turbo", messages)
    print(response)
