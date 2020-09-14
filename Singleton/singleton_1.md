# 单例模式_1

    所谓单例模式，就是说不管什么时候要确保只有一个对象实例的存在。在很多情况下，整个系统中只需要存在一个对象，
    所有的信息都从这个对象获取，比如系统的配置对象，或者是线程池。这些场景下，就非常适合使用单例模式。总结起来，
    就是说不管我们初始化一个对象多少次，真正干活的对象只会生成一次并且在首次生成。
    
    下面来看下实现单例模式的代码。
    
```python
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

```

    这段代码的运行结果：
    sing1.id: 1369888343616, sing1.display: 1369888622576
    sing2.id: 1369888622768, sing2.display: 1369888622576
    
    可以看出虽然创建了两个不同的实例，但是访问其属性的ID是相同的。
    
    在这个单例模式的实现中，我们借助了类变量_instance来存储创建的实例，我们在首次初始化singleton时，生成了_A类
    的实例，并将其存储到Singleton._instance中，在这之后的每次初始化，都从_instance中获取真实工作类的实例，这样
    就实现了单例模式。