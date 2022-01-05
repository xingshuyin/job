import scrapy
import time
import json
import random
import re
import json
import datetime
from ..items import JobItem
from selenium import webdriver
from lxml.etree import HTML
import pymysql


class LagouSpider(scrapy.Spider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = ['http://www.lagou.com/']
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'job.middlewares.LagouDownloaderMiddleware': 543,
        },
    }

    # db = pymysql.connect(host='localhost', user='root', port=3306, password='123456', db='job', charset='utf8')
    # cursor = db.cursor()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        option = webdriver.ChromeOptions()
        option.add_argument('--headless')
        # option.add_argument('--disable-gpu')
        option.add_argument('--no-sandbox')
        option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
        self.d = webdriver.Chrome(chrome_options=option)

    def closed(self, spider):
        self.d.close()

    def start_requests(self):
        gj = ['在校/应届', '3年及以下', '3-5年', '5-10年', '10年以上', '不要求']
        xl = ['大专', '本科', '硕士', '博士', '不要求']
        yx = ['2k以下', '2k-5k', '5k-10k', '10k-15k', '15k-25k', '25k-50k', '50k以上']
        jd = ['未融资', '天使轮', 'A轮', 'B轮', 'C轮', 'D轮及以上', '上市公司', '不需要融资']
        urls = ['https://www.lagou.com/wn/jobs?px=default&gj=' + i + '&pn={}&yx=' + j for i in
                gj for j in yx]
        num = 0
        real_url = []
        for url in urls:
            for j in range(1, 31):
                u = url.format(j)
                real_url.append(u)
        for j in real_url:
            print('page: ' + j)
            yield scrapy.Request(j, callback=self.parse)

    def parse(self, response):
        page_source = response.text
        js = re.search('</span>{(.*?)}<span', page_source).group(1)
        js = json.loads('{' + js + '}')
        items = js['props']['pageProps']['initData']['content']['positionResult']['result']
        for i in items:
            item = JobItem()
            item['url'] = 'https://www.lagou.com/jobs/' + str(i['positionId']) + '.html'
            item['job'] = i['positionName']
            item['company'] = i['companyFullName']
            item['position'] = i['city']
            item['salary'] = self.f_salary(i['salary'])
            item['education'] = i['workYear']
            item['label'] = i['firstType'].replace('|', '/')
            item['issue'] = i['createTime']
            item['requires'] = re.sub('<.*?>', '', i['positionDetail'])
            item['platform'] = 'lagou'
            yield item
    def f_salary(self,salary):
        if 'k' in salary:
            return salary.replace('k','').replace('K','')