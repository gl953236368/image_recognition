from image_recognition.hamming_distance import hamming_distance
from PIL import Image


def padding_bg(fgfile):
    """
    给背景填充白色 然后再转灰度
    :param fgfile:
    :return:
    """
    new_file = "new_fg_pic.png"
    im = Image.open(fgfile)
    x, y = im.size
    p = Image.new('RGBA', im.size, (255, 255, 255))
    p.paste(im, (0, 0, x, y), im)
    p.save(new_file)
    return new_file


if __name__ == '__main__':
    bg_pic = "bg_pic.jpg"
    fg_pic = "fg_pic.jpg"
    """ 快手的滑块需要填充色，高度接口会给"""
    new_fg_pic = padding_bg(fg_pic)
    distance = hamming_distance(new_fg_pic, bg_pic, 147)
    print(distance)


