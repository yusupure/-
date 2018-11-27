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
from allfullspidersearch.dataitem.jobboler.jobboler_es_sql import ArticleType

class AllfullspidersearchPipeline(object):
    def process_item(self, item, spider):
        return item


# JSONdowm自定义：
class Newjsondownload(object):
    def __init__(self):
        self.file = codecs.open('json1.txt', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        # 用ScrapyJSONEncoder调用CLS处理日期date问题
        datalist = json.dumps(dict(item), ensure_ascii=False, cls=ScrapyJSONEncoder) + '\n'
        self.file.write(datalist)
        return item

    def close_json(self):
        self.file.close()


# 内置JSON下载方法
class NkJsondownPipline(object):
    def __init__(self):
        self.file = open('json2.txt', 'wb')
        self.jsdm = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.jsdm.start_exporting()

    def close_json(self):
        self.jsdm.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.jsdm.export_item(item)
        return item


# 自定义IMAGE下载
class NEWimagedownPipline(object):
    def process_item(self, item, spider):
        print(type(item['image_list_url']))
        imagepicture = requests.get(item['image_list_url'])
        filelist = '{}\{}.{}'.format(os.getcwd(), item['image_list_id'], 'jpg')
        with open(filelist, 'wb') as fb:
            fb.write(imagepicture.content)
            fb.close()


# 内置image下载方法
class NkimagedownPipline(ImagesPipeline):
    def item_completed(self, results, item, info):
        for ok, values in results:
            image_path = values['path']
            if image_path:
                item['image_list_path'] = image_path
            else:
                item['image_list_path'] = 0
            return item


# 自定义SQL
class NEWinsertsqlPipline(object):
    def __init__(self):
        self.db = pymysql.connect(host='192.168.7.126', port=3336, db='TD_OA', user='myoa999', password='myoa999')
        self.cur = self.db.cursor()

    def process_item(self, item, spider):
        insert_sql = '''insert into 
        ajobler(id,title,datelist,category,mainbody,zang,sc,pl,image_list_url,image_list_path) 
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ON DUPLICATE KEY UPDATE zang=VALUES(zang)
        '''
        parmer = (
        item['image_list_id'], item['title'], item['datelist'], item['category'], item['mainbody'], item['zang'],
        item['sc'], item['pl'], item['image_list_url'], item['image_list_path'])
        self.cur.execute(insert_sql, parmer)
        print('ok')
        self.db.commit()
        return item

    def close_sql(self):
        self.db.close()


# 内置SQL
class NkinsertsqlPipline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbpool = adbapi.ConnectionPool("pymysql", host=settings["MYSQL_HOST"], port=settings["MYSQL_PORT"],
            user=settings["MYSQL_USER"], password=settings["MYSQL_PASSWORD"], db=settings["MYSQL_DBNAME"],
                                       # charset='utf8',
                                       # use_unicode=True,
            cursorclass=pymysql.cursors.DictCursor)
        return cls(dbpool)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.insert_handle, item)
        query.addErrback(self.handle_error)

    def handle_error(self, Failure):
        print(Failure)

    def insert_handle(self, cursor, item):
        insert_sql = '''insert into 
                ajobler(id,title,datelist,category,mainbody,zang,sc,pl,image_list_url,image_list_path) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                ON DUPLICATE KEY UPDATE zang=VALUES(zang)
                '''  # ON DUPLICATE KEY UPDATE zang=VALUES(zang)
        parmer = (
            item['image_list_id'], item['title'], item['datelist'], item['category'], item['mainbody'], item['zang'],
            item['sc'], item['pl'], item['image_list_url'], item['image_list_path'])
        cursor.execute(insert_sql, parmer)


from elasticsearch_dsl import DocType, Date, Integer, Keyword, Text, connections, Completion

es = connections.connections.create_connection(ArticleType._doc_type.using)


def gen_suggest(index, info_tuple):
    # 根据字符串生成所搜建议数据
    # python重要性titel:10
    used_words = set()
    suggest = []
    for text, weight in info_tuple:
        if text:
            # 调用es的analyze借口分析字符串
            words = es.indices.analyze(index=index, analyzer="ik_max_word", params={'filter': ['lowercase']}, body=text)
            anylzed_words = set([r['token'] for r in words['tokens'] if len(r["token"]) > 1])
            new_words = anylzed_words - used_words
        else:
            new_words = set()
        if new_words:
            suggest.append({"input": list(new_words), "weight": weight})
    return suggest


class ElasicsearchPipline(object):
    def process_item(self, item, spider):
        article = ArticleType()
        article.title = item['title']
        article.datalist = item['datelist']
        article.dianzang = item['zang']
        article.shouchang = item['sc']
        article.pinglunshu = item['pl']
        article.suggest = gen_suggest(article._doc_type.index,
                                      ((article.title, 10), (article.dianzang, 7)))  # 用来控制模糊搜索设置权重weight
        article.save()
        return item
