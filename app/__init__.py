from flask import Flask
from flask_cors import CORS
import os

# 创建Flask应用实例
app = Flask(__name__)

# 配置CORS，允许跨域请求
CORS(app)

# 设置上传文件夹（使用应用根目录的相对路径）
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

# 确保上传文件夹存在
UPLOAD_FOLDER = app.config['UPLOAD_FOLDER']
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# 导入路由
from app import routes
