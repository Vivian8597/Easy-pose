import cv2
import numpy as np
from PIL import Image
import os

class ImageAnalyzer:
    def __init__(self):
        # 初始化模型和参数
        self.scene_categories = ['indoor', 'outdoor', 'nature', 'city', 'beach', 'mountain', 'forest', 'urban']
        self.light_categories = ['bright', 'dim', 'soft', 'harsh']
    
    def analyze(self, image_path):
        """
        分析图片，提取场景特征
        :param image_path: 图片路径
        :return: 场景特征字典
        """
        # 读取图片
        image = cv2.imread(image_path)
        if image is None:
            raise Exception(f"Failed to read image: {image_path}")
        
        # 转换为RGB格式
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # 图片预处理
        image_resized = cv2.resize(image_rgb, (224, 224))
        
        # 1. 场景分类（简化实现，实际可使用预训练模型）
        scene_type = self._classify_scene(image)
        
        # 2. 光线分析
        light_type = self._analyze_light(image)
        
        # 3. 色彩分析
        color_features = self._analyze_color(image)
        
        # 4. 内容分析（简化实现）
        content_features = self._analyze_content(image)
        
        # 5. 详细场景描述
        scene_description = self._generate_scene_description(scene_type, light_type, color_features, content_features)
        
        # 6. 场景元素分析
        scene_elements = self._analyze_scene_elements(scene_type)
        
        # 整合所有特征（包含更详细的场景分析）
        scene_features = {
            'scene_type': scene_type,
            'scene_description': scene_description,
            'scene_elements': scene_elements,
            'light_type': light_type,
            'colors': color_features,
            'content': content_features,
            'image_size': image.shape[:2],  # (height, width)
            'detailed_analysis': {
                'scene_summary': f'这是一张{color_features["dominant_color"]}色调的{scene_type}场景照片，光线{light_type}，场景复杂度{content_features["complexity"]}',
                'lighting_summary': self._get_lighting_summary(light_type),
                'color_summary': self._get_color_summary(color_features),
                'composition_summary': self._get_composition_summary(content_features)
            }
        }
        
        return scene_features
    
    def _generate_scene_description(self, scene_type, light_type, color_features, content_features):
        """
        生成详细的场景描述
        :param scene_type: 场景类型
        :param light_type: 光线类型
        :param color_features: 色彩特征
        :param content_features: 内容特征
        :return: 场景描述字符串
        """
        descriptions = {
            'nature': {
                'bright': {
                    'warm': '明亮温暖的自然场景，可能包含绿色植被和温暖的阳光',
                    'cool': '明亮清爽的自然场景，可能包含蓝天、水域或茂密的绿色植物',
                    'fresh': '明亮清新的自然场景，充满生机的绿色植物',
                    'vibrant': '明亮鲜艳的自然场景，色彩丰富，充满活力'
                },
                'soft': {
                    'warm': '柔和温暖的自然场景，可能是清晨或傍晚的柔和阳光',
                    'cool': '柔和凉爽的自然场景，可能是阴天或树荫下',
                    'fresh': '柔和清新的自然场景，可能是雨后或清晨的清新空气',
                    'vibrant': '柔和鲜艳的自然场景，色彩柔和但丰富'
                },
                'dim': {
                    'warm': '昏暗温暖的自然场景，可能是日落时分或森林深处',
                    'cool': '昏暗凉爽的自然场景，可能是阴天的森林或傍晚的水域',
                    'fresh': '昏暗清新的自然场景，可能是清晨的迷雾森林',
                    'vibrant': '昏暗但色彩鲜明的自然场景，可能是夜晚的萤火虫或极光'
                },
                'harsh': {
                    'warm': '强光温暖的自然场景，可能是正午的阳光直射',
                    'cool': '强光凉爽的自然场景，可能是雪地或海滩的强光反射',
                    'fresh': '强光清新的自然场景，可能是高山或高原的强烈阳光',
                    'vibrant': '强光鲜艳的自然场景，色彩对比强烈'
                }
            },
            'city': {
                'bright': {
                    'warm': '明亮温暖的城市场景，可能是夕阳下的城市建筑',
                    'cool': '明亮凉爽的城市场景，可能是白天的现代城市',
                    'fresh': '明亮清新的城市场景，可能是城市公园或绿化带',
                    'vibrant': '明亮鲜艳的城市场景，色彩丰富的城市景观'
                },
                'soft': {
                    'warm': '柔和温暖的城市场景，可能是傍晚的城市灯光',
                    'cool': '柔和凉爽的城市场景，可能是阴天的城市街道',
                    'fresh': '柔和清新的城市场景，可能是雨后的城市街道',
                    'vibrant': '柔和鲜艳的城市场景，色彩柔和的城市夜景'
                },
                'dim': {
                    'warm': '昏暗温暖的城市场景，可能是夜晚的城市小巷',
                    'cool': '昏暗凉爽的城市场景，可能是夜晚的现代城市建筑',
                    'fresh': '昏暗清新的城市场景，可能是清晨的城市公园',
                    'vibrant': '昏暗鲜艳的城市场景，可能是夜晚的霓虹灯街道'
                },
                'harsh': {
                    'warm': '强光温暖的城市场景，可能是正午阳光下的城市广场',
                    'cool': '强光凉爽的城市场景，可能是玻璃幕墙反射的强烈阳光',
                    'fresh': '强光清新的城市场景，可能是城市喷泉或水景',
                    'vibrant': '强光鲜艳的城市场景，色彩对比强烈的城市景观'
                }
            },
            'beach': {
                'bright': {
                    'warm': '明亮温暖的海滩场景，阳光明媚的沙滩和海水',
                    'cool': '明亮凉爽的海滩场景，晴朗的蓝天和海水',
                    'fresh': '明亮清新的海滩场景，清新的海风和海浪',
                    'vibrant': '明亮鲜艳的海滩场景，色彩丰富的海滩活动'
                },
                'soft': {
                    'warm': '柔和温暖的海滩场景，日落时分的海滩',
                    'cool': '柔和凉爽的海滩场景，阴天的海滩',
                    'fresh': '柔和清新的海滩场景，清晨的海滩',
                    'vibrant': '柔和鲜艳的海滩场景，日落时分的彩色天空'
                },
                'dim': {
                    'warm': '昏暗温暖的海滩场景，夜晚的海滩篝火',
                    'cool': '昏暗凉爽的海滩场景，夜晚的海滩和星空',
                    'fresh': '昏暗清新的海滩场景，清晨的迷雾海滩',
                    'vibrant': '昏暗鲜艳的海滩场景，夜晚的海滩派对'
                },
                'harsh': {
                    'warm': '强光温暖的海滩场景，正午的强烈阳光',
                    'cool': '强光凉爽的海滩场景，强烈阳光反射的海水',
                    'fresh': '强光清新的海滩场景，强劲的海风和海浪',
                    'vibrant': '强光鲜艳的海滩场景，色彩鲜明的沙滩活动'
                }
            },
            'indoor': {
                'bright': {
                    'warm': '明亮温暖的室内场景，阳光充足的房间',
                    'cool': '明亮凉爽的室内场景，光线明亮的现代室内',
                    'fresh': '明亮清新的室内场景，通风良好的室内空间',
                    'vibrant': '明亮鲜艳的室内场景，色彩丰富的室内装饰'
                },
                'soft': {
                    'warm': '柔和温暖的室内场景，温暖灯光下的房间',
                    'cool': '柔和凉爽的室内场景，柔和灯光下的现代室内',
                    'fresh': '柔和清新的室内场景，柔和灯光下的简约室内',
                    'vibrant': '柔和鲜艳的室内场景，柔和灯光下的色彩装饰'
                },
                'dim': {
                    'warm': '昏暗温暖的室内场景，烛光或温暖小灯的房间',
                    'cool': '昏暗凉爽的室内场景，光线较暗的室内空间',
                    'fresh': '昏暗清新的室内场景，昏暗灯光下的简约室内',
                    'vibrant': '昏暗鲜艳的室内场景，昏暗灯光下的彩色装饰'
                },
                'harsh': {
                    'warm': '强光温暖的室内场景，强烈灯光照射的室内',
                    'cool': '强光凉爽的室内场景，强烈荧光灯照射的室内',
                    'fresh': '强光清新的室内场景，强烈灯光下的简约室内',
                    'vibrant': '强光鲜艳的室内场景，强烈灯光下的色彩装饰'
                }
            },
            'outdoor': {
                'bright': {
                    'warm': '明亮温暖的户外场景，阳光明媚的户外环境',
                    'cool': '明亮凉爽的户外场景，晴朗的户外环境',
                    'fresh': '明亮清新的户外场景，清新的户外空气',
                    'vibrant': '明亮鲜艳的户外场景，色彩丰富的户外景观'
                },
                'soft': {
                    'warm': '柔和温暖的户外场景，柔和阳光的户外环境',
                    'cool': '柔和凉爽的户外场景，阴天的户外环境',
                    'fresh': '柔和清新的户外场景，柔和气候的户外环境',
                    'vibrant': '柔和鲜艳的户外场景，柔和光线的彩色景观'
                },
                'dim': {
                    'warm': '昏暗温暖的户外场景，黄昏时分的户外环境',
                    'cool': '昏暗凉爽的户外场景，夜晚的户外环境',
                    'fresh': '昏暗清新的户外场景，夜晚的清新空气',
                    'vibrant': '昏暗鲜艳的户外场景，夜晚的彩色灯光'
                },
                'harsh': {
                    'warm': '强光温暖的户外场景，强烈阳光的户外环境',
                    'cool': '强光凉爽的户外场景，强烈光线的户外环境',
                    'fresh': '强光清新的户外场景，强风或强光线的户外',
                    'vibrant': '强光鲜艳的户外场景，强烈光线的彩色景观'
                }
            }
        }
        
        # 默认描述
        default_desc = f'这是一张{color_features["dominant_color"]}色调的{scene_type}场景照片，光线{light_type}'
        
        # 生成详细描述
        try:
            desc = descriptions.get(scene_type, {}).get(light_type, {}).get(color_features["dominant_color"], default_desc)
            return desc
        except:
            return default_desc
    
    def _analyze_scene_elements(self, scene_type):
        """
        分析场景元素
        :param scene_type: 场景类型
        :return: 场景元素列表
        """
        elements = {
            'nature': ['树木', '草地', '花朵', '山脉', '河流', '天空', '动物', '阳光'],
            'city': ['建筑', '街道', '车辆', '行人', '灯光', '天空', '道路', '桥梁'],
            'beach': ['沙滩', '海水', '天空', '阳光', '海浪', '贝壳', '遮阳伞', '船只'],
            'indoor': ['家具', '墙壁', '地板', '窗户', '灯光', '装饰品', '植物', '电器'],
            'outdoor': ['天空', '地面', '植被', '建筑', '车辆', '行人', '阳光', '阴影'],
            'mountain': ['山脉', '岩石', '树木', '天空', '阳光', '阴影', '草地', '溪流'],
            'forest': ['树木', '草地', '阳光', '阴影', '花朵', '溪流', '动物', '苔藓'],
            'urban': ['建筑', '街道', '车辆', '行人', '灯光', '广告牌', '道路', '桥梁']
        }
        
        return elements.get(scene_type, ['其他元素'])
    
    def _get_lighting_summary(self, light_type):
        """
        获取光线总结
        :param light_type: 光线类型
        :return: 光线总结字符串
        """
        summaries = {
            'bright': '光线明亮，适合拍摄清晰、活力的照片',
            'soft': '光线柔和，适合拍摄温馨、自然的照片',
            'dim': '光线较暗，适合拍摄氛围感、忧郁的照片',
            'harsh': '光线强烈，适合拍摄对比度高、有冲击力的照片'
        }
        return summaries.get(light_type, '光线条件一般')
    
    def _get_color_summary(self, color_features):
        """
        获取色彩总结
        :param color_features: 色彩特征
        :return: 色彩总结字符串
        """
        dominant_color = color_features['dominant_color']
        saturation = color_features['saturation_mean']
        brightness = color_features['brightness_mean']
        
        saturation_level = '高饱和度' if saturation > 128 else '低饱和度'
        brightness_level = '明亮' if brightness > 128 else '暗调'
        
        return f'主色调为{dominant_color}，{saturation_level}，{brightness_level}，适合营造特定氛围'
    
    def _get_composition_summary(self, content_features):
        """
        获取构图总结
        :param content_features: 内容特征
        :return: 构图总结字符串
        """
        complexity = content_features['complexity']
        edge_density = content_features['edge_density']
        
        return f'场景复杂度{complexity}，边缘密度{edge_density:.2f}，{("适合复杂构图" if complexity == "high" else "适合简洁构图")}'
    
    def _classify_scene(self, image):
        """
        简化的场景分类，实际可使用预训练模型
        :param image: 图片
        :return: 场景类型
        """
        # 这里使用简化的实现，根据图片的颜色和对比度来判断
        # 实际项目中应该使用预训练的CNN模型
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # 计算绿色通道的平均值（自然场景通常有较高的绿色值）
        green_mean = np.mean(image[:, :, 1])
        
        # 计算蓝色通道的平均值（天空/水域通常有较高的蓝色值）
        blue_mean = np.mean(image[:, :, 0])
        
        # 计算红色通道的平均值（城市建筑可能有较高的红色值）
        red_mean = np.mean(image[:, :, 2])
        
        # 简化的场景判断逻辑
        if green_mean > 120 and blue_mean > 100:
            return 'nature'
        elif blue_mean > 130:
            return 'beach' if green_mean > 80 else 'outdoor'
        elif red_mean > 100 and green_mean < 100:
            return 'city'
        else:
            return 'indoor'
    
    def _analyze_light(self, image):
        """
        分析图片的光线条件
        :param image: 图片
        :return: 光线类型
        """
        # 转换为灰度图
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # 计算平均亮度
        mean_brightness = np.mean(gray)
        
        # 计算对比度
        contrast = np.std(gray)
        
        if mean_brightness > 150:
            return 'bright' if contrast > 80 else 'soft'
        else:
            return 'dim' if contrast < 50 else 'harsh'
    
    def _analyze_color(self, image):
        """
        分析图片的色彩特征
        :param image: 图片
        :return: 色彩特征
        """
        # 转换为HSV颜色空间
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # 计算各通道的平均值
        h_mean = np.mean(hsv[:, :, 0])
        s_mean = np.mean(hsv[:, :, 1])
        v_mean = np.mean(hsv[:, :, 2])
        
        # 简单的色彩分类
        dominant_color = ""
        if h_mean < 30:
            dominant_color = "warm"  # 红色、橙色、黄色
        elif h_mean < 90:
            dominant_color = "fresh"  # 绿色
        elif h_mean < 150:
            dominant_color = "cool"  # 蓝色
        else:
            dominant_color = "vibrant"  # 紫色、粉色
        
        return {
            'dominant_color': dominant_color,
            'hue_mean': h_mean,
            'saturation_mean': s_mean,
            'brightness_mean': v_mean
        }
    
    def _analyze_content(self, image):
        """
        简化的内容分析
        :param image: 图片
        :return: 内容特征
        """
        # 这里使用简化的实现，实际可使用目标检测模型
        # 计算边缘密度（边缘多的场景可能更复杂）
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        edge_density = np.sum(edges > 0) / (image.shape[0] * image.shape[1])
        
        return {
            'complexity': 'high' if edge_density > 0.1 else 'low',
            'edge_density': edge_density
        }
    
    def generate_search_keywords(self, scene_features, style):
        """
        根据场景特征和风格生成搜索关键词
        :param scene_features: 场景特征
        :param style: 风格
        :return: 搜索关键词列表
        """
        keywords = []
        
        # 基于场景类型
        keywords.append(scene_features['scene_type'])
        
        # 基于光线
        keywords.append(scene_features['light_type'])
        
        # 基于主色调
        keywords.append(scene_features['colors']['dominant_color'])
        
        # 基于风格
        keywords.append(style)
        
        # 确保搜索结果包含人物
        keywords.append("person")
        keywords.append("people")
        
        # 添加更具体的姿势相关关键词
        keywords.append("human_pose")
        keywords.append("photography_pose")
        keywords.append("pose")
        
        # 添加场景特定的人物姿势关键词
        scene_type = scene_features['scene_type']
        scene_keywords = {
            'nature': ['outdoor_pose', 'nature_photography', 'person_in_nature'],
            'city': ['urban_pose', 'city_photography', 'person_in_city'],
            'beach': ['beach_pose', 'beach_photography', 'person_on_beach'],
            'indoor': ['indoor_pose', 'interior_photography', 'person_indoor'],
            'outdoor': ['outdoor_pose', 'outdoor_photography', 'person_outdoor'],
            'mountain': ['mountain_pose', 'hiking_pose', 'person_in_mountains'],
            'forest': ['forest_pose', 'nature_photography', 'person_in_forest'],
            'urban': ['urban_pose', 'city_photography', 'person_in_urban']
        }
        
        # 添加场景特定关键词
        if scene_type in scene_keywords:
            keywords.extend(scene_keywords[scene_type])
        
        # 添加风格特定的姿势关键词
        style_pose_keywords = {
            '生命力': ['dynamic_pose', 'energetic_pose', 'lively_pose'],
            '忧郁': ['melancholy_pose', 'introspective_pose', 'calm_pose'],
            '氛围感': ['atmospheric_pose', 'moody_pose', 'artistic_pose'],
            '清新': ['fresh_pose', 'natural_pose', 'light_pose'],
            '酷飒': ['cool_pose', 'edgy_pose', 'stylish_pose'],
            '甜美': ['sweet_pose', 'cute_pose', 'lovely_pose']
        }
        
        # 添加风格特定关键词
        if style in style_pose_keywords:
            keywords.extend(style_pose_keywords[style])
        
        return keywords
