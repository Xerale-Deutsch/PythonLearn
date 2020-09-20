import re
import sys

from parse_1.handlers import HTMLRender
from parse_1.rules import rule_list
from parse_1.util import blocks


class Parser(object):
    """
    解析器父类
    """

    def __init__(self, handler):
        self.handler = handler
        self.rules = []
        self.filters = []

    def add_rule(self, rule):
        """
        向解析器中添加规则类的实例
        """

        self.rules.append(rule)

    def add_filter(self, pattern, name):
        """
        添加过滤函数
        """

        def filter(block, handler):
            return re.sub(pattern, handler.sub(name), block)

        self.filters.append(filter)

    def parse(self, file):
        """
        核心方法
        解析文本文件，
        打印符合要求的标签，
        写入新的文件中
        """

        self.handler.start('document')

        for block in blocks(file):
            for filter in self.filters:
                block = filter(block, self.handler)

            for rule in self.rules:
                if rule.condition(block):
                    last = rule.action(block, self.handler)

                    if last:
                        break

        self.handler.end('document')


class BasicTextParser(Parser):
    """
    纯文本解析器
    """

    def __init__(self, handler):
        super().__init__(handler)
        for rule in rule_list:
            self.add_rule(rule)

        self.add_filter(r'\*(.+?)\*', 'emphasis')
        self.add_filter(r'(http://[\.a-zA-Z/]+)', 'url')
        self.add_filter(r'([\.a-zA-Z]+@[\.a-zA-Z]+[a-zA-Z]+)', 'mail')


def main():
    """
    主函数，控制程序运行
    """

    handler = HTMLRender()
    parser = BasicTextParser(handler)
    parser.parse(sys.stdin)


if __name__ == '__main__':
    main()
