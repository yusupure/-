
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst,Join,MapCompose

def return_value(value):
    return value

class zhihunewItemloader(ItemLoader):
    default_output_processor = TakeFirst()

class ZhihuItemLoader(scrapy.Item):
    zhihu_url_id=scrapy.Field()#Id
    zhihu_title=scrapy.Field()#标题
    zhihu_commer=scrapy.Field()#评论数
    zhihu_tags=scrapy.Field()#标识
    zhihu_itemInner=scrapy.Field()#关注人
    #zhihu_item=scrapy.Field()#浏览次数
    zhihu_headerText=scrapy.Field()#回答数
    zhihu_unescapable=scrapy.Field()#回答内容
