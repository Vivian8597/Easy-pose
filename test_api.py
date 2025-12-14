import requests

# 测试风格列表API
def test_styles_api():
    url = 'http://127.0.0.1:5000/api/styles'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        print('✓ Styles API 测试成功')
        print(f'可用风格: {data.get("styles", [])}')
        return True
    except Exception as e:
        print(f'✗ Styles API 测试失败: {e}')
        return False

# 测试主页
def test_home_page():
    url = 'http://127.0.0.1:5000/'
    try:
        response = requests.get(url)
        response.raise_for_status()
        print('✓ 主页测试成功')
        return True
    except Exception as e:
        print(f'✗ 主页测试失败: {e}')
        return False

if __name__ == '__main__':
    print('开始测试拍照姿势推荐应用 API...\n')
    test_styles_api()
    print()
    test_home_page()
    print('\n测试完成！')
