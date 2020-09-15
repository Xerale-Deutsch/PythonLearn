# 代理模式_1

    所谓代理模式就是给一个对象提供一个代理，并由代理对象控制对原对象的访问。通过代理，我们可以对访问做一些控制。在开发中，
    经常会遇到频繁访问某一资源，如果每次都是新的访问，每次都要重新请求这个资源，那么累积起来的IO耗时，连起来可能绕地球无数圈，
    这时候就会用到缓存技术，通过缓存代理解决一些热门资源访问问题。
    
```python
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import time


class Redis(object):
    """
    用于模拟 redis 服务
    """

    def __init__(self):
        """
        使用字典存储数据
        """
        self.cache = dict()

    def get(self, key):
        """
        获取数据
        """
        return self.cache.get(key)

    def set(self, key, value):
        """
        设置数据
        """
        self.cache[key] = value


class Image(object):
    """
    模拟图片的存储，图片对象，图片存在云端，这里直接用百度logo来模拟
    """

    def __init__(self, name):
        self.name = name

    @property
    def url(self):
        time.sleep(2)
        return "https://www.baidu.com/img/bd_logo1.png"


class Page(object):
    """
    用于显示图片
    """

    def __init__(self, image):
        """
        需要图片进行初始化
        """
        self.image = image

    def render(self):
        """
        显示图片
        """
        print(self.image.url)


redis = Redis()


class ImageProxy(object):
    """
    图片代理，首次访问会从真正的图片对象中获取地址，以后都从 Redis 缓存中获取
    """

    def __init__(self, image):
        self.image = image

    @property
    def url(self):
        addr = redis.get(self.image.name)
        if not addr:
            addr = self.image.url
            print("Set url in redis cache!")
            redis.set(self.image.name, addr)
        else:
            print("Get url from redis cache!")
        return addr


if __name__ == '__main__':
    img = Image(name="logo")
    proxy = ImageProxy(img)
    page = Page(proxy)
    # 首次访问
    page.render()
    print("")
    # 第二次访问
    page.render()

```

    运行结果：
    Set url in redis cache!
    https://www.baidu.com/img/bd_logo1.png
    
    Get url from redis cache!
    https://www.baidu.com/img/bd_logo1.png
    
    使用代理模式实现了对图片的缓存。在使用缓存之前，我们实现了Redis对象简单模拟了Redis服务。可以看到访问Image.url属性是比
    较耗时的操作（我们使用time.sleep模拟了耗时操作），如果每次都是直接访问该属性，就会浪费大量的时间。通过实现ImageProxy
    缓存代理，我们将图片地址缓存到 Redis 中，提高了后续的访问速度。
    
    代理对象和真实的对象之间都实现了共同的接口，这使我们可以在不改变原接口情况下，使用真实对象的地方都可以使用代理对象。
    其次，代理对象在客户端和真实对象之间直接起到了中介作用，同时通过代理对象，我们可以在将客户请求传递给真实对象之前做
    一些必要的预处理。