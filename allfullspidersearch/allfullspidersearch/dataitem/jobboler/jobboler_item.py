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

#默认提取第一个内容方法
class NewjobboleItemload(ItemLoader):
    default_output_processor =TakeFirst()
#提取多个内容方法outinput
def return_value(value):
    return value

#处理日期时间
def datatiemlist(value):
    value=value.replace('·','').strip()
    try:
        datatimedata=datetime.datetime.strptime(value,"%y/%m/%d").date()
    except:
        datatimedata=datetime.datetime.now().date()
    return datatimedata

def tags_list(value):
    if '评论' in value:
        return ""
    else:
        return value

class jobboleSearchItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title=scrapy.Field()
    datelist=scrapy.Field(
        input_processor=MapCompose(datatiemlist)
    )
    category=scrapy.Field(
        input_processor=MapCompose(tags_list),
        output_processor=Join(',')
    )
    mainbody=scrapy.Field(
        #output_processor = MapCompose(return_value)
    )
    image_list_url=scrapy.Field(

    )
    image_list_id=scrapy.Field(
        input_processor=MapCompose(MD5_sh)
    )
    image_list_path=scrapy.Field()

