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
#处理数据内含评论数
def tags_list(value):
    if '评论' in value:
        return ""
    else:
        return value
#处理收藏评论赞内中文字去除
def return_number(value):
    numbers=re.findall(".*(\d+).*?",value)
    if numbers:
        return numbers
    else:
        return 0
class jobboleSearchItem(scrapy.Item):
    title=scrapy.Field()
    datelist=scrapy.Field(input_processor=MapCompose(datatiemlist))
    category=scrapy.Field(
        input_processor=MapCompose(tags_list),
        #合并列表内的字符用逗号串联
        output_processor=Join(',')
    )
    mainbody=scrapy.Field()#output_processor = MapCompose(return_value)))
    zang=scrapy.Field(input_processor=MapCompose(return_number))
    sc=scrapy.Field(input_processor=MapCompose(return_number))
    pl=scrapy.Field(input_processor=MapCompose(return_number))
    image_list_url=scrapy.Field(output_processor=MapCompose(return_value))
    image_list_id=scrapy.Field(input_processor=MapCompose(MD5_sh))
    image_list_path=scrapy.Field()

