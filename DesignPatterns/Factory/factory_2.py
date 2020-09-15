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

