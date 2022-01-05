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

cookie = json.load(open('job/zhilian_cookie.txt','r'))

class ZhilianSpider(scrapy.Spider):
    name = 'zhilian'
    allowed_domains = ['zhaopin.com']
    start_urls = ['http://https://sou.zhaopin.com//']
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'job.middlewares.ZhilianDownloaderMiddleware': 543,
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
        self.d.get('https://sou.zhaopin.com')
        for i in cookie:
            if 'expirationDate' in i.keys():
                i["expirationDate"] = int(time.time()+10000000)
            self.d.add_cookie(i)
    def closed(self, spider):
        self.d.close()
        
    def start_requests(self):
        base_url = 'https://sou.zhaopin.com/?jl={}&p={}'
        urls = []
        """
        >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        地区不全
        
        """
        citys = {'上海':538, '北京':530, '广州':763, '深圳':765, '天津':531, '武汉':736, '西安':854, '成都':801, '南京':635, '杭州':653, '重庆':551, '厦门':682}
        for i in citys.items():
            for j in range(1,10):
                url = base_url.format(i,j)
                urls.append(url)
        for i in urls:
            yield scrapy.Request(i, callback=self.parse, dont_filter=True)
    def parse(self, response):
        urls = re.findall('http://jobs.zhaopin.com/(.*?)\.htm\?refcode=4019&amp;srccode=&amp;', response.text)
        for i in urls:
            # print(i.split('.')[0])
            url = 'https://fe-api.zhaopin.com/c/i/jobs/position-detail-new?&number='+i.split('.')[0]
            yield scrapy.Request(url, callback=self.parse_item, dont_filter=True)
    def parse_item(self,response):
        rp = json.loads(re.search('({.*})',response.text).group(1))
        i = rp['data']['detailedPosition']
        item = JobItem()
        item['url'] = i['positionUrl']
        item['job'] = i['positionName']
        item['company'] = i['companyName']
        item['position'] = i['workCity']
        item['salary'] = self.f_salary(i['salary60'])
        item['education'] = i['education']
        item['label'] = i['jobTypeLevelName']
        item['issue'] = i['positionPublishTime']
        item['requires'] = i['jobDescPC']
        item['platform'] = 'zhilian'
        return item
    def f_salary(self,salary):
        a = salary.split('-')
        for i in range(len(a)):
            if '千' in a[i]:
                a[i] = a[i].replace('千','')
            elif '万' in a[i]:
                a[i] = str(float(a[i].replace('万',''))*10)
        return '-'.join(a)