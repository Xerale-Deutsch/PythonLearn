# 工厂模式_2

    在之前的简单工厂模式中，遇到了一个让人很不爽的问题：如果需要增加一种work，需要修改工厂代码。
    这像极了刚刚写好一段代码，项目经理那边又提了新的需求，劳资还要改改改。。。难道就没有省事的方法吗？
    方法肯定是有，仔细想想，如果对工厂进行抽象化，让每个工厂只负责一种产品的生产，那这样当增加一种产品时，
    就不需要修改已有的工厂了，只需要新增加一个工厂就行了，这样就避免修改整个工厂。而实现的方法就是用抽象类。
    
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
import abc


class BasicClass(object):
    """
    基础类
    """
    def get_work(self):
        return "basic_class: work!"

    def __str__(self):
        return "BasicClass"


class ProjectClass(object):
    """
    项目类
    """
    def get_work(self):
        return "project_class: work!"

    def __str__(self):
        return "ProjectClass"


class Factory(metaclass=abc.ABCMeta):
    """
    抽象工厂类
    """

    @abc.abstractmethod
    def create_work(self):
        """
        抽象方法，供其他调用的类来重写
        """
        pass


class BasicWorkFactory(Factory):
    """
    基础工厂类
    """
    def create_work(self):
        return BasicClass()


class ProjectWorkFactory(Factory):
    """
    项目工厂类
    """
    def create_work(self):
        return ProjectClass()


def get_factory():
    """
    随机获取一个工厂类
    """
    return random.choice([BasicWorkFactory, ProjectWorkFactory])()


if __name__ == '__main__':
    factory = get_factory()
    work = factory.create_work()
    print(work.get_work())


```

    运行结果：
    basic_class: work!
    或
    project_class: work!
    随机选一个实例化。
    
    在上面代码中，我们增加了一个Factory类，这个类继承自ABC类，其中我们定义了抽象方法create_work用于创建work，这样
    只需要添加继承自Factory的子类，然后重写create_work这个方法即可，就不需要修改已经存在的基础工厂和项目工厂了。
    
    但是，这好像有点问题，当有这么个场景的时候，比如说我有一大堆要需要去创建的工厂类，这重复的工程量还是很巨大，
    这样的代码，又不香了，一点看不出来有啥cool的地方了。。。