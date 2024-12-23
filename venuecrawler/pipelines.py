# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import boto3
import os
import googlemaps
from decimal import Decimal

class VenuecrawlerPipeline:
  def open_spider(self, spider):
    self.VENUES_TABLE = boto3.resource('dynamodb').Table('venues')
    self.GMAPS = googlemaps.Client(key=os.environ['GAPI_KEY'])

  def geocode_item(self, item):
    geocode_result = self.GMAPS.geocode(f"{item['venue_name']} {item['address']}")

    if len(geocode_result) < 1:
      return
    if 'geometry' not in geocode_result[0]:
      return

    item['lat'] = Decimal(str(geocode_result[0]['geometry']['location']['lat']))
    item['lng'] = Decimal(str(geocode_result[0]['geometry']['location']['lng']))
    item['place_id'] = geocode_result[0]['place_id']

  def process_item(self, item, spider):
    self.geocode_item(item)
    self.VENUES_TABLE.put_item(Item=item)
    # key = {
    #   'venue_name': item['venue_name'],
    #   'territory': item['territory']
    # }
    #
    # response = self.VENUES_TABLE.get_item(
    #   Key=key
    # )
    #
    # if 'Item' in response:
    #   pass unless
    #   del item['territory']
    #   del item['venue_name']
    #   set_args = ','.join([f" {x} = :{x}" for x in item.keys()])
    #
    #   self.VENUES_TABLE.update_item(
    #     Key=key,
    #     UpdateExpression=f"SET{set_args}",
    #     ExpressionAttributeValues=dict([(f":{x}", y) for (x,y) in item.items()])
    #   )
    # else:
    #   self.VENUES_TABLE.put_item(Item=item)
    return item
