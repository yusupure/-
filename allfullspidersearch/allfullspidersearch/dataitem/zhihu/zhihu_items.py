
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst,Join,MapCompose

# def return_value(value):
#     return value
#
# class zhihunewItemloader(ItemLoader):
#     default_output_processor = TakeFirst()
from allfullspidersearch.dataset.dataset import MD5_sh
import re

class ZhihuItemLoader(scrapy.Item):
    zhihu_url_id=scrapy.Field()#Id
    zhihu_title=scrapy.Field()#标题
    zhihu_commer=scrapy.Field()#评论数
    zhihu_tags=scrapy.Field()#标识
    zhihu_itemInner=scrapy.Field()#关注人
    zhihu_item=scrapy.Field()#浏览次数
    zhihu_detail = scrapy.Field()
    zhihu_headerText=scrapy.Field()#回答数
    zhihu_unescapable=scrapy.Field()#回答内容
    def clean_data(self):
        self['zhihu_url_id'] = MD5_sh(self['zhihu_url_id'][0])
        self['zhihu_title'] = self['zhihu_title'][0]  # 标题
        self['zhihu_commer'] =int(re.findall(r'(\d+).*',self['zhihu_commer'][0],re.S)[0])# 评论数
        self['zhihu_tags'] = ','.join(self['zhihu_tags'])# 标识
        self['zhihu_itemInner'] = int(self['zhihu_itemInner'][0])  # 关注人
        self['zhihu_item'] = int(self['zhihu_item'][1])  # 浏览次数

    def save_sql_es(self):
        insert_sql='''
            insert into zhihunew(zhihu_url_id,zhihu_title,zhihu_commer,zhihu_tags,zhihu_itemInner,zhihu_item)
            values (%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE zhihu_commer=VALUES(zhihu_commer),
            zhihu_itemInner=VALUES(zhihu_itemInner),zhihu_item=VALUES(zhihu_item)
        '''
        # zhihu_url_id = MD5_sh(self['zhihu_url_id'][0])
        # zhihu_title = self['zhihu_title'][0]  # 标题
        # zhihu_commer =int(re.findall(r'(\d+).*',self['zhihu_commer'][0],re.S)[0])# 评论数
        # zhihu_tags = ','.join(self['zhihu_tags'])# 标识
        # zhihu_itemInner = int(self['zhihu_itemInner'][0])  # 关注人
        # zhihu_item = int(self['zhihu_item'][1])  # 浏览次数
        self.clean_data()
        parmer=(self['zhihu_url_id'],self['zhihu_title'],self['zhihu_commer'],self['zhihu_tags'],
                self['zhihu_itemInner'],self['zhihu_item'])
        return (insert_sql,parmer)




# class zhihusjsonItemLoader(scrapy.item):
#     zhihuid=scrapy.Field()
#     zhihu_content=scrapy.Field()
#     zhihu_title=scrapy.Field()
#     url_token=scrapy.Field()
#     follow_name=scrapy.Field()
