import cv2
import os

# 测试OpenCV是否能读取图片
def test_opencv_read():
    # 测试当前目录下的测试图片
    test_image_path = 'test_image.jpg'
    uploads_image_path = 'uploads/test_image.jpg'
    
    print(f'测试直接读取: {test_image_path}')
    img1 = cv2.imread(test_image_path)
    print(f'结果: {img1 is not None}')
    if img1 is not None:
        print(f'图片尺寸: {img1.shape}')
    
    print(f'\n测试读取uploads目录下的图片: {uploads_image_path}')
    img2 = cv2.imread(uploads_image_path)
    print(f'结果: {img2 is not None}')
    if img2 is not None:
        print(f'图片尺寸: {img2.shape}')
    
    # 测试绝对路径
    absolute_path = os.path.abspath(uploads_image_path)
    print(f'\n测试绝对路径: {absolute_path}')
    img3 = cv2.imread(absolute_path)
    print(f'结果: {img3 is not None}')
    if img3 is not None:
        print(f'图片尺寸: {img3.shape}')

if __name__ == '__main__':
    test_opencv_read()
