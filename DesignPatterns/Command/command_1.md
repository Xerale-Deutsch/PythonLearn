# 命令模式_1

    顾名思义，命令模式就是对命令的封装。所谓封装命令，就是将一系列操作封装到命令类中，并且命令类只需要对外公开
    一个执行方法execute，调用此命令的对象只需要执行命令的execute方法就可以完成所有的操作。这样调用此命令的对
    象就和命令具体操作之间解耦了。更进一步，通过命令模式可以抽象出调用者，接收者和命令三个对象。调用者就是简单
    的调用命令，然后将命令发送给接收者，而接收者则接收并执行命令，执行命令的方式也是简单的调用命令的execute方
    法就可以了。发送者与接收者之间没有直接引用关系，发送请求的对象只需要知道如何发送请求，而不必知道如何完成请求。
    
```python
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

```

    运行结果：
    Command start
    Command stop
    
    通过命令模式，使命令调用者CommandInvoker和命令接收者CommandRecevier之间解耦，前者不必知道后者具体是怎么进行具体操作的，
    只需要通过CommandInvoker.do()方法调用Command.execute()方法能完成相关操作。
    
    总的来说，命令模式的封装性很好：每个命令都被封装起来，对于客户端来说，需要什么功能就去调用相应的命令，而无需知道命令具体是
    怎么执行的。同时命令模式的扩展性很好，在命令模式中，在接收者类中一般会对操作进行最基本的封装，命令类则通过对这些基本的操作
    进行二次封装，当增加新命令的时候，对命令类的编写一般不是从零开始的，有大量的接收者类可供调用，也有大量的命令类可供调用，代
    码的复用性很好。