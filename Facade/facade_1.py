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