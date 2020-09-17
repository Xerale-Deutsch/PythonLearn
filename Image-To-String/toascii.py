import argparse

from PIL import Image

# 构建命令行输入参数处理 ArgumentParser 的实例
parser = argparse.ArgumentParser()

# 定义输入文件、输出文件、输出字符画的宽和高
parser.add_argument('file')
parser.add_argument('-o', '--output')
parser.add_argument('--width', type=int, default=80)
parser.add_argument('--height', type=int, default=80)

# 解析并获取参数
args = parser.parse_args()

IMG = args.file
OUTPUT = args.output
WIDTH = args.width
HEIGHT = args.height

# 字符画所用的字符表
ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")


def get_char(r, g, b, alpha=256):
    """
    将256个灰度映射到list的字符上

    :param r:       int     红色
    :param g:       int     绿色
    :param b:       int     蓝色
    :param alpha:   int     透明度
    :return:        str     灰度值对应的字符
    """

    # 如果透明度为0，返回空字符
    if alpha == 0:
        return ' '

    # 获取字符数组的长度
    length = len(ascii_char)
    # 将 RGB 值转为灰度值 gray，灰度值范围为 0-255
    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)
    # 灰度值范围为 0-255，而字符集只有 70
    # 需要进行如下处理才能将灰度值映射到指定的字符上
    unit = (256.0 + 1) / length

    return ascii_char[int(gray / unit)]


if __name__ == '__main__':
    img = Image.open(IMG)
    img = img.resize((WIDTH, HEIGHT), Image.NEAREST)

    txt = ""
    for i in range(HEIGHT):
        for j in range(WIDTH):
            # 将 (j,i) 坐标的 RGB 像素转为字符后添加到 txt 字符串
            txt += get_char(*img.getpixel((j, i)))

        txt += '\n'

    # 输出到文件
    if OUTPUT:
        with open(OUTPUT, 'w') as f:
            f.write(txt)
    else:
        with open('output.txt', 'w') as f:
            f.write(txt)
