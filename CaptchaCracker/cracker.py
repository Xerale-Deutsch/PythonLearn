import math
import os

from PIL import Image


class VectorCompare(object):
    """
    AI向量空间识别
    """

    def magnitude(self, concordance):
        """
        计算矢量的大小
        """

        total = 0
        for word, con in concordance.items():
            total += con ** 2

        return math.sqrt(total)

    def relation(self, concordance1, concordance2):
        """
        计算矢量之间的 cos 值
        """

        relevance = 0
        topvalue = 0
        for word, con in concordance1.items():
            if word in concordance2:
                topvalue += con * concordance2[word]

        return topvalue / (self.magnitude(concordance1) * self.magnitude(concordance2))


def build_vector(image):
    d1 = {}
    count = 0
    for i in image.getdata():
        d1[count] = i
        count += 1

    return d1


def captcha_cracker(img_name):
    """
    破解验证码

    """
    captcha_code = ""
    vector = VectorCompare()
    iconset = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
               'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    imageset = []

    for letter in iconset:
        for img in os.listdir('./iconset/{0}/'.format(letter)):
            temp = []
            temp.append(build_vector(Image.open("./iconset/{0}/{1}".format(letter, img))))
            imageset.append({letter: temp})

    img = Image.open(img_name)
    img.convert('P')
    img2 = Image.new("P", img.size, 255)

    # 遍历全部像素点，取出所要的红色和灰色，红色是220，灰色是227
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            pix = img.getpixel((x, y))
            if pix == 220 or pix == 227:
                img2.putpixel((x, y), 0)

    in_letter = False
    found_letter = False
    start = 0
    end = 0

    letters = []

    # 遍历新图像的像素点。此图像是进行了二值化处理的验证码，白色区域为背景，这里获取到字符的左右宽度
    for x in range(img2.size[0]):
        for y in range(img2.size[1]):
            pix = img2.getpixel((x, y))
            if pix != 255:
                in_letter = True

        if found_letter is False and in_letter is True:
            found_letter = True
            start = x

        if found_letter is True and in_letter is False:
            found_letter = False
            end = x
            letters.append((start, end))

        in_letter = False

    count = 0
    # crop 方法是获取一个区域，tuple里的参数分别对应左、上、右、下
    for letter in letters:
        img3 = img2.crop((letter[0], 0, letter[1], img2.size[1]))
        guess = []
        for image in imageset:
            for x, y in image.items():
                if len(y) != 0:
                    guess.append((vector.relation(y[0], build_vector(img3)), x))

        guess.sort(reverse=True)
        captcha_code += guess[0][1]

        count += 1

    return captcha_code


if __name__ == '__main__':
    # 单一样例测试
    file_name = './captcha.gif'
    code = captcha_cracker(file_name)
    print(code)

    # 大量样例测试
    # file_name_list = os.listdir("./examples")
    # for file_name in file_name_list:
    #     file_name = "./examples/{0}".format(file_name)
    #     code = captcha_cracker(file_name)
    #     print("{0}: {1}".format(file_name, code))

