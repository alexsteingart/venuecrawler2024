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
    key = {
      'venue_name': item['venue_name'],
      'territory': item['territory']
    }

    response = self.venues_table.get_item(
      Key=key
    )

    if 'Item' in response:
      # del item['territory']
      # del item['venue_name']
      # set_args = ','.join([f" {x} = :{x}" for x in item.keys()])
      #
      # self.venues_table.update_item(
      #   Key=key,
      #   UpdateExpression=f"SET{set_args}",
      #   ExpressionAttributeValues=dict([(f":{x}", y) for (x,y) in item.items()])
      # )
      pass
    else:
      self.venues_table.put_item(Item=item)
    return item
