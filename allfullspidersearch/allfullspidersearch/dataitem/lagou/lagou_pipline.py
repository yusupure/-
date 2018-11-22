# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
import os
from scrapy.exporters import JsonItemExporter
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.serialize import ScrapyJSONEncoder
import requests
import pymysql
from twisted.enterprise import adbapi
import pymysql.cursors

from allfullspidersearch.dataitem.lagou.lagou_es_sql import ArticleType
from elasticsearch_dsl import DocType, Date, Integer, Keyword, Text, connections,Completion
es=connections.connections.create_connection(ArticleType._doc_type.using,hosts='192.168.7.126')#非本地部署elastisearch需添加hosts
def gen_suggest(index,info_tuple):
    #根据字符串生成所搜建议数据
    #python重要性titel:10
    used_words=set()
    suggest=[]
    for text,weight in info_tuple:
        if text:
            #调用es的analyze借口分析字符串
            words=es.indices.analyze(index=index,analyzer="ik_max_word",params={'filter':['lowercase']},body=text)
            anylzed_words=set([r['token'] for r in words['tokens'] if len(r["token"])>1])
            new_words=anylzed_words-used_words
        else:
            new_words=set()
        if new_words:
            suggest.append({"input":list(new_words),"weight":weight})
    return suggest

class ElasicsearchPipline(object):
    def process_item(self, item, spider):
        article=ArticleType()
        article.job_company = item['job_company']
        article.job_position = item['job_position']
        article.job_salary = item['job_salary']
        article.job_address = item['job_address']
        article.job_experience = item['job_experience']
        article.job_education = item['job_education']
        article.job_request = item['job_request']
        article.job_detail = item['job_detail']
        article.publish_time =item['publish_time']
        article.work_addr =item['work_addr']
        #article.job_feature = item['job_feature']
        article.fourSquare = item['fourSquare']
        article.trend = item['trend']
        article.figure = item['figure']
        article.home = item['home']
        article.suggest = gen_suggest(article._doc_type.index, ((article.job_company, 10),(article.job_request,7)))  # 用来控制模糊搜索设置权重weight
        article.save()
        return item
