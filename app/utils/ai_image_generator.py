import json
import os
from dotenv import load_dotenv
from dashscope import MultiModalConversation
import dashscope

# 加载环境变量
load_dotenv()

class AIImageGenerator:
    def __init__(self):
        # 初始化阿里云DashScope API配置
        self.api_key = os.environ.get("DASHSCOPE_API_KEY", "")
        self.model = "qwen-image-edit-plus"
        
        # 配置DashScope API URL
        # 以下为中国（北京）地域url，若使用新加坡地域的模型，需将url替换为： `https://dashscope-intl.aliyuncs.com/api/v1`
        dashscope.base_http_api_url = os.environ.get("DASHSCOPE_API_URL", "https://dashscope.aliyuncs.com/api/v1")
    
    def generate_images(self, scene_features, style, prompt_template=None, num_images=3):
        """
        根据场景特征和风格生成参考图片
        :param scene_features: 场景特征字典
        :param style: 风格
        :param prompt_template: 提示词模板
        :param num_images: 生成图片数量
        :return: 生成的图片URL列表
        """
        # 这个方法暂时不使用，因为我们只需要基于输入图片生成AI参考图片
        return []
    
    def _generate_prompt(self, scene_features, style):
        """
        生成AI生成图片的提示词
        :param scene_features: 场景特征字典
        :param style: 风格
        :return: 生成的提示词
        """
        # 构建提示词，使用真人代替火柴人，强调动作、姿势、大小与环境背景的和谐
        prompt = f"我将要在这个场景中拍照，帮我生成3张推荐的姿势参考图片，要求：1. 不改变上传的原始场景图片；2. 每张图片只有一个人；3. 人物站位合理，与场景和谐；4. 动作多样，三张照片之间的动作各不相同；5. 人物穿着符合场景；6. 不在场景之外添加其他物品；7. 强调人的动作、姿势、大小与环境背景的和谐。风格偏好：{style}。场景是{scene_features['scene_type']}，光线{scene_features['light_type']}，主色调{scene_features['colors']['dominant_color']}。"
        
        # 添加详细场景描述
        if "scene_description" in scene_features:
            prompt += f" 场景描述：{scene_features['scene_description']}"
        
        return prompt
    
    def generate_images_from_image(self, image_path, scene_features, style, num_images=3):
        """
        基于输入图片生成AI参考姿势推荐图片
        :param image_path: 输入图片路径
        :param scene_features: 场景特征字典
        :param style: 风格
        :param num_images: 生成图片数量
        :return: 生成的图片URL列表
        """
        try:
            # 生成提示词
            prompt = self._generate_prompt(scene_features, style)
            
            # 调用DashScope API生成AI姿势推荐图片
            images = self._call_dashscope_api(image_path, prompt, num_images)
            
            return images
        except Exception as e:
            print(f"AI image generation from image error: {e}")
            # 如果API调用失败，返回空列表
            return []
    
    def _call_dashscope_api(self, image_path, prompt, num_images=3):
        """
        调用阿里云DashScope API生成AI姿势推荐图片
        :param image_path: 输入图片路径
        :param prompt: 提示词
        :param num_images: 生成图片数量
        :return: 生成的图片URL列表
        """
        # 读取图片并编码为base64
        import base64
        with open(image_path, "rb") as f:
            image_data = f.read()
            base64_image = base64.b64encode(image_data).decode("utf-8")
        
        # 构建messages
        messages = [
            {
                "role": "user",
                "content": [
                    {"image": f"data:image/jpeg;base64,{base64_image}"},
                    {"text": prompt}
                ]
            }
        ]
        
        # 调用DashScope API
        response = MultiModalConversation.call(
            api_key=self.api_key,
            model=self.model,
            messages=messages,
            stream=False,
            n=num_images,
            watermark=False,
            negative_prompt=" ",
            prompt_extend=True
        )
        
        images = []
        
        if response.status_code == 200:
            # 解析响应，提取图片URL
            for i, content in enumerate(response.output.choices[0].message.content):
                if "image" in content:
                    images.append({
                        "url": content["image"],
                        "thumbnail": content["image"],
                        "source": "aliyun_qwen",
                        "photographer": "阿里云通义千问生成",
                        "prompt": prompt
                    })
        else:
            print(f"HTTP返回码：{response.status_code}")
            print(f"错误码：{response.code}")
            print(f"错误信息：{response.message}")
            print("请参考文档： `https://help.aliyun.com/zh/model-studio/developer-reference/error-code` ")
        
        return images
