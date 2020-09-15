# 适配器模式_1

    所谓适配器，这个词见过最多的应该就是电源适配器，假如你买了港行的iPhone，他们赠送的就是适应香港地区的电源适配器，拿回
    大陆使用，可能用不了，但是国行的就能用，这就是适配的问题，而想要用这个港行的插头，那就得用一个转换器，需要把插头插在
    转换器上，再插在电源上才能使用，这就是适配器模式。
    
```python
# !/usr/bin/env python3
# -*- coding: utf-8 -*-


class OldModel(object):
    """
    老型号类
    """

    def show(self):
        """
        显示关于本型号的所有信息
        """
        print("show old description")
        print("show old author of model")
        print("show old factory")


class Machine(object):
    """
    使用型号的机器
    """

    def __init__(self, model):
        self.model = model

    def render(self):
        self.model.show()


class NewModel(object):
    """
    新型号类, 为了模块化显示信息，实现了新型号类
    """
    def show_desc(self):
        """
        显示描述信息
        """
        print("show new description")

    def show_author(self):
        """
        显示作者信息
        """
        print("show new author of model")

    def show_factory(self):
        """
        显示工厂
        """
        print("show new factory")


class Adapter(object):
    """
    适配器, 尽管实现了新模型类，但是在很多代码中还是需要使用 OldModel.show() 方法
    """

    def __init__(self, model):
        self.model = model

    def show(self):
        """
        适配方法，调用真正的操作
        """
        self.model.show_desc()
        self.model.show_author()
        self.model.show_factory()


if __name__ == '__main__':
    old_model = OldModel()
    machine = Machine(old_model)
    machine.render()
    print("")
    new_model = NewModel()
    # 新课程类没有 show 方法，我们需要使用适配器进行适配
    adapter = Adapter(new_model)
    machine = Machine(adapter)
    machine.render()

```

    运行结果：
    show old description
    show old author of model
    show old factory
    
    show new description
    show new author of model
    show new factory
    
    在这段代码中，我们有一个OldModel类，它有一个show方法，来显示具体信息，并且在Machine中能够用到，但是为了满足产品的进步，
    我们又有了NewModel类，但是这个NewModel类只能满足部分信息的展示。为了使NewModel也能在Machine中正常使用，就用到了适配器
    模式来给他做个兼容。在适配器Adapter中，就可以调用其show方法了。
    
    适配器模式就是把一个类的接口变换成客户端所期待的另一种接口，使原本因接口不兼容而无法在一起工作的两个类能够在一起工作。
    