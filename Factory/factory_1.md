# 工厂模式_1

    所谓工厂模式，也就是说我们可以通过工厂类创建产品。
    结合代码来理解什么是工厂模式。
    
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random


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


class SimpleClassFactory(object):

    @staticmethod
    def create_work(type):
        """
        简单工厂，用于创建工作
        """
        if type == 'bc':
            return BasicClass()
        elif type == 'pc':
            return ProjectClass()


if __name__ == '__main__':
    work_type = random.choice(['bc', 'pc'])
    work = SimpleClassFactory.create_work(work_type)
    print(work.get_work())

```

    这段代码的理念其实很简单，就是类似一个函数，传入需要创建的产品类型，然后返回相应的产品就行了。在这里work是我们的产品
    然后使用SimpleCourseFactory.create_work来创建work，在这个静态方法中，我们根据传递的需要创建的work类型来创建不同的
    work。
    
    但是
    
    如果需要增加一种产品（比如：modulework），那我们还需要改造整个工厂，这显然一点都不cool。。。
    
    