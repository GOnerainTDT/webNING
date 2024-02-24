from waitress import serve
from a12 import app  # 导入你的 Flask 应用实例

serve(app, host='0.0.0.0', port=8080)
