import scrapy
from ..items import JobItem
from lxml.etree import HTML
import datetime
import json
from selenium import webdriver
class TongchengSpider(scrapy.Spider):
    name = 'tongcheng'
    allowed_domains = ['http://sjz.58.com/job/pve_5363_244/?utm_source=sem-360-pc&spm=42692169095.f1fd8fc7f256fd3a&utm_campaign=sell&utm_medium=cpc']
    start_urls = ['http://https://sjz.58.com/job/pve_5363_244/?utm_source=sem-360-pc&spm=42692169095.f1fd8fc7f256fd3a&utm_campaign=sell&utm_medium=cpc/']
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'job.middlewares.TongchengDownloaderMiddleware2': 543,
        },
        'COOKIES_ENABLED':True
    }
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        option = webdriver.ChromeOptions()
        option.add_argument('--no-sandbox')
        option.add_argument('--disable-gpu')
        # option.add_argument('--headless')
        option.add_experimental_option("excludeSwitches",['enable-automation', 'enable-logging', "ignore-certificate-errors"])
        self.d = webdriver.Chrome(chrome_options=option)
        # self.d.set_page_load_timeout(10)
        with open('job/tongcheng_cookie.txt','r') as c:
            self.cookie = json.loads(c.read())



    def start_requests(self):
        self.d.get('https://sjz.58.com//?utm_source=sem-360-pc&spm=35028788141.8428840355&utm_campaign=sell&utm_medium=cpc')
        for i in self.cookie:
            try:
                if str(i['expiry'])[0] == '1':
                    i['expiry'] = int(time.time()) + 100
            except:
                pass
            self.d.add_cookie(i)
        urls = []
        for i in range(2,9):
            for j in range(4,10):
                for k in ['2000_2999','3000_4999','6000_7999','8000,11999','12000_19999','20000_24999','25000_999999']:
                    for l in range(1,11):
                        url = f'https://sjz.58.com/job/pn{l}/pve_5356_{i}_pve_5357_{j}/?utm_source=sem-360-pc&spm=42692169095.f1fd8fc7f256fd3a&utm_campaign=sell&utm_medium=cpc&minxinzi={k}'
                        urls.append(url)
        for m in urls[20:]:
            yield scrapy.Request(m,callback=self.parse,dont_filter=True, meta={'page':1,'url':m},cookies=self.cookie)

    def closed(self,spider):
        self.d.close()

    def parse(self, response):
        rp = HTML(response.text)
        # print(rp)
        dl = rp.xpath('//div[@id="infolist"]/dl')
        # if len(dl)<=0:
        #     self.isblank = True
        for i in dl:
            item = JobItem()
            item['url'] = i.xpath('./dt[1]/a/@href')[0]
            item['job'] = i.xpath('./dt[1]/a/text()')[0]
            issue = i.xpath('./dd[last()]/text()')[0]
            if '今天' in issue:
                issue = str(datetime.datetime.today())
            item['issue'] = issue
            # print(item['url'])
            yield scrapy.Request(item['url'],callback=self.parse_item,dont_filter=True, meta={'item':item,'page':0,'url':item['url']})

    def parse_item(self,response):
        print(response.text[2])
        rp = HTML(response.text)
        item = response.meta['item']
        item['company'] = rp.xpath('//div[@class="baseInfo_link"]/a/text()')[0]
        try:
            item['position'] = rp.xpath('//span[@class="pos_area_span pos_address"]/span[2]/text()|//div[@class="pos-area"]/span/text()')[0]
        except:
            item['position'] = ''
        item['salary'] = ''.join(rp.xpath('//span[@class="pos_salary"]//text()'))
        item['education'] = rp.xpath('//span[@class="item_condition"]/text()')[0]
        item['label'] = rp.xpath('//p[@class="comp_baseInfo_belong"]//text()')[0]
        item['requires'] = ''.join(rp.xpath('//div[@class="subitem_con pos_description"]//text()'))
        item['platform'] = 'tongcheng'
        yield item



