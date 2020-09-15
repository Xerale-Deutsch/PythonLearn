# 装饰器模式_1

    说到装饰器模式，如果用过Flask，就会想到，在使用Flask-login登录的时候，可以使用login_required装饰器来包装一个需要用户
    登录访问的View，那个东西就是装饰器模式的玩法。
    
```python
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from functools import wraps

HOST_DOCKER = 0


def docker_host_required(f):
    """
    装饰器，必须要求 host 类型是 HOST_DOCKER
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        if args[0].type != HOST_DOCKER:
            raise Exception("Not docker host")
        else:
            return f(*args, **kwargs)
    return wrapper


class Host(object):
    """
    host 类
    """

    def __init__(self, type):
        self.type = type

    # 装饰这一方法
    @docker_host_required
    def create_container(self):
        print("create container")


if __name__ == '__main__':
    # 初始化 Host
    host = Host(HOST_DOCKER)
    host.create_container()
    # 再次初始化 Host 这里给他个1来试试，用try来捕捉一下异常
    try:
        host = Host(1)
        host.create_container()
    except Exception as e:
        print(e)

```

    运行结果：
    create container
    Not docker host
    
    在上面的代码中，Host有一个方法Host.create_container，只有当Host实例的类型是DOCKER_HOST的时候才能执行该方法。
    为了加上这一行为，我们使用了装饰者模式。可以看出使用装饰者模式，我们可以动态改变类的行为，同时能提高代码复用性，因为任何类型为HOST_DOCKER的Host都可以使用该装饰器