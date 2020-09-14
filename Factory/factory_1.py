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
