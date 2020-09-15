# 外观模式_1

    所谓外观模式，就是将各种子系统的复杂操作通过外观模式简化，让客户端使用起来更方便简洁。
    这里用一个商业网课站的创建课程学习逻辑来展示。
    
```python
# !/usr/bin/env python3
# -*- coding: utf-8 -*-


class User(object):
    """
    用户类
    """
    def is_login(self):
        return True

    def has_privilege(self, privilege):
        return True


class Course(object):
    """
    课程类
    """
    def can_be_learned(self):
        return True


class Lesson(object):
    """
    章节类
    """
    def can_be_started(self):
        return True


class Client(object):
    """
    客户类，用于开始一门课程的学习
    """
    def __init__(self, user, course, lesson):
        self.user = user
        self.course = course
        self.lesson = lesson

    def start_learn(self):
        """
        开始实验，需要一系列的判断：用户是否登录，课程是否可以学习，实验是否可以开始。判断非常繁琐！
        """
        if self.user.is_login() and self.course.can_be_learned() and self.lesson.can_be_started():
            print("start learning")
        else:
            print("can not start learning")


class FacadeLesson(object):
    """
    新的Lesson类，应用了面向对象模式
    """

    def __init__(self, user, course, lesson):
        self.user = user
        self.course = course
        self.lesson = lesson

    def can_be_started(self):
        if self.user.is_login() and self.course.can_be_learned() and self.lesson.can_be_started():
            return True
        else:
            return False


class NewClient(object):
    """
    新的客户类，使用外观模式
    """
    def __init__(self, facade_lesson):
        self.lesson = facade_lesson

    def start_lesson(self):
        """
        开始实验，只需要判断 FacadeLesson 是否可以开始
        """
        if self.lesson.can_be_started:
            print("start learning")
        else:
            print("can not start learning")


if __name__ == '__main__':
    user = User()
    course = Course()
    lesson = Lesson()
    client = Client(user, course, lesson)
    client.start_learn()

    print("Use Facade Pattern:")
    facade_lesson = FacadeLesson(user, course, lesson)
    facade_client = NewClient(facade_lesson)
    facade_client.start_lesson()

```

    运行结果：
    start learning
    Use Facade Pattern:
    start learning
    
    正常情况下，我们开始一个课程的学习，需要判断一系列前置条件：用户是否已经登录，用户是否购买了课程，课程是否满足学习的条件等。
    如果我们直接将这些对象在客户端Client类中使用，无疑增加了客户端类和User，Course和Lesson类的耦合度。另外如果我们要增加新的
    前置条件判断时，我们就要修改Client类。为了解决这些问题，我们引入了外观模式实现了FacadeLab类，在这个类中，我们通过对外提供
    接口FacadeLesson.can_be_started来屏蔽客户端类对子系统的直接访问，使得新的客户端类NewClient的代码变得简洁。
    
    总的来说外观模式的主要目的在于降低系统的复杂程度，在面向对象软件系统中，类与类之间的关系越多，不能表示系统设计得越好，反而
    表示系统中类之间的耦合度太大，这样的系统在维护和修改时都缺乏灵活性，因为一个类的改动会导致多个类发生变化，而外观模式的引入
    在很大程度上降低了类与类之间的耦合关系。引入外观模式之后，增加新的子系统或者移除子系统都非常方便，客户类无须进行修改（或者
    极少的修改），只需要在外观类中增加或移除对子系统的引用即可。