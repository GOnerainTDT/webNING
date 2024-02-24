from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_session import Session
import redis
from werkzeug.utils import secure_filename
from pyzbar.pyzbar import decode
from PIL import Image
import os
import cv2
import numpy as np
import datetime
import ipadrr
import weather
import random
import haveFood
import fortune
import uploadImage
from chatGPTClient import OpenAIChatClient

app = Flask(__name__)
app.secret_key = 'Sxyyyxn1.'

UPLOAD_FOLDER = 'uploads/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Flask-Session配置
app.config["SESSION_TYPE"] = "redis"  # 使用Redis存储会话
app.config["SESSION_PERMANENT"] = False  # 会话不是永久性的
app.config["SESSION_USE_SIGNER"] = True  # 加密cookie
app.config["SESSION_KEY_PREFIX"] = "session:"  # 会话在Redis中的前缀
app.config["SESSION_REDIS"] = redis.StrictRedis(host='localhost', port=6379, db=0)  # Redis数据库的配置

Session(app)  # 初始化应用以使用Flask-Session

# 初始化二维码检测器
detector = cv2.QRCodeDetector()

# 实例化OpenAIChatClient
chat_client = OpenAIChatClient(http_proxy="127.0.0.1:7890", https_proxy="127.0.0.1:7890")

# 首页路由
@app.route('/')
def index():
    return render_template('index.html')

# Generic 页面路由
@app.route('/wish')
def generic():
    return render_template('generic.html')

@app.route('/upload_image', methods=['POST'])
def upload_image():
    file = request.files.get('fileInput')
    if not file or file.filename == '':
        flash('No file selected')
        return redirect(request.url)
    
    usr_image = None
    try:
        # 将文件对象转换为PIL图像对象
        image = Image.open(file.stream)

        # 确保图像模式是RGB
        if image.mode != 'RGB':
                image = image.convert('RGB')

        # 将PIL图像对象转换为numpy数组
        image_np = np.array(image)
        usr_image = image_np

    except Exception as e:
        print(e)
        return redirect(request.url)

    # 保存图片
    # save_path = uploadImage.save_uploaded_file(app.config['UPLOAD_FOLDER'] ,file)
    # image_np = cv2.imread(save_path)
    # 读取二维码
    qr_data, _, _ = detector.detectAndDecode(usr_image)
    # ip位置
    visitor_ip = uploadImage.get_visitor_ip()
    usrCountry, usrCity = ipadrr.get_location(visitor_ip)
    
    usrName, id, birthday, message = uploadImage.process_qr_data(qr_data)
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if qr_data:
        usr_weather_info, usr_city_temp, usr_city_weather = weather.get_weather(usrCity)  # 假设已获取天气信息
        # str_fortune = usrName + "," + haveFood.ask_about_meal() + weather.get_weather(usrCity) + fortune.get_fortune(birthday)
        str_fortune = chat_client.get_personalized_message(name=usrName, city=usrCity, weather_info=usr_city_weather,temp=usr_city_temp)
        print(str_fortune)
        # str_fortune = chat_client.get_personalized_message(name="谢宁", city="沈阳", weather_info="大雪",temp="4摄氏度")
        return jsonify(success=True, name=usrName, id=id, birthday=birthday, current_time=current_time, visitor_ip=visitor_ip, country=usrCountry, city=usrCity, strFortune=str_fortune, message=message)
    
    return jsonify(success=False, message='No QR Code detected' if not qr_data else message, current_time=current_time, visitor_ip=visitor_ip, country=usrCountry, city=usrCity, strFortune="")


# Elements 页面路由
@app.route('/chatRobo')
def elements():
    OpenAIChatClient.check_and_reset_limit()  # 确保每天重置
    remaining = OpenAIChatClient.daily_limit - OpenAIChatClient.request_count
    return render_template('chat.html', remaining=remaining)

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.form['message']
    conversation_history = session.get('conversation_history', [])
    
    # 更新聊天历史
    conversation_history.append({'role': 'user', 'content': user_message})
    session['conversation_history'] = conversation_history
    
    # 获取回复
    reply = chat_client.get_response_session(conversation_history)
    
    # 将回复也添加到历史中
    conversation_history.append({'role': 'assistant', 'content': reply})
    session['conversation_history'] = conversation_history

    OpenAIChatClient.check_and_reset_limit()  # 确保每天重置
    usr_remaining = OpenAIChatClient.daily_limit - OpenAIChatClient.request_count

    print(OpenAIChatClient.daily_limit,OpenAIChatClient.request_count,usr_remaining)
    
    return jsonify({"reply": reply, "remaining": usr_remaining})
    # user_message = request.form['message']
    # print(user_message)
    # reply = chat_client.get_response(user_message)
    # print(reply)
    # return jsonify({"reply": reply})

# Elements 页面路由
@app.route('/map')
def uploads():
    return render_template('elements.html')
    

if __name__ == '__main__':
    app.run(port=5000)
