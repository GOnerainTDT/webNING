# 1. 环境安装
`
    pip install -r requirements.txt
`
# 2. 需要修改的部分
如果您的环境向chatgpt发送信息需要使用代理，那么请在app.py修改您代理的端口，如果不需要，您也可以删除代理参数。
```
    # 实例化OpenAIChatClient
    chat_client = OpenAIChatClient(http_proxy="127.0.0.1:您的端口", https_proxy="127.0.0.1:您的端口")
```





