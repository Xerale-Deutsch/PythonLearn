# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import abc


class Swimming(metaclass=abc.ABCMeta):
    """
    游泳模板基类
    """

    def finished(self):
        """
        游泳方法中，确定了要执行哪些操作才能完美的游泳
        """
        self.prepare()
        self.go_to_swimming_pool()
        self.find_location()
        print("start swimming")

    @abc.abstractmethod
    def prepare(self):
        pass

    @abc.abstractmethod
    def go_to_swimming_pool(self):
        pass

    @abc.abstractmethod
    def find_location(self):
        pass


class ZhenSwimming(Swimming):
    """
    阿珍想去游泳，必须实现规定的三个步骤
    """

    def prepare(self):
        """
        先准备一套泳衣，从X宝购买
        """
        print("Zhen: buy a swimming suit from Xbao")

    def go_to_swimming_pool(self):
        """
        开车去游泳池
        """
        print("Zhen: to the swimming pool by driving her car")

    def find_location(self):
        """
        寻找预定的地点
        """
        print("Zhen: find the location where they booked")


class QiangSwimming(Swimming):
    """
    阿强想去游泳，也必须实现三个步骤
    """

    def prepare(self):
        """
        买一套泳装，从X东买吧
        """
        print("Qiang: buy a swimming suit from XD")

    def go_to_swimming_pool(self):
        """
        骑自行车去游泳池
        """
        print("Qiang: to the swimming pool by biking")

    def find_location(self):
        """
        寻找预订好的地方
        """
        print("Qiang: find the location where they booked")


if __name__ == '__main__':
    # 阿珍去游泳
    f = ZhenSwimming()
    f.finished()

    # 阿强去游泳
    f = QiangSwimming()
    f.finished()