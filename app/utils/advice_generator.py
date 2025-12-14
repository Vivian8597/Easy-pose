class AdviceGenerator:
    def __init__(self):
        # 初始化建议模板
        self.advice_templates = {
            'angle': {
                'general': [
                    '尝试从{}角度拍摄，这样可以更好地展现人物与场景的关系',
                    '考虑使用{}角度，能增加照片的视觉冲击力',
                    '{}角度适合展现场景的层次感，同时突出人物',
                    '使用{}角度拍摄，会让人物看起来更有气势',
                    '{}角度能营造出更亲密、更有感染力的氛围'
                ],
                'options': ['低', '高', '平', '俯视', '仰视', '侧面', '对角线']
            },
            'position': {
                'general': [
                    '将人物放在画面的{}位置，符合黄金分割构图原则',
                    '尝试将人物置于{}，这样能平衡整个画面',
                    '考虑人物与背景的关系，将人物放在{}会更和谐',
                    '使用{}构图，让人物成为画面的视觉中心',
                    '将人物放在{}，能更好地利用场景元素'
                ],
                'options': ['黄金分割点', '画面中心', '左侧三分之一处', '右侧三分之一处', '前景', '背景', '边缘']
            },
            'lighting': {
                'general': [
                    '利用{}光线，能突出人物的轮廓和立体感',
                    '考虑使用{}光，营造出柔和、自然的效果',
                    '{}光能增加照片的戏剧性和氛围感',
                    '避免{}光，它会在人物脸上产生生硬的阴影',
                    '尝试{}光，能让人物的肤色看起来更健康'
                ],
                'options': ['顺', '逆', '侧', '顶', '柔和的', '温暖的', '散射的']
            },
            'pose': {
                'general': [
                    '建议人物采用{}姿势，与整体风格更协调',
                    '尝试{}的姿势，能展现出更自然的状态',
                    '考虑{}的动作，增加照片的动感和活力',
                    '使用{}的姿势，能突出人物的特点',
                    '建议{}，这样能与场景更好地融合'
                ],
                'options': ['自然站立', '坐姿', '动态跳跃', '侧身回眸', '手臂舒展', '轻微倾斜身体', '双手自然摆动']
            },
            'hand_movements': {
                'general': [
                    '建议手部做出{}动作，能增加画面的生动性',
                    '尝试{}的手势，与整体风格更协调',
                    '考虑{}，让手部自然融入场景',
                    '使用{}手势，能突出人物的情绪',
                    '建议手部{}，这样能平衡整个画面'
                ],
                'options': ['自然下垂', '轻触头发', '放在口袋里', '比心', '指向远方', '托腮', '张开双臂', '轻扶场景中的物体']
            },
            'foot_movements': {
                'general': [
                    '建议脚部采用{}姿势，能保持身体的平衡感',
                    '尝试{}，增加画面的动感',
                    '考虑{}，与整体风格更协调',
                    '使用{}站姿，能展现出更自然的状态',
                    '建议脚部{}，这样能更好地融入场景'
                ],
                'options': ['自然分开', '前后交错', '踮起脚尖', '一只脚微微抬起', '双脚并拢', '侧身站立', '单腿弯曲']
            },
            'expression': {
                'general': [
                    '建议面部做出{}表情，与整体风格更协调',
                    '尝试{}，能展现出更自然的状态',
                    '考虑{}表情，突出人物的情绪',
                    '使用{}的表情，能增加照片的感染力',
                    '建议{}，这样能更好地传达主题'
                ],
                'options': ['自然微笑', '侧头微笑', '面无表情', '沉思', '大笑', '凝视远方', '闭眼享受']
            },
            'composition': {
                'general': [
                    '采用{}构图法，能增强画面的层次感',
                    '使用{}来引导观众的视线到人物身上',
                    '考虑画面的{}，保持视觉平衡',
                    '尝试{}，让照片更有故事性',
                    '利用场景中的{}作为框架，突出人物'
                ],
                'options': ['三分法', '引导线', '对称性', '前景元素', '框架', '留白', '对角线']
            }
        }
        
        # 风格特定建议
        self.style_specific_advice = {
            '生命力': {
                'angle': ['低', '侧', '对角线'],
                'position': ['左侧三分之一处', '右侧三分之一处', '前景'],
                'lighting': ['顺', '温暖的', '散射的'],
                'pose': ['动态跳跃', '手臂舒展', '轻微倾斜身体'],
                'hand_movements': ['张开双臂', '指向远方', '轻触头发', '比心'],
                'foot_movements': ['踮起脚尖', '一只脚微微抬起', '前后交错', '单腿弯曲'],
                'expression': ['大笑', '自然微笑', '凝视远方', '侧头微笑'],
                'composition': ['三分法', '引导线', '留白']
            },
            '忧郁': {
                'angle': ['高', '平', '侧面'],
                'position': ['画面中心', '边缘', '背景'],
                'lighting': ['侧', '柔和的', '散射的'],
                'pose': ['自然站立', '侧身回眸', '双手自然摆动'],
                'hand_movements': ['自然下垂', '放在口袋里', '托腮', '轻扶场景中的物体'],
                'foot_movements': ['双脚并拢', '侧身站立', '自然分开', '一只脚微微抬起'],
                'expression': ['面无表情', '沉思', '闭眼享受', '侧头微笑'],
                'composition': ['对称性', '框架', '留白']
            },
            '氛围感': {
                'angle': ['低', '高', '俯视', '仰视'],
                'position': ['黄金分割点', '前景', '背景'],
                'lighting': ['逆', '侧', '温暖的'],
                'pose': ['自然站立', '坐姿', '轻微倾斜身体'],
                'hand_movements': ['轻触头发', '轻扶场景中的物体', '托腮', '自然下垂'],
                'foot_movements': ['自然分开', '前后交错', '侧身站立', '单腿弯曲'],
                'expression': ['凝视远方', '沉思', '自然微笑', '闭眼享受'],
                'composition': ['三分法', '引导线', '框架']
            },
            '清新': {
                'angle': ['平', '侧', '对角线'],
                'position': ['左侧三分之一处', '右侧三分之一处', '前景'],
                'lighting': ['顺', '柔和的', '散射的'],
                'pose': ['自然站立', '手臂舒展', '双手自然摆动'],
                'hand_movements': ['轻触头发', '比心', '张开双臂', '自然下垂'],
                'foot_movements': ['自然分开', '踮起脚尖', '一只脚微微抬起', '前后交错'],
                'expression': ['自然微笑', '侧头微笑', '大笑', '凝视远方'],
                'composition': ['三分法', '留白', '对称性']
            },
            '酷飒': {
                'angle': ['低', '侧', '对角线'],
                'position': ['左侧三分之一处', '右侧三分之一处', '画面中心'],
                'lighting': ['侧', '顶', '逆'],
                'pose': ['自然站立', '轻微倾斜身体', '双手自然摆动'],
                'hand_movements': ['放在口袋里', '指向远方', '自然下垂', '轻扶场景中的物体'],
                'foot_movements': ['侧身站立', '前后交错', '自然分开', '单腿弯曲'],
                'expression': ['面无表情', '侧头微笑', '凝视远方', '沉思'],
                'composition': ['三分法', '对角线', '框架']
            },
            '甜美': {
                'angle': ['高', '平', '侧'],
                'position': ['黄金分割点', '画面中心', '前景'],
                'lighting': ['顺', '柔和的', '温暖的'],
                'pose': ['坐姿', '手臂舒展', '双手自然摆动'],
                'hand_movements': ['比心', '轻触头发', '托腮', '张开双臂'],
                'foot_movements': ['踮起脚尖', '双脚并拢', '一只脚微微抬起', '前后交错'],
                'expression': ['自然微笑', '侧头微笑', '大笑', '闭眼享受'],
                'composition': ['对称性', '留白', '框架']
            }
        }
    
    def generate_advice(self, scene_features, style):
        """
        根据场景特征和风格生成拍摄建议
        :param scene_features: 场景特征
        :param style: 风格
        :return: 拍摄建议字典
        """
        import random
        
        # 基础建议（包含新添加的建议类型）
        advice = {
            'angle': '',
            'position': '',
            'lighting': '',
            'pose': '',
            'hand_movements': '',
            'foot_movements': '',
            'expression': '',
            'composition': '',
            'general_tips': ''
        }
        
        # 获取风格特定的选项
        style_options = self.style_specific_advice.get(style, {})
        
        # 生成各方面建议
        for category in advice.keys():
            if category == 'general_tips':
                continue
                
            # 选择风格特定的选项或通用选项
            options = style_options.get(category, self.advice_templates[category]['options'])
            selected_option = random.choice(options)
            
            # 选择一个模板并填充选项
            template = random.choice(self.advice_templates[category]['general'])
            advice[category] = template.format(selected_option)
        
        # 生成通用建议
        advice['general_tips'] = self._generate_general_tips(scene_features, style)
        
        return advice
    
    def _generate_general_tips(self, scene_features, style):
        """
        生成通用拍摄建议
        :param scene_features: 场景特征
        :param style: 风格
        :return: 通用建议列表
        """
        tips = []
        
        # 基于场景类型的建议
        scene_type = scene_features['scene_type']
        if scene_type == 'nature':
            tips.append('利用自然环境作为背景，让人物与自然融为一体')
            tips.append('注意环境中的线条和形状，将人物置于合适的位置')
        elif scene_type == 'city':
            tips.append('利用城市建筑的线条和几何形状增强构图')
            tips.append('考虑人与城市环境的对比，突出主题')
        elif scene_type == 'beach':
            tips.append('利用沙滩和海水的自然线条作为引导线')
            tips.append('注意避免强烈的阳光直射，选择合适的拍摄时间')
        elif scene_type == 'indoor':
            tips.append('利用室内的灯光营造氛围')
            tips.append('注意背景的整洁，避免杂乱的元素')
        
        # 基于光线类型的建议
        light_type = scene_features['light_type']
        if light_type == 'bright':
            tips.append('在明亮的光线下，注意人物的表情和姿态，避免过度曝光')
        elif light_type == 'dim':
            tips.append('在昏暗的光线下，尝试使用剪影效果，增加神秘感')
        elif light_type == 'harsh':
            tips.append('强烈的光线下，考虑使用反光板或寻找阴影区域')
        
        # 基于风格的建议
        if style == '生命力':
            tips.append('鼓励人物做出自然、充满活力的动作，捕捉瞬间的动感')
        elif style == '忧郁':
            tips.append('注意人物的表情和眼神，传达出内心的情感')
        elif style == '氛围感':
            tips.append('关注整体画面的意境，利用光影创造氛围')
        elif style == '清新':
            tips.append('保持画面的简洁和纯净，避免过多的装饰元素')
        elif style == '酷飒':
            tips.append('强调人物的个性和态度，尝试不同的构图角度')
        elif style == '甜美':
            tips.append('捕捉人物自然、可爱的表情，营造温馨的氛围')
        
        # 随机选择3-5条建议
        import random
        return random.sample(tips, min(5, len(tips)))
