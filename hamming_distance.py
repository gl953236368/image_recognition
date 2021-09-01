from PIL import Image
import os
from functools import reduce
import glob
import re

def hamming_distance(fg_pic, bg_pic, disY):
    """
    汉明距离 确定相似图片 从而确定 mouseX 移动坐标
    :param fg_pic: 滑块图片
    :param bg_pic: 缺口背景图片
    :param disY: 高度
    :return:
    """

    def crop_image(h, bgImage, savePath, offset):
        """
        滑块图片进行切割
        eg. 1.xhs的滑块图片 高度（除了图片之外为全白）和背景图一致 需要截取
            2.ks的滑块 只有滑块图片，但接口中返回高度
        :param fgImageGray:
        :param bgImage:
        :param savePath:
        :return:
        """
        if not os.path.exists(savePath):
            os.makedirs(savePath)
        x,y = bgImage.size
        for i in range(offset, x - offset , 4):  #  每次偏移4个像素点
            z = bgImage.crop((i, h, i + offset, h + offset))
            z.save(f'{savePath}/{i}.png')


    def calc_hash(im):
        """
        图片压缩 转成 hash
        :param im:
        :return:
        """
        if not isinstance(im, Image.Image):
            im = Image.open(im)
        # 缩放为 8x8位 高质量灰度图
        im = im.resize((8, 8), Image.ANTIALIAS).convert('L')

        # 求所有点位和 的平均值
        avg = reduce(lambda x, y: x + y, im.getdata()) / 64

        rs = []
        # 小于平均值则为 0  转换为 0，1数组
        for index, v in enumerate(map(lambda i: 0 if i < avg else 1, im.getdata())):
            rs.append(str(v))
        return ''.join(rs)

    def compare_hash(h1, h2):
        """
        切割图片和滑块hash对比的值
        :param h1:
        :param h2:
        :return:
        """
        h = 0
        for i in range(len(h1)):
            if h1[i] == h2[i]:
                h += 1
        return h


    def calc_distance(fgfile, bgfile, disY, savePath='images'):
        """
        汉明距离计算
        :param fgfile: 滑块
        :param bgfile: 背景图片
        :param disY: 缺口位置在背景图片中的高度
        :param savePath:
        :return:
        """
        # gray1 = padding_bg(fgfile)
        gray1 = Image.open(fgfile).convert('L')
        x, y = gray1.size  # 碎片的长宽
        gray2 = Image.open(bgfile).convert('L')

        crop_image(disY, gray2, savePath, x)  # 切割图片
        t1 = calc_hash(gray1)
        filenames = glob.glob(f'{savePath}/*.png')
        rs = []

        for filename in filenames:
            rs.append((compare_hash(t1, calc_hash(filename)), filename))
            # os.remove(filename)

        # 从大到小排序
        t = sorted(rs, key=lambda x: x[0], reverse=True)
        n = re.search(r'(\d+)\.png', t[0][1]).group(1)

        distance = int(n)
        print(f"距离(未压缩)：{distance}")

        return distance

    return calc_distance(fg_pic, bg_pic, disY)