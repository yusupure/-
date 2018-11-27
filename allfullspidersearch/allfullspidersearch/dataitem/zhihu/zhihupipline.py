
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
import os

from elasticsearch_dsl import connections
from scrapy.exporters import JsonItemExporter
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.serialize import ScrapyJSONEncoder
import requests
import pymysql
from twisted.enterprise import adbapi
import pymysql.cursors

from allfullspidersearch.dataitem.jobboler.jobboler_es_sql import ArticleType
from allfullspidersearch.dataitem.zhihu.zhihu_es_sql import ZhuhuArticleType
from allfullspidersearch.dataitem.zhihu.zhihu_items import ZhihuItemLoader

es = connections.connections.create_connection(ZhuhuArticleType._doc_type.using, hosts = '192.168.7.126')

class AllfullspidersearchPipeline(object):
    def process_item(self, item, spider):
        return item

def gen_suggest(index, info_tuple):
        # 根据字符串生成所搜建议数据
        # python重要性titel:10
    used_words = set()
    suggest = []
    for text, weight in info_tuple:
        if text:
            # 调用es的analyze借口分析字符串
            words = es.indices.analyze(index = index, analyzer = "ik_max_word", params = {'filter': ['lowercase']},                           body = text)
            anylzed_words = set([r['token'] for r in words['tokens'] if len(r["token"]) > 1])
            new_words = anylzed_words - used_words
        else:
            new_words = set()
        if new_words:
            suggest.append({"input": list(new_words), "weight": weight})
    return suggest

class zhihuspiderPipline(object):
    def process_item(self, item, spider):
        item.elasticsearch_es_sql()
        return item
