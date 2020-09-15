# 策略模式_1

    这个例子是模拟用户访问页面，如果用户是admin，则显示admin权限的页面，否则是用户显示的页面。
    先展示下没有使用策略模式之前的代码。
    
```python
# !/usr/bin/env python3
# -*- coding: utf-8 -*-


class ShowPage(object):
    """
    问题对象，没有使用策略模式之前的作法
    """

    def __init__(self, admin=True):
        self._role = admin

    def show(self):
        """
        根据权限显示不同的信息
        """
        if self._role is True:
            return "show page as admin"
        else:
            return "show page as user"


if __name__ == '__main__':
    sp = ShowPage(admin=False)
    print(sp.show())
    
```

    上面代码中，根据role角色不同，展示不同页面，逻辑看上去没啥问题，但是如果该死的项目经理又提出了一堆需求。。。
    让你多加一堆角色，那就爽歪歪了，得添加一堆标志位，改吧，累死你不偿命哦。。。(啥时候能把那个项目经理打死呢？)
    基于上述情景，这种写法就很费劲，一点都不cool了。。。
    那么有啥办法来搞定他呢？策略模式可以搞一下~
    
    废话不多说，直接上代码，来吧，展示：
    
```python
# -*- coding: utf-8 -*-

import abc


class AbsShow(metaclass=abc.ABCMeta):
    """
    抽象显示对象
    """

    @abc.abstractmethod
    def show(self):
        pass


class AdminShow(AbsShow):
    """
    管理员的显示操作
    """

    def show(self):
        return "show as admin"


class UserShow(AbsShow):
    """
    普通用户的显示操作
    """

    def show(self):
        return "show as user"


class ShowPage(object):
    """
    问题对象，使用策略模式之后的作法
    """

    def __init__(self, show_obj):
        self.show_obj = show_obj

    def show(self):
        return self.show_obj.show()


if __name__ == '__main__':
    sp = ShowPage(show_obj=AdminShow())
    print(sp.show())
    # 这里替换原来的显示对象，体现了策略模式的互换行为
    sp.show_obj = UserShow()
    print(sp.show())
    
```
    运行结果：
    show as admin
    show as user
    
    ps:为了展现策略模式的互换行为，通过改show_obj来展示下这个行为

    考虑到role的改变的其实只是不同的show方法，那么如果用一个抽象类，来把show的方法搞成个抽象的类，那么不同的角色，
    只需要让他们有不同show方法来重写抽象类的show方法就行了呗？这样把对象和方法解耦合了，每个不同的角色就可以通过
    不同的show方法来展示他们不同的页面了。
    
    
    
    