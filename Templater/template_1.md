# 模板模式_1

    提到模板，不难想到文档模板、简历模板等。其实模板方法模式中的模板就是这个意思，在模板方法模式中，我们先定义一个类模板，
    在这个类中，我们定义了各种操作的顺序（轮毂或者说是骨架），但是并不实现这些操作，这些操作由子类来操作。
    
    举个栗子：
    阿珍爱上了阿强，他们约定一起去游泳，那这具体都是个什么过程呢，第一步，要买泳装；第二步，去游泳池；第三步，找到他们订的
    地方。两个人的套路都是一样的，但是具体细节不同，阿珍喜欢X宝购物，阿强喜欢X东买货；阿珍喜欢开车去，阿强喜欢骑行；但是也
    有共同的地方，那就是都是一起找他们的预订位置，这就可以使用模板模式来搞一搞了。
    
```python
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

```

    运行结果：
    Zhen: buy a swimming suit from Xbao
    Zhen: to the swimming pool by driving her car
    Zhen: find the location where they booked
    start swimming
    Qiang: buy a swimming suit from XD
    Qiang: to the swimming pool by biking
    Qiang: find the location where they booked
    start swimming
    
    模板方法模式是结构最简单的行为型设计模式，在其结构中只存在父类与子类之间的继承关系。通过使用模板方法模式，可以将一些
    复杂流程的实现步骤封装在一系列基本方法中，在抽象父类中提供一个称之为模板方法的方法来定义这些基本方法的执行次序，而通
    过其子类来覆盖某些步骤，从而使得相同的算法框架可以有不同的执行结果。模板方法模式提供了一个模板方法来定义算法框架，而
    某些具体步骤的实现可以在其子类中完成。