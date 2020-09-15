# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import abc


class CommandReceiver(object):
    """
    命令接收者，执行命令的地方
    """

    def start(self):
        print("Command start")

    def stop(self):
        print("Command stop")


class Command(metaclass=abc.ABCMeta):
    """
    命令抽象类
    """

    @abc.abstractmethod
    def execute(self):
        """
        命令对象对外只提供 execute 方法
        """
        pass


class StartCommand(Command):
    """
    开始命令
    """

    def __init__(self, recevier):
        """
        使用一个命令接收者初始化
        """
        self.recevier = recevier

    def execute(self):
        """
        真正执行命令的时候命令接收者开始命令
        """
        self.recevier.start()


class StopCommand(Command):
    """
    终止命令
    """

    def __init__(self, recevier):
        """
        使用一个命令接收者初始化
        """
        self.recevier = recevier

    def execute(self):
        """
        真正执行命令的时候命令接收者终止命令
        """
        self.recevier.stop()


class CommandInvoker(object):
    """
    命令调用者
    """

    def __init__(self, command):
        self.command = command

    def do(self):
        self.command.execute()


if __name__ == '__main__':
    recevier = CommandReceiver()
    start_command = StartCommand(recevier)
    # 命令调用者同时也是客户端，通过命令实例也执行真正的操作
    ci = CommandInvoker(start_command)
    ci.do()

    # 能告诉命令接收者执行不同的操作
    stop_command = StopCommand(recevier)
    ci.command = stop_command
    ci.do()