# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2
import os


class FormcPipeline:

    def open_spider(self, spider):
        host=os.environ['DB_HOST']
        user=os.environ['DB_USER']
        password=os.environ['DB_PASS']
        dbname=os.environ['DB_NAME']
        self.connection = psycopg2.connect( host=host, user=user, password=password, dbname=dbname)
        self.c = self.connection.cursor()



    def process_item(self, item, spider):
        return item
