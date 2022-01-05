# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import json
import scrapy
from scrapy import signals
import requests
from selenium import webdriver
from scrapy.http import HtmlResponse
import time
import random
import selenium
import twisted


class WuYouDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # print('processrequest')
        self.ua = random.choice(self.User_Agent_list)
        request.headers.setdefault('User-Agent', self.ua)
        return None

    User_Agent_list = [
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36',
        'Mozilla/5.0 (X11; OpenBSD i386) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2309.372 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2117.157 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1866.237 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/4E423F',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36 Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.517 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1664.3 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1664.3 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1623.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.17 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS i686 4319.74.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.2 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1467.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1500.55 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.90 Safari/537.36',
        'Mozilla/5.0 (X11; NetBSD) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.60 Safari/537.17',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17',
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.15 (KHTML, like Gecko) Chrome/24.0.1295.0 Safari/537.15',
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.14 (KHTML, like Gecko) Chrome/24.0.1292.0 Safari/537.14']

    def process_response(self, request, response, spider):
        # print('process_response')
        return response

    def process_exception(self, request, exception, spider):
        return None

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


def get_proxy(num=1):
    passPort = ['1', '7', '9', '11', '13', '15', '17', '19', '20', '21', '22', '23', '25', '37', '42', '43', '53', '77',
                '79', '87', '95', '101', '102', '103', '104', '109', '110', '111', '113', '115', '117', '119', '123',
                '135', '139', '143', '179', '389', '465', '512', '513', '514', '515', '526', '530', '531', '532', '540',
                '556', '563', '587', '601', '636', '993', '995', '2049', '3659', '4045', '6000', '6665', '6666', '6667',
                '6668', '6669']  # 排除谷歌不支持端口

    proxy_url = f'http://api.qingtingip.com/ip?app_key=45ecbcf3aa28ef214b8606c9aeb93eba&num={num}&ptc=http&fmt=json&lb=\r\n&port=0&mr=1&'
    header = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36 Edg/93.0.961.52',
    }
    rp = requests.get(proxy_url, headers=header)
    rp = json.loads(rp.text)
    # while str(rp['data'][0]['port']) in passPort:
    #     time.sleep(1)
    #     rp = requests.get(proxy_url, headers=header)
    #     rp = json.loads(rp.text)
    proxys = ['http://' + str(i['ip']) + ':' + str(i['port']) for i in rp['data']]
    print(proxys)
    return proxys


from lxml.etree import HTML


class LagouDownloaderMiddleware:
    with open('job/lagou_cookies.txt', 'r') as c:  # 添加cookie前要访问一下网站不然会造成domain与当前连接不符
        print('open cookie')
        cookie = json.load(c)

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        print('process_request')
        url = 'view-source:' + request.url
        time.sleep(1)
        spider.d.get(url)
        time.sleep(random.randint(4, 6))
        # cookie字典组成的列表, 一定要在浏览器请求地址后设置
        # print('>>>>>>>>>>> set cookies <<<<<<<<<<')
        for i in self.cookie:
            try:
                if str(i['expiry'])[0] == '1':
                    i['expiry'] = int(time.time()) + 100
            except:
                pass
            spider.d.add_cookie(i)
        source = spider.d.page_source
        return HtmlResponse(url, body=source, status=200, encoding='utf-8')

    def process_response(self, request, response, spider):
        print('process_response')
        # print(response.text)
        if '账号安全提醒' in response.text:
            print(response.text)
            spider.d.close()
            option = webdriver.ChromeOptions()
            option.add_argument('--headless')
            # option.add_argument('--disable-gpu')
            option.add_argument('--no-sandbox')
            option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
            proxy = get_proxy()[0]
            option.add_argument("--proxy-server=" + proxy)
            spider.d = webdriver.Chrome(chrome_options=option)
            print('设置代理: ' + get_proxy())
            return request
        return response

    def process_exception(self, request, exception, spider):
        print('process_exception')
        # if exception is selenium.common.exceptions.WebDriverException:
        #     print('selenium.common.exceptions.WebDriverException>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        # spider.d.close()
        # option = webdriver.ChromeOptions()
        # # option.add_argument('--headless')
        # # option.add_argument('--disable-gpu')
        # option.add_argument('--no-sandbox')
        # option.add_experimental_option('excludeSwitches', ['enable-automation'])
        # proxy = get_proxy()
        # option.add_argument("--proxy-server=" + proxy)
        # spider.d = webdriver.Chrome(chrome_options=option)
        # print('设置代理: ' + get_proxy())
        # return request

        return None

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class BossDownloaderMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        print('process_request')
        url = request.url
        spider.d.get(url)
        time.sleep(random.randint(4, 6))
        source = spider.d.page_source
        return HtmlResponse(url, body=source, status=200, encoding='utf-8')

    def process_response(self, request, response, spider):
        if '点击进行验证 ' in response.text or '您暂时无法继续访问' in response.text or '未连接到互联网' in response.text or '无法访问此网站' in response.text or '请在五分钟内完成验证' in response.text:
            spider.d.close()
            option = webdriver.ChromeOptions()
            option.add_argument('--headless')
            # option.add_argument('--disable-gpu')
            option.add_argument('--no-sandbox')
            option.add_experimental_option("excludeSwitches",
                                           ['enable-automation', 'enable-logging', "ignore-certificate-errors"])
            proxy = get_proxy()[0]
            option.add_argument("--proxy-server=" + proxy)
            spider.d = webdriver.Chrome(chrome_options=option)
            print('设置代理: ' + get_proxy()[0])
            return request
        return response

    def process_exception(self, request, exception, spider):
        if exception is selenium.common.exceptions.WebDriverException:
            print('selenium.common.exceptions.WebDriverException>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            spider.d.close()
            option = webdriver.ChromeOptions()
            option.add_argument('--headless')
            # option.add_argument('--disable-gpu')
            option.add_argument('--no-sandbox')
            option.add_experimental_option('excludeSwitches', ['enable-automation'])
            proxy = get_proxy()
            option.add_argument("--proxy-server=" + proxy)
            spider.d = webdriver.Chrome(chrome_options=option)
            print('设置代理: ' + get_proxy())
            return request
        return None

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


User_Agent_list = [
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36',
    'Mozilla/5.0 (X11; OpenBSD i386) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2309.372 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2117.157 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1866.237 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/4E423F',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36 Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.517 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1664.3 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1664.3 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1623.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.17 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36',
    'Mozilla/5.0 (X11; CrOS i686 4319.74.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.2 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1467.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1500.55 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.90 Safari/537.36',
    'Mozilla/5.0 (X11; NetBSD) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36',
    'Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.60 Safari/537.17',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.15 (KHTML, like Gecko) Chrome/24.0.1295.0 Safari/537.15',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.14 (KHTML, like Gecko) Chrome/24.0.1292.0 Safari/537.14']


class TongchengDownloaderMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.proxys = get_proxy(10)
        self.num = 0

    def process_request(self, request, spider):
        if request.meta['page'] == 1:
            # url = 'view-source:'+request.url
            url = request.url
            for i in spider.cookie:
                try:
                    if str(i['expiry'])[0] == '1':
                        i['expiry'] = int(time.time()) + 100
                except:
                    pass
                spider.d.add_cookie(i)
            spider.d.get(url)
            time.sleep(random.randint(5, 8))
            source = spider.d.page_source
            return HtmlResponse(url, body=source, status=200, encoding='utf-8')
        elif request.meta['page'] == 0:
            proxy = self.proxys[self.num]
            self.num += 1
            if self.num > 9:
                self.num = 0
            print('使用代理(process_request): ' + proxy)
            request.meta['proxy'] = proxy
            # request.cookies = self.cookie
            request.headers['User-Agent'] = random.choice(User_Agent_list)
            time.sleep(6)
            return None

    def process_response(self, request, response, spider):

        if '请在五分钟内完成验证' in response.text:
            proxy = request.meta['proxy']
            print('IP失效(process_response):  ' + proxy + '  ' + request.meta['url'])
            del self.proxys[self.proxys.index(proxy)]
            self.proxys.append(get_proxy()[0])
            return scrapy.Request(request.meta['url'], callback=spider.parse_item, dont_filter=True,
                                  meta={'item': request.meta['item'], 'page': 0, 'url': request.meta['url']})
        return response

    def process_exception(self, request, exception, spider):
        if exception is twisted.internet.error.ConnectError:
            proxy = request.meta['proxy']
            print('IP失效(process_exception):  ' + proxy)
            del self.proxys['proxy']
            self.proxys.append(get_proxy()[0])
            return scrapy.Request(request.meta['url'], callback=spider.parse_item, dont_filter=True,
                                  meta={'item': request.meta['item'], 'page': 0, 'url': request.meta['url']})
        return None

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class TongchengDownloaderMiddleware2:
    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with open('job/tongcheng_cookie.txt', 'r') as c:
            self.cookie = json.loads(c.read())

    def process_request(self, request, spider):
        print('process_request')
        url = request.url
        # for i in self.cookie:
        #     try:
        #         if str(i['expiry'])[0] == '1':
        #             i['expiry'] = int(time.time()) + 100
        #     except:
        #         pass
        #     spider.d.add_cookie(i)
        spider.d.get(url)
        time.sleep(random.randint(4, 6))
        source = spider.d.page_source
        if '请在五分钟内完成验证' in source:
            button = spider.d.find_element_by_id('btnSubmit').click()
            time.sleep(5)
        source = spider.d.page_source
        return HtmlResponse(url, body=source, status=200, encoding='utf-8')

    def process_response(self, request, response, spider):
        if '请在五分钟内完成验证' in response.text:
            time.sleep(10)
            # button = spider.d.find_element_by_id('btnSubmit').click()
            spider.d.close()
            option = webdriver.ChromeOptions()
            # option.add_argument('--headless')
            # option.add_argument('--disable-gpu')
            option.add_argument('--no-sandbox')
            option.add_experimental_option("excludeSwitches",
                                           ['enable-automation', 'enable-logging', "ignore-certificate-errors"])
            proxy = get_proxy()[0]
            option.add_argument("--proxy-server=" + proxy)
            spider.d = webdriver.Chrome(chrome_options=option)
            spider.d.get(
                'https://sjz.58.com//?utm_source=sem-360-pc&spm=35028788141.8428840355&utm_campaign=sell&utm_medium=cpc')
            for i in self.cookie:
                try:
                    if str(i['expiry'])[0] == '1':
                        i['expiry'] = int(time.time()) + 100
                except:
                    pass
                spider.d.add_cookie(i)
            print('设置代理(process_response): ' + get_proxy()[0])
            return Request(request.meta['url'], callback=spider.parse_item, dont_filter=True,
                           meta={'url': request.meta['url']})
        return response

    def process_exception(self, request, exception, spider):
        # if exception is selenium.common.exceptions.WebDriverException:
        #     print('selenium.common.exceptions.WebDriverException>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        #     spider.d.close()
        #     option = webdriver.ChromeOptions()
        #     # option.add_argument('--headless')
        #     # option.add_argument('--disable-gpu')
        #     option.add_argument('--no-sandbox')
        #     option.add_experimental_option('excludeSwitches', ['enable-automation'])
        #     proxy = get_proxy()
        #     option.add_argument("--proxy-server=" + proxy)
        #     spider.d = webdriver.Chrome(chrome_options=option)
        #     print('设置代理(process_exception): ' + get_proxy())
        #     spider.d.get('https://sjz.58.com/')
        #     return request
        return None

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ZhilianDownloaderMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        print('process_request')
        url = 'view-source:' + request.url
        # url = request.url
        time.sleep(3)
        spider.d.get(url)
        time.sleep(random.randint(2, 3))
        source = spider.d.page_source
        return HtmlResponse(url, body=source, status=200, encoding='utf-8')

    def process_response(self, request, response, spider):
        # print('process_response')
        # # print(response.text)
        # if '账号安全提醒' in response.text:
        #     print(response.text)
        #     spider.d.close()
        #     option = webdriver.ChromeOptions()
        #     option.add_argument('--headless')
        #     # option.add_argument('--disable-gpu')
        #     option.add_argument('--no-sandbox')
        #     option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
        #     proxy = get_proxy()[0]
        #     option.add_argument("--proxy-server=" + proxy)
        #     spider.d = webdriver.Chrome(chrome_options=option)
        #     print('设置代理: ' + get_proxy())
        #     return request
        return response

    def process_exception(self, request, exception, spider):
        print('process_exception')

        return None

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class LiepinDownloaderMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        print('process_request')
        # url = 'view-source:' + request.url
        url = request.url
        time.sleep(5)
        spider.d.get(url)
        time.sleep(random.randint(5, 7))
        source = spider.d.page_source
        return HtmlResponse(url, body=source, status=200, encoding='utf-8')

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        print('process_exception')

        return None

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
