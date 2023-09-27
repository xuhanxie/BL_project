# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql


class BridgelegalPipeline:
    def open_spider(self, spider):
        self.fp = open('case.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        self.fp.write(str(item))
        return item

    def close_spider(self, spider):
        self.fp.close()


from scrapy.utils.project import get_project_settings
class MysqlPipeline:
    def open_spider(self, spider):
        settings = get_project_settings()
        self.host = settings['DB_HOST']
        self.port = settings['DB_PORT']
        self.user = settings['DB_USER']
        self.password = settings['DB_PASSWORD']
        self.db = settings['DB_NAME']
        self.charset = settings['DB_CHARSET']
        self.connect()

    def connect(self):
        self.conn = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            db=self.db,
            charset=self.charset
        )

        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        sql = 'INSERT INTO masstorts(case_name, article, url, date) values("{}", "{}", "{}", "{}")'.format(item['case'], item['article'], item['url'], item['date'])
        self.cursor.execute(sql)
        self.conn.commit()
        print("Database inserted successfully")
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()
