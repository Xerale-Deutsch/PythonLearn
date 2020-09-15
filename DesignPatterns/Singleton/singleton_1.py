#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Singleton(object):
    """
    单例模式
    """
    class _A(object):
        """
        真正工作的类
        """
        def __init__(self):
            pass

        def display(self) -> int:
            """
            返回当前实例的ID，全局唯一
            """
            return id(self)

    # 类变量，用于存储 _A 的实例
    _instance = None

    def __init__(self):
        """
        先判断类变量中是否已经保存了 _A 的实例，
        如果没有则创建一个后返回
        """
        if Singleton._instance is None:
            Singleton._instance = Singleton._A()

    def __getattr__(self, attr):
        """
        所有的属性都应从 _instance 获得
        """
        return getattr(self._instance, attr)


if __name__ == '__main__':
    # 创建实例
    sing1 = Singleton()
    sing2 = Singleton()
    print("sing1.id: {0}, sing1.display: {1}".format(id(sing1), sing1.display()))
    print("sing2.id: {0}, sing2.display: {1}".format(id(sing2), sing2.display()))

