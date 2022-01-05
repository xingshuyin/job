from scrapy.cmdline import execute
from apscheduler.schedulers.blocking import BlockingScheduler
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def mian(**kwargs):
    p = CrawlerProcess(get_project_settings())
    spiders = ['lagou']
    print(p.spiders.list())
    for spider_name in p.spiders.list():
        if spider_name in spiders:
            p.crawl(spider_name)
            execute(['srapy', 'crawl', spider_name])
    p.start()


if __name__ == '__main__':
    mian()
    s = BlockingScheduler()
    s.add_job(mian, 'cron', day_of_week=1, hour=1, minute=00)
    s.start()