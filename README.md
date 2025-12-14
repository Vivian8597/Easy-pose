# Easy-pose - 你的拍照姿势助手

## 项目简介

Easy-pose 是一个基于 AI 的拍照姿势推荐应用，用户可以上传场景图片，选择风格偏好，获取 AI 生成的真人姿势参考图片。

## 功能特点

- **场景分析**：自动分析上传图片的场景特征，包括场景类型、光线条件、主色调等
- **风格匹配**：支持多种风格偏好选择
- **AI 姿势生成**：基于阿里云 DashScope API 生成符合场景的真人姿势参考图片
- **拍摄建议**：提供专业的拍摄建议，包括角度、位置、光线等
- **大图预览**：支持点击查看 AI 生成图片的大图

## 技术栈

- **后端**：Python Flask
- **前端**：HTML, CSS, JavaScript, Bootstrap
- **AI 服务**：阿里云 DashScope API (qwen-image-edit-plus 模型)
- **图像处理**：OpenCV
- **依赖管理**：pip

## 目录结构

```
.
├── app/                    # 主应用目录
│   ├── static/             # 静态资源
│   │   ├── css/            # CSS 样式文件
│   │   └── js/             # JavaScript 文件
│   ├── templates/          # HTML 模板
│   ├── utils/              # 工具模块
│   │   ├── ai_image_generator.py  # AI 图片生成
│   │   ├── advice_generator.py     # 拍摄建议生成
│   │   ├── image_analyzer.py       # 图像分析
│   │   ├── image_searcher.py       # 图像搜索
│   │   └── style_matcher.py        # 风格匹配
│   ├── __init__.py         # 应用初始化
│   └── routes.py           # 路由定义
├── uploads/                # 上传文件存储目录
├── .env                    # 环境变量配置
├── requirements.txt        # 依赖列表
├── run.py                  # 应用启动脚本
└── README.md               # 项目文档
```

## 安装和运行

### 1. 克隆仓库

```bash
git clone <your-repo-url>
cd Easy-pose
```

### 2. 创建虚拟环境（可选）

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置环境变量

在 `.env` 文件中配置阿里云 DashScope API 密钥：

```
# DashScope API配置（用于qwen-image-edit-plus模型）
DASHSCOPE_API_KEY=your_api_key
DASHSCOPE_API_URL=https://dashscope.aliyuncs.com/api/v1
```

### 5. 运行应用

```bash
python run.py
```

应用将在 `http://127.0.0.1:5000` 启动

## 使用指南

1. **上传场景图片**：点击或拖拽图片到上传区域
2. **选择风格**：从风格列表中选择您喜欢的风格
3. **获取推荐**：点击 "获取推荐" 按钮
4. **查看结果**：
   - 查看场景分析结果
   - 查看拍摄建议
   - 查看 AI 生成的姿势参考图片
   - 点击图片查看大图

## 注意事项

- 支持 JPG、PNG 格式图片，最大 16MB
- 确保网络连接正常，以便使用 AI 生成功能
- 首次使用可能需要等待几秒钟，因为 AI 生成图片需要时间
- 页面可能会显示 Bootstrap Icons CDN 加载失败的错误，这是 CDN 访问限制导致的，不会影响应用核心功能

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 联系方式

如有问题或建议，请通过 GitHub Issues 联系我们。