from image_recognition.hamming_distance import hamming_distance
from PIL import Image
import numpy as np

def get_fg_image(fgImageGray):
    """
    确定 滑块图片在 背景图片中的高度
    :param fgImageGray:  背景图片
    :return:
    """
    tmp_image = np.asarray(fgImageGray)  # 300x90 高x宽
    h = 0  # 最后确定的高度
    for i in range(200):  # 取图像碎片的大概位置
        if tmp_image[i, 30] and tmp_image[i, 35] and tmp_image[i, 25]:
            h = i
            break

    return h

if __name__ == '__main__':
    """ 数美滑块 滑块图片和背景图片等高 需要先切割 确定高度"""
    fg_file = "fg_pic.jpg"
    bg_pic = "bg_pic.jpg"
    gray1 = Image.open(fg_file).convert('L')
    h = get_fg_image(gray1)
    image = gray1.crop((0, h, 90, h + 90))
    image.save(f"new_{fg_file}")
    distance = hamming_distance(f"new_{fg_file}", bg_pic, h)
