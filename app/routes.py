from flask import request, jsonify, render_template
from app import app
from app.utils.image_analyzer import ImageAnalyzer
from app.utils.style_matcher import StyleMatcher
from app.utils.image_searcher import ImageSearcher
from app.utils.advice_generator import AdviceGenerator
from app.utils.ai_image_generator import AIImageGenerator
import os
from werkzeug.utils import secure_filename

# 初始化各个模块
image_analyzer = ImageAnalyzer()
style_matcher = StyleMatcher()
image_searcher = ImageSearcher()
advice_generator = AdviceGenerator()
ai_image_generator = AIImageGenerator()

# 主页路由
@app.route('/')
def home():
    return render_template('index.html')

# 获取可用风格列表
@app.route('/api/styles', methods=['GET'])
def get_styles():
    styles = style_matcher.get_available_styles()
    return jsonify({'styles': styles})

# 上传图片路由
@app.route('/api/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return jsonify({'filename': filename, 'filepath': filepath})

# 姿势推荐主路由
@app.route('/api/recommend', methods=['POST'])
def recommend_pose():
    try:
        # 获取请求数据
        data = request.form
        image_file = request.files.get('image')
        style = data.get('style')
        
        if not image_file or not style:
            return jsonify({'error': 'Missing image or style parameter'}), 400
        
        # 保存上传的图片
        filename = secure_filename(image_file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image_file.save(filepath)
        
        # 1. 分析图片
        scene_features = image_analyzer.analyze(filepath)
        
        # 2. 风格匹配
        style_features = style_matcher.match_style(style)
        
        # 3. 生成拍摄建议
        advice = advice_generator.generate_advice(scene_features, style)
        
        # 4. AI生成参考图片
        ai_reference_images = ai_image_generator.generate_images_from_image(
            filepath, 
            scene_features, 
            style, 
            num_images=3
        )
        
        # 返回结果
        result = {
            'scene_features': scene_features,
            'style': style,
            'ai_reference_images': ai_reference_images,
            'advice': advice
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
