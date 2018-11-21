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

def check_date(value):
    data=re.findall(r'</i> (.*) <span',value,re.S)
    data=''.join(data).strip()
    return data

def cregt_data(value):
    work_addr=''.join(value).replace('查看地图','')
    return work_addr
class LagousearchItemload(scrapy.Item):
    job_id=scrapy.Field(input_processor=MapCompose(MD5_sh))
    job_company=scrapy.Field()
    job_position=scrapy.Field()
    job_request=scrapy.Field(output_processor=MapCompose(return_value))
    job_detail=scrapy.Field(input_processor=MapCompose(return_value),output_processor=Join(''))
    publish_time=scrapy.Field()
    work_addr=scrapy.Field(input_processor=MapCompose(return_value),output_processor=(cregt_data))
    job_feature=scrapy.Field()
    fourSquare=scrapy.Field(input_processor=MapCompose(check_date))
    trend=scrapy.Field(input_processor=MapCompose(check_date))
    figure=scrapy.Field(input_processor=MapCompose(check_date))
    home=scrapy.Field()

