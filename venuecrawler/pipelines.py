# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import boto3

class VenuecrawlerPipeline:
    def open_spider(self, spider):
        self.venues_table = boto3.resource('dynamodb').Table('venues')

    def process_item(self, item, spider):
        self.venues_table.put_item(item)
        return item
