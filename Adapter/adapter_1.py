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