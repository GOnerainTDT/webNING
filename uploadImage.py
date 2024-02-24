import os
import datetime
import random
from flask import request

def save_uploaded_file(upload_folder, file):
    _, file_extension = os.path.splitext(file.filename)
    current_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    random_number = random.randint(1000, 9999)
    new_filename = f"{current_time}_{random_number}{file_extension}"
    save_path = os.path.join(upload_folder, new_filename)
    file.save(save_path)
    return save_path

def get_visitor_ip():
    headers = request.headers
    x_forwarded_for = headers.get('X-Forwarded-For')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.remote_addr

def process_qr_data(qr_data):
    if qr_data == "":
        return "我不知道你的名字，陌生人", "0", "2000-01-01", "QR数据格式不正确或不完整"
    data_parts = qr_data.split(", ")
    if len(data_parts) == 3:
        return *data_parts, ""
    return "我不知道你的名字，陌生人", "0", "2000-01-01", "QR数据格式不正确或不完整"