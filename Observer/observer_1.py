# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import abc


class Commodity(object):
    """
    商品类，被观察对象的基类
    """

    def __init__(self):
        self._observers = []

    def addattention(self, observer):
        """
        注册一个观察者
        """
        if observer not in self._observers:
            self._observers.append(observer)

    def delattention(self, observer):
        """
        注销一个观察者
        """
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

    def notify(self):
        """
        通知所有观察者，执行观察者的更新方法
        """
        for observer in self._observers:
            observer.update(self)


class SubCommodity(Commodity):
    """
    商品子类，被观察的对象
    """

    def __init__(self):
        super(SubCommodity, self).__init__()
        self._message = None

    @property
    def message(self):
        """
        message 是一个属性
        """
        return self._message

    @message.setter
    def message(self, msg):
        """
        message 属性设置的装饰器
        """
        self._message = msg
        self.notify()


class Observer(metaclass=abc.ABCMeta):
    """
    观察者抽象类
    """

    @abc.abstractmethod
    def update(self, subject):
        pass


class UserObserver(Observer):
    """
    用户观察者
    """

    def update(self, subject):
        print("User observer: %s" % subject.message)


class StoreObserver(Observer):
    """
    店家观察者
    """

    def update(self, subject):
        print("Store observer: %s" % subject.message)


if __name__ == '__main__':
    # 初始化一个用户观察者
    user = UserObserver()
    # 初始化一个机构观察者
    store = StoreObserver()

    # 初始化一个商品子类
    subc = SubCommodity()
    # 注册观察者
    subc.addattention(user)
    subc.addattention(store)

    # 设置subc.message，这时观察者会收到通知
    subc.message = "two observers"

    # 注销一个观察者
    subc.delattention(user)
    subc.message = "single observer"