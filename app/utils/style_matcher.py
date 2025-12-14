class StyleMatcher:
    def __init__(self):
        # 初始化风格数据库
        self.styles = {
            '生命力': {
                'description': '活泼、动感、充满活力的风格',
                'pose_characteristics': ['dynamic', 'energetic', 'upright', 'open'],
                'composition': ['diagonal', 'asymmetrical', 'active'],
                'lighting': ['bright', 'natural', 'even'],
                'keywords': ['vibrant', 'active', 'dynamic', 'lively', 'energetic']
            },
            '忧郁': {
                'description': '柔和、低对比度、深色调的风格',
                'pose_characteristics': ['subtle', 'closed', 'relaxed', 'introverted'],
                'composition': ['symmetrical', 'centered', 'static'],
                'lighting': ['soft', 'dim', 'diffused'],
                'keywords': ['melancholy', 'soft', 'gentle', 'introspective', 'calm']
            },
            '氛围感': {
                'description': '意境、构图、光影丰富的风格',
                'pose_characteristics': ['balanced', 'expressive', 'contextual', 'harmonious'],
                'composition': ['rule_of_thirds', 'leading_lines', 'depth'],
                'lighting': ['atmospheric', 'directional', 'dramatic'],
                'keywords': ['atmospheric', 'moody', 'expressive', 'artistic', 'cinematic']
            },
            '清新': {
                'description': '明亮、自然、简约的风格',
                'pose_characteristics': ['light', 'natural', 'relaxed', 'open'],
                'composition': ['simple', 'clean', 'airy'],
                'lighting': ['soft', 'natural', 'even'],
                'keywords': ['fresh', 'clean', 'natural', 'light', 'simple']
            },
            '酷飒': {
                'description': '时尚、前卫、有态度的风格',
                'pose_characteristics': ['confident', 'sharp', 'defined', 'strong'],
                'composition': ['geometric', 'bold', 'stylized'],
                'lighting': ['contrast', 'harsh', 'directional'],
                'keywords': ['cool', 'edgy', 'stylish', 'confident', 'bold']
            },
            '甜美': {
                'description': '柔和、温馨、可爱的风格',
                'pose_characteristics': ['playful', 'cute', 'friendly', 'soft'],
                'composition': ['symmetrical', 'balanced', 'charming'],
                'lighting': ['warm', 'soft', 'diffused'],
                'keywords': ['sweet', 'cute', 'lovely', 'warm', 'charming']
            }
        }
    
    def get_available_styles(self):
        """
        获取所有可用的风格列表
        :return: 风格列表
        """
        return list(self.styles.keys())
    
    def match_style(self, style_name):
        """
        根据风格名称匹配风格特征
        :param style_name: 风格名称
        :return: 风格特征字典
        """
        if style_name not in self.styles:
            raise ValueError(f"Unknown style: {style_name}")
        
        return self.styles[style_name]
    
    def get_style_keywords(self, style_name):
        """
        获取风格相关的关键词
        :param style_name: 风格名称
        :return: 关键词列表
        """
        style = self.match_style(style_name)
        return style['keywords']
    
    def get_pose_characteristics(self, style_name):
        """
        获取特定风格对应的姿势特征
        :param style_name: 风格名称
        :return: 姿势特征列表
        """
        style = self.match_style(style_name)
        return style['pose_characteristics']
    
    def get_composition_tips(self, style_name):
        """
        获取特定风格对应的构图建议
        :param style_name: 风格名称
        :return: 构图建议列表
        """
        style = self.match_style(style_name)
        return style['composition']
    
    def get_lighting_tips(self, style_name):
        """
        获取特定风格对应的光线建议
        :param style_name: 风格名称
        :return: 光线建议列表
        """
        style = self.match_style(style_name)
        return style['lighting']
