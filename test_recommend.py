import requests
import os

# 测试图片路径（使用项目中现有的图片或创建一个简单的测试图片）
TEST_IMAGE_PATH = 'test_image.jpg'

# 创建一个简单的测试图片（白色背景）
def create_test_image():
    from PIL import Image
    img = Image.new('RGB', (600, 400), color='white')
    img.save(TEST_IMAGE_PATH)
    print(f'已创建测试图片: {TEST_IMAGE_PATH}')

# 测试推荐API
def test_recommend_api():
    url = 'http://127.0.0.1:5000/api/recommend'
    
    # 确保测试图片存在
    if not os.path.exists(TEST_IMAGE_PATH):
        create_test_image()
    
    # 打开测试图片
    with open(TEST_IMAGE_PATH, 'rb') as f:
        files = {'image': (TEST_IMAGE_PATH, f, 'image/jpeg')}
        data = {'style': '生命力'}
        
        try:
            print('正在测试推荐API...')
            response = requests.post(url, files=files, data=data)
            print(f'响应状态码: {response.status_code}')
            print(f'响应内容: {response.text}')
            
            if response.status_code == 200:
                data = response.json()
                print('✓ 推荐API测试成功')
                return True
            else:
                print('✗ 推荐API测试失败')
                return False
        except Exception as e:
            print(f'✗ 推荐API测试发生异常: {e}')
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    test_recommend_api()
