import time
import pymysql
import scrapy
from ..items import JobItem
import json
import re
from selenium import webdriver
import math
cookie = json.load(open('job/wuyou_cookie.txt','r'))
class WuyouSpider(scrapy.Spider):
    name = 'wuyou'
    allowed_domains = ['www.51job.com']
    start_urls = ['http://www.51job.com/']
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'job.middlewares.WuYouDownloaderMiddleware': 543,
        },
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dada = {
            'lang': 'c',
            'postchannel': '0000',
            'workyear': '99',
            'cotype': '99',
            'degreefrom': '99',
            'jobterm': '99',
            'companysize': '99',
            'ord_field': '0',
            'dibiaoid': '0',
            'line': '',
            'welfare': '',
        }
        option = webdriver.ChromeOptions()
        option.add_argument('--no-sandbox')
        option.add_argument('--disable-gpu')
        # option.add_argument('--headless')
        option.add_experimental_option("excludeSwitches",['enable-automation', 'enable-logging', "ignore-certificate-errors"])
        self.driver = webdriver.Chrome(chrome_options=option)
        self.driver.get('https://login.51job.com/login.php?loginway=0&isjump=0&lang=c&from_domain=i&url=')
        for i in cookie:
            if 'expirationDate' in i.keys():
                i["expirationDate"] = int(time.time()+10000000)
            self.driver.add_cookie(i)

    def start_requests(self):
        print('startrequest')
        salary = {'01': '2千以下', '02': '2-3千', '03': '3-4.5千', '04': '4.5-6千', '05': '6-8千', '06': '0.8-1万',
                  '07': '1-1.5万', '08': '1.5-2万', '09': '2-3万', '10': '3-4万', '11': '4-5万', '12': '5万以上'}
        workyear = {'01': '在校/应届', '02': '1-3年', '03': '3-5年', '04': '5-10年', '05': '>10年', '06': '无'}
        degreefrom = {'01': '初中及以下', '02': '高中/中技/中专', '03': '大专', '04': '本科', '05': '硕士', '06': '博士', '07': '无学历要求'}

        # 全国
        urls = [
            'https://search.51job.com/list/000000,000000,0000,00,9,99,+,2,{}.html?lang=c&postchannel=0000&workyear=' + i + '&cotype=99&degreefrom=' + j + '&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare='
            for i in workyear for j in degreefrom
        ]
        for i in urls:
            url = i.format(1)
            yield scrapy.Request(url, callback=self.parse_page, meta={'url': i})

    def closed(self, spider):
        self.driver.close()

    def get_page(self, response):
        # print('getpage')
        # print(response.text)
        pages = re.search('"total_page":"(\d+?)",', response.text).group(1)
        return int(pages)

    def parse_page(self, response):
        print('parsepage')
        # self.cursor.execute("select page from page where name='wuyou'")
        # start = self.cursor.fetchone()[0]
        # print('start page: ' + str(start))
        pages = self.get_page(response)
        for i in range(1, pages):
            url = response.meta['url'].format(i)
            # print(url)
            yield scrapy.Request(url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        # print(response.text)
        json_item = re.search('<script type="text/javascript">.*?window.__SEARCH_RESULT__ = \{(.*?)\}</script>',
                              response.text, re.S).group(1)
        items = json.loads("{" + json_item + "}")['engine_jds']
        for i in items:
            item = JobItem()
            item['url'] = i['job_href']
            time.sleep(3)
            item['job'] = i['job_title']
            item['company'] = i['company_name']
            item['position'] = i['workarea_text']
            item['salary'] = self.f_salary(i['providesalary_text'])
            item['education'] = "|".join(i['attribute_text'][1:3])
            item['label'] = i['companyind_text']
            item['issue'] = i['issuedate'].split(' ')[0]
            item['requires'] = self.get_require(item['url'])
            item['platform'] = '51job'
            print(item['salary'])
            yield item

    def get_require(self, url):
        self.driver.get(url)
        time.sleep(5)
        require = self.driver.find_element_by_class_name('tCompany_main').text
        # print(len(require))
        return ''.join(require)
    def f_salary(self,salary):
        if '千' in salary:
            return salary.split('千')[0]
        elif '万' in salary:
            if '月' in salary:
                a = salary.split('万')[0].split('-')
                return '-'.join([str(float(i)*10) for i in a])
            elif '年' in salary:
                a = salary.split('万')[0].split('-')
                return '-'.join([str(round(float(i)*10/12),2) for i in a])
        elif '元' in salary:
            return salary.split('元')[0]+'/h'