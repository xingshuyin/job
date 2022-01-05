from apscheduler.schedulers.blocking import BlockingScheduler
import os
from multiprocessing import Process
def run(spider_name):
    os.system('scrapy crawl '+spider_name)
def mian(**kwargs):
    for i in ['wuyou','lagou','zhilian','liepin']:
        p = Process(target=run,args=(i,))
        p.start()




if __name__ == '__main__':

    # mian()
    s = BlockingScheduler()
    s.add_job(mian, 'cron',day_of_week =  hour=10, minute=26)
    s.start()
