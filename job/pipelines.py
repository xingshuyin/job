# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
import emoji
import re
from pymysql.converters import escape_string
import datetime
import time
import hashlib


class JobPipeline:
    def __init__(self):
        print('connect mysql')
        self.db = pymysql.connect(host='47.104.78.62', user='root', port=3306, password='111111', db='job', charset='utf8')
        # self.db = pymysql.connect(host='127.0.0.1', user='root', port=3306, password='123456', db='job', charset='utf8')
        self.cursor = self.db.cursor()

    def process_item(self, item, spider):
        try:

            job = escape_string(item['job'])  # 自动转译\
            company = escape_string(item['company'])
            position = escape_string(item['position'])
            salary = escape_string(item['salary'])
            education = escape_string(item['education'])
            requires = escape_string(item['requires'].strip())
            platform = escape_string(item['platform'])
            url = escape_string(item['url'])
            url_hash = hashlib.md5(url.encode(encoding='utf-8')).hexdigest()
            label = item['label']
            issue = item['issue']
            get_data = datetime.datetime.today()
            sql = f"""insert IGNORE into message(id,job,company,position,salary,education,requires,url,platform,label,issue,
            get_data,url_hash) values (default,"{job}","{company}","{position}","{salary}","{education}","{requires}","{url}",
            "{platform}","{label}","{issue}","{get_data}","{url_hash}") 
            """
            # sql = re.sub('(:.*?:)', '',   
            self.cursor.execute(emoji.demojize(sql))  # emoji.demojize(sql))->用于表情符号引起的处理编码问题

            for i in label.split("/"):
                insert_label = f"""
                    insert IGNORE into label(url_hash,label) values ("{url_hash}", "{i}")
                """
                self.cursor.execute(insert_label)
            self.db.commit()
            print(item['company'], item['url'], item['requires'][:10])

        except pymysql.err.InterfaceError:
            self.db.ping(reconnect=True)  # 服务自动断开后重连
            self.cursor.execute(emoji.demojize(sql))
            self.db.commit()

    def close(self):

        self.db.close()
