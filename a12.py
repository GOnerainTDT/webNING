from flask import Flask, request

app = Flask(__name__)

@app.before_request
def before_request():
    # 尝试获取X-Forwarded-For头部的第一个值作为真实IP
    if 'X-Forwarded-For' in request.headers:
        real_ip = request.headers.get('X-Forwarded-For').split(',')[0]
        request.remote_addr = real_ip  # 更新request的remote_addr属性

@app.route('/')
def home():
    return f"Your IP is: {request.remote_addr}"

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=8080)
