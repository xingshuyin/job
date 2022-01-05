from datetime import datetime
import time
import pymysql
import scrapy
from ..items import JobItem
import json
import re
from lxml.etree import HTML
from bs4 import BeautifulSoup
from selenium import webdriver
from copyheaders import headers_raw_to_dict


cookie = json.load(open('job/liepin_cookie.txt','r'))

class LiepinSpider(scrapy.Spider):
    name = 'liepin'
    allowed_domains = ['www.liepin.com']
    start_urls = ['http://www.liepin.com/']
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'job.middlewares.LiepinDownloaderMiddleware': 543,
        },
    }
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        option = webdriver.ChromeOptions()
        option.add_argument('--no-sandbox')
        option.add_argument('--disable-gpu')
        # option.add_argument('--headless')
        option.add_experimental_option("excludeSwitches",['enable-automation', 'enable-logging', "ignore-certificate-errors"])
        self.d = webdriver.Chrome(chrome_options=option)
        self.d.get('https://c.liepin.com/?time=1638363296007')
        for i in cookie:
            self.d.add_cookie(i)
    def closed(self, spider):
        self.d.close()
    def start_requests(self):
        base_url = 'https://www.liepin.com/zhaopin/?headId=56aa611dbfb692503c90ba913eff41f9&eduLevel={}&workYearCode={}&currentPage={}'
        eduLevel = {'博士':'010','MBA/EMBA':'020','硕士':'030','本科':'040','大专':'050','中专/中技':'060','高中':'070','初中及以下':'090'}
        workYearCode = {'应届生':'1','实习生':'2','1年以内':'0$1','1-3年':'1$3','3-5年':'3$5','5-10年':'5$10','10年以上':'10$999',}
        # 默认全国
        dq = {'北京':'010','天津':'030','大连':'210040','上海':'020','南京':'060020','苏州':'060080','杭州':'070020','武汉':'170020','广州':'050020','深圳':'050090','重庆':'040','成都':'280020',}
        urls = []
        for i in eduLevel.items():
            for j in workYearCode.items():
                for k in range(0,10):
                    url = base_url.format(i,j,k)
                    urls.append(url)
        for i in urls:
            yield scrapy.Request(i, callback=self.parse, dont_filter=True)
    def parse(self, response):
        jobs = HTML(response.text).xpath('//div[@class="job-detail-box"]')
        for job in jobs:
            url = job.xpath('./a[@data-nick="job-detail-job-info"]/@href')[0]
            item = JobItem()
            item['url'] = url
            item['company'] = job.xpath('.//span[@class="company-name ellipsis-1"]/text()')[0]
            try:
                item['label'] = job.xpath('.//div[@class="company-tags-box ellipsis-1"]/span[1]/text()')[0]
            except Exception as e:
                print(e)
                item['label'] = ''
            yield scrapy.Request(url, callback=self.parse_item, dont_filter=True, meta={'item':item})
    def f_salary(self,salary):
        print(salary)
        return salary.split('k')[0]

    def parse_item(self,response):
        i = HTML(response.text)
        item = response.meta['item']
        item['job'] = i.xpath('//span[@class="name ellipsis-1"]/text()')[0]
        item['position'] = i.xpath('//div[@class="job-properties"]/span[1]/text()')[0]
        item['salary'] = self.f_salary(i.xpath('//span[@class="salary"]/text()')[0])
        item['education'] = i.xpath('//div[@class="job-properties"]/span[5]/text()')[0]
        item['issue'] = datetime.today()
        item['requires'] = ''.join(i.xpath('//section[@class="job-intro-container"]//text()'))
        item['platform'] = 'liepin'
        return item
