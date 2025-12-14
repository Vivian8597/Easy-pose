import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 测试DashScope API配置
def test_dashscope_api():
    print('正在测试DashScope API配置...')
    
    # 打印配置信息（隐藏API密钥的一部分）
    api_key = os.environ.get("DASHSCOPE_API_KEY", "")
    api_url = os.environ.get("DASHSCOPE_API_URL", "")
    
    masked_api_key = f"{api_key[:4]}****{api_key[-4:]}" if api_key else "未配置"
    print(f"DashScope API URL: {api_url}")
    print(f"DashScope API Key: {masked_api_key}")
    
    # 检查配置是否完整
    if api_key and api_url:
        print('✓ DashScope API配置完整')
    else:
        print('✗ DashScope API配置不完整，请检查.env文件')
    
    print('\nDashScope API配置测试完成！')
    print('提示：要测试完整的图生图功能，需要运行完整的应用并上传图片。')

if __name__ == '__main__':
    test_dashscope_api()
