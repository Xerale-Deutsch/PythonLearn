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
    print("")
    # 再次初始化 Host
    try:
        host = Host(1)
        host.create_container()
    except Exception as e:
        print(e)
