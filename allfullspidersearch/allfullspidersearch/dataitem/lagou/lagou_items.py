# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst,MapCompose,Join
import datetime
from allfullspidersearch.dataset.dataset import MD5_sh
import re

class lagouItemloader(ItemLoader):
    default_output_processor = TakeFirst()

def return_value(value):
    return value
def clear_data(value):
    data=value.replace('\n','').strip()
    return data
class LagousearchItemload(scrapy.Item):
    job_id=scrapy.Field()
    job_company=scrapy.Field()
    job_position=scrapy.Field()
    job_request=scrapy.Field(output_processor=MapCompose(return_value))
    job_detail=scrapy.Field(input_processor=MapCompose(return_value),output_processor=Join(''))
    publish_time=scrapy.Field()
    work_addr=scrapy.Field(input_processor=MapCompose(return_value),output_processor=Join(''))
    job_feature=scrapy.Field()
    fourSquare=scrapy.Field(input_processor=MapCompose(return_value),output_processor=MapCompose(clear_data))
    trend=scrapy.Field(input_processor=MapCompose(return_value),output_processor=Join(''))
    figure=scrapy.Field(input_processor=MapCompose(return_value),output_processor=Join(''))
    home=scrapy.Field()
