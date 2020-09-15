# 单例模式_2

    用装饰器来实现单例模式
    
    
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Singleton(object):
    """
    单例类装饰器，可以用于想实现单例的任何类。
    Warning： 不能用于多线程环境使用。
    """
    def __init__(self, cls):
        """
        这里传入的是一个类
        """
        self._cls = cls

    def instance(self):
        """
        返回真正的实例
        """
        try:
            return self._instance
        except AttributeError:
            self._instance = self._cls()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._decorated)


# 装饰器
@Singleton
class A(object):
    """
    一个需要单例模式的类
    """
    def __init__(self):
        pass

    def display(self):
        return id(self)


if __name__ == '__main__':
    s1 = A.instance()
    s2 = A.instance()
    print(s1, s1.display())
    print(s2, s2.display())
    print(s1 is s2)

```

    代码运行结果：
    
    <__main__.A object at 0x0000018CB93887C0> 1703914538944
    <__main__.A object at 0x0000018CB93887C0> 1703914538944
    True
    
    任何想使用单例模式的类，只需要使用 Singleton 装饰器装饰一下就可以使用了。可以看到其核心工作原理其实和第一种实现方式是
    一致的，也是使用内置的属性 Singleton._instance 来存储实例的。通过使用装饰器的模式我们将代码解耦了，使用更加灵活。
    
    在这段代码中，其实也用到了装饰者模式。
    