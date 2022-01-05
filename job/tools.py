from pybloom_live import ScalableBloomFilter


class Bloomfilter:
    def __init__(self):
        self.f = ScalableBloomFilter(initial_capacity=100, error_rate=0.001)  # 可扩容过滤容器

    def add(self,value):
        self.f.add('mike')  # 添加元素

    def get(self,value):
        return value in self.f


import pymysql


