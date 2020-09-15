# 观察者模式_1

    所谓观察者模式，就是说当一个对象发生变化时，观察者能及时得到通知并更新。观察者模式在很多地方都有应用，比如在购物时，关注商品等场景。
    
```python
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

```

    运行结果：
    User observer: two observers
    Store observer: two observers
    Store observer: single observer
    
    在上面的代码中，最重要的就是Commodity类了，它实现了观察者模式中大部分功能。作为一个被观察的对象，
    Commodity实现了注册观察者，注销观察者和通知观察者的功能。接着我们基于Commodity创建了我们的商品子类
    SubCommodity，并且当我们设置SubCommodity.message属性时，SubCommodity对象会通知到所有观察者。
    可以看出，观察者模式使被观察的对象（主题）和观察者之间解耦了。