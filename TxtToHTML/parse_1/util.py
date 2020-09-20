def lines(file):
    """
    处理文本
    在文本后加一空行
    """

    for line in file:
        yield line
    yield "\n"


def blocks(file):
    """
    将文本内容，生成一个个单独的文本块
    按空行分割
    """

    block = []
    for line in lines(file):
        if line.strip():
            block.append(line)
        elif block:
            yield "".join(block).strip()
            block = []

