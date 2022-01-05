# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobItem(scrapy.Item):

    job = scrapy.Field()  # 职位
    company = scrapy.Field()  # 公司
    position = scrapy.Field()  # 具体地址
    salary = scrapy.Field()  # 薪资
    education = scrapy.Field()  # 学历
    requires = scrapy.Field()  # 具体要求
    url = scrapy.Field()  # 详情链接
    platform = scrapy.Field()  # 平台
    label = scrapy.Field()  # 标签
    issue = scrapy.Field()  # 发布时间
