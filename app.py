from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
from pyzbar.pyzbar import decode
from PIL import Image
import os
import cv2
import datetime
import random
import ipadrr
import haveFood
import weather
import fortune

app = Flask(__name__)
app.secret_key = 'Sxyyyxn1.'

UPLOAD_FOLDER = 'uploads/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 初始化二维码检测器
detector = cv2.QRCodeDetector()

# 首页路由
@app.route('/')
def index():
    return render_template('index.html')

# Generic 页面路由
@app.route('/generic')
def generic():
    return render_template('generic.html')

@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'fileInput' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['fileInput']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file:
        _, file_extension = os.path.splitext(file.filename)
        current_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        random_number = random.randint(1000, 9999)
        new_filename = f"{current_time}_{random_number}{file_extension}"
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
        file.save(save_path)

        # 二维码识别
        image = cv2.imread(save_path)
        # 检测并解码二维码
        qr_data, bbox, straight_qrcode = detector.detectAndDecode(image)
        headers = request.headers
        x_forwarded_for = headers.get('X-Forwarded-For')
        visitor_ip = request.remote_addr  # 获取访问者的 IP 地址
        if x_forwarded_for is None:
            visitor_ip = request.remote_addr
        else:
            visitor_ip = x_forwarded_for.split(',')[0]  # 取第一个IP地址
        country, city = ipadrr.get_location(visitor_ip)
        print(visitor_ip)
        print(city)
        str_fortune = ""
        if qr_data != "":
            # 使用split方法按照", "分割字符串
            data_parts = qr_data.split(", ")
            # 分割后的数据
            if len(data_parts) == 3:
                name, id, birthday = data_parts
                print(f"姓名: {name}")
                print(f"身份证号: {id}")
                print(f"生日: {birthday}")
            else:
                name, id, birthday = "我不知道你的名字，陌生人", "0", "2000-01-01"
                print("QR数据格式不正确或不完整")
                
            current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            str_fortune = name + "," + haveFood.ask_about_meal() + weather.get_weather(city) + fortune.get_fortune(birthday)
            return jsonify({
                'success': True,
                'name': name,
                'id':id,
                'birthday':birthday,
                'current_time': current_time,
                'visitor_ip': visitor_ip,  # 返回访问者的 IP 地址
                'country': country,
                'city': city,
                'strFortune': str_fortune
            })
        else:
            current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            return jsonify({
                'success': False,
                'message': 'No QR Code detected',
                'current_time': current_time,
                'visitor_ip': visitor_ip,  # 返回访问者的 IP 地址
                'country': country,
                'city': city,
                'strFortune': str_fortune
            })
        
    return redirect(url_for('generic'))
# @app.route('/upload_image', methods=['POST'])
# def upload_image():
#     if 'fileInput' not in request.files:
#         flash('No file part')
#         return redirect(request.url)
#     file = request.files['fileInput']
#     if file.filename == '':
#         flash('No selected file')
#         return redirect(request.url)
#     if file:
#         # 获取文件扩展名
#         _, file_extension = os.path.splitext(file.filename)
#         # 生成新的文件名
#         current_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
#         random_number = random.randint(1000, 9999)
#         new_filename = f"{current_time}_{random_number}{file_extension}"
#         # 确保上传目录存在
#         if not os.path.exists(app.config['UPLOAD_FOLDER']):
#             os.makedirs(app.config['UPLOAD_FOLDER'])
#         save_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
#         file.save(save_path)
#         flash('File uploaded successfully')
#     return redirect(url_for('generic'))

# Elements 页面路由
@app.route('/elements')
def elements():
    return render_template('elements.html')

# Elements 页面路由
@app.route('/upload')
def uploads():
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
