# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

#from elasticsearch_dsl import connections
#from allfullspidersearch.dataitem.zhihu.zhihu_es_sql import ZhuhuArticleType
#es = connections.connections.create_connection(ZhuhuArticleType._doc_type.using, hosts = '192.168.7.126')

class AllfullspidersearchPipeline(object):
    def process_item(self, item, spider):
        return item

class zhihuspiderPipline(object):
    def process_item(self, item, spider):
        item.elasticsearch_es_sql()
        return item

class zhihuanswerPipline(object):
    def process_item(self, item, spider):
        try:
            item.elasticsearch_anes_sql()
        except:
            pass
        return item
