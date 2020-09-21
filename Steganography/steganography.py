from PIL import Image


def make_even_image(image):
    """
    使用最低有效位(Least Significant Bit, lsb)来隐写信息
    原理：肉眼几乎无法分辨最低位的色差，那用这方式，最低位就可以用来传递信息了

    将像素所有值最后一位bit数字改为偶数 0
    image.getdata() 返回的是一个可迭代对象，其中包含图片中所有
    像素点的数据每个像素点表示一个颜色，每种颜色有红绿蓝三种颜
    色按比例构成R Red 红色；G Green 绿色；B Blue 蓝色；A Alpha 透明度
    基数减一变偶数，偶数不变，位运算 >> 和 << 即可实现需求
    """

    pixel_list = [(r >> 1 << 1, g >> 1 << 1, b >> 1 << 1, a >> 1 << 1) for r, g, b, a in image.getdata()]
    even_image = Image.new(image.mode, image.size)
    even_image.putdata(pixel_list)

    return even_image


def encode_data_to_image(image, data):
    """
    将字节串编码到图片中
    1.将字符串解为二进制字符串，将每个字符转换成二进制，
      对应一个或多个字节码
    2.每个字节码为一个十进制的数，将这个十进制的数转为
      八位二进制数
    3.每个像素的RGBA都清空了一位，分别可以存储一个二进
      制数据，所以最大能存数据长度为像素数量的四倍，如果
      字符串长度超出，抛出异常
    """

    even_image = make_even_image(image)

    binary = ''.join(map(lambda i: str(bin(i)[2:].zfill(8)), bytearray(data, 'utf-8')))

    max_len = len(even_image.getdata()) * 4
    if len(binary) > max_len:
        raise Exception("不能将超过{0}bit的数据写入到这个图片中".format(max_len))

    encode_pixels = [(r + int(binary[index * 4 + 0]),
                      g + int(binary[index * 4 + 1]),
                      b + int(binary[index * 4 + 2]),
                      a + int(binary[index * 4 + 3]))
                     if index * 4 < len(binary) else (r, g, b, a)
                     for index, (r, g, b, a) in enumerate(even_image.getdata())]

    encode_image = Image.new(even_image.mode, even_image.size)
    encode_image.putdata(encode_pixels)

    return encode_image


def decode_data_from_image(image):
    """
    从图片中解出隐写的信息
    1. 将全部的像素的rgba最后一位数据读出
    2. 确定数据结束位置
    3. 将字节串解析为字符串
    """

    binary = ''.join([bin(r)[-1] + bin(g)[-1] + bin(b)[-1] + bin(a)[-1] for r, g, b, a in image.getdata()])

    # 因为有可能出现8个连续0的情况，故查找16个连续0的情况
    many_zero_index = binary.find('0' * 16)
    # 末尾可能为0，判断是否是8的倍数，然后确定末尾数字有多少0，来确定正确的结束为止
    end_index = many_zero_index + 8 - many_zero_index % 8 if many_zero_index % 8 != 0 else many_zero_index

    binary_data = binary[:end_index]
    data = []
    for i in range(len(binary_data) // 8):
        code = binary_data[i * 8:(i + 1) * 8]
        data.append(int(code, 2))

    data = bytes(data).decode()

    return data


if __name__ == '__main__':
    data = "https://www.baidu.com"
    img = Image.open("./ima.jpg").convert("RGBA")

    encode_image = encode_data_to_image(img, data)
    encode_image.save("./enc.png")
    content = decode_data_from_image(encode_image)
    print(content)
