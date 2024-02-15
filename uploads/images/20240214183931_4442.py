import qrcode

# 人物信息
name = "张三"
id = "12345678"
birthday = "1990-01-01"

# 将信息格式化为一个字符串
qr_data = f"姓名：{name}, ID：{id}, 生日：{birthday}"

# 生成二维码
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(qr_data)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")
img.save("person_qr.png")
