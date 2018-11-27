import scrapy
from elasticsearch_dsl import connections
import datetime

from w3lib.html import remove_tags

from allfullspidersearch.dataitem.zhihu.zhihu_es_sql import ZhuhuArticleType, ZhiHuAnswerIndex
from allfullspidersearch.dataset.dataset import MD5_sh
import re

from allfullspidersearch.settings import SQL_DATETIME_FORMAT,SQL_DATE_FORMAT

es = connections.connections.create_connection(ZhuhuArticleType._doc_type.using, hosts = '192.168.7.126')

class ZhihuItemLoader(scrapy.Item):
    zhihu_url_id=scrapy.Field()#Id
    zhihu_title=scrapy.Field()#标题
    zhihu_commer=scrapy.Field()#评论数
    zhihu_tags=scrapy.Field()#标识
    zhihu_itemInner=scrapy.Field()#关注人
    zhihu_item=scrapy.Field()#浏览次数

    def clean_data(self):
        self['zhihu_url_id'] = MD5_sh(self['zhihu_url_id'][0])
        self['zhihu_title'] = self['zhihu_title'][0]  # 标题
        self['zhihu_commer'] =int(re.findall(r'(\d+).*',self['zhihu_commer'][0],re.S)[0])# 评论数
        self['zhihu_tags'] = ','.join(self['zhihu_tags'])# 标识
        self['zhihu_itemInner'] = int(self['zhihu_itemInner'][0])  # 关注人
        self['zhihu_item'] = int(self['zhihu_item'][1])  # 浏览次数

    def save_sql_es(self):
        insert_sql="""
            insert into zhihunew(zhihu_url_id,zhihu_title,zhihu_commer,zhihu_tags,zhihu_itemInner,zhihu_item)
            values (%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE zhihu_commer=VALUES(zhihu_commer),
            zhihu_itemInner=VALUES(zhihu_itemInner),zhihu_item=VALUES(zhihu_item)
        """
        self.clean_data()
        parmer=(self['zhihu_url_id'],self['zhihu_title'],self['zhihu_commer'],self['zhihu_tags'],
                self['zhihu_itemInner'],self['zhihu_item'])
        return (insert_sql,parmer)

    def gen_suggest(self,index, info_tuple):
        # 根据字符串生成所搜建议数据
        # python重要性titel:10
        used_words = set()
        suggest = []
        for text, weight in info_tuple:
            if text:
                # 调用es的analyze借口分析字符串
                words = es.indices.analyze(index = index, analyzer = "ik_max_word", params = {'filter': ['lowercase']},
                                           body = text)
                anylzed_words = set([r['token'] for r in words['tokens'] if len(r["token"]) > 1])
                new_words = anylzed_words - used_words
            else:
                new_words = set()
            if new_words:
                suggest.append({"input": list(new_words), "weight": weight})
        return suggest


    def elasticsearch_es_sql(self):
        self.clean_data()
        Article=ZhuhuArticleType()
        Article.zhihu_url_id=self['zhihu_url_id']
        Article.zhihu_title=self['zhihu_title']
        Article.zhihu_commer=self['zhihu_commer']
        Article.zhihu_tags=self['zhihu_tags']
        Article.zhihu_itemInner=self['zhihu_itemInner']
        Article.zhihu_item=self['zhihu_item']
        Article.suggest=self.gen_suggest(ZhuhuArticleType._doc_type.index,((Article.zhihu_title,10),(Article.zhihu_item,7)))
        Article.save()



class zhihusjsonItemLoader(scrapy.Item):
    url_object_id = scrapy.Field()
    answer_id = scrapy.Field()
    question_id = scrapy.Field()
    author_id = scrapy.Field()
    author_name = scrapy.Field()
    content = scrapy.Field()
    praise_num = scrapy.Field()
    comments_num = scrapy.Field()
    url = scrapy.Field()
    update_time = scrapy.Field()
    crawl_time = scrapy.Field()

    def clean_data(self):
        #self["create_time"] = datetime.datetime.fromtimestamp(self["create_time"]).strftime(SQL_DATE_FORMAT)
        #self["update_time"] = datetime.datetime.fromtimestamp(self["update_time"]).strftime(SQL_DATE_FORMAT)
        self["crawl_time"] = self["crawl_time"].strftime(SQL_DATE_FORMAT)
        self["content"] = remove_tags(self["content"])

    def save_to_mysql(self):
        # 插入知乎answer表的sql语句
        insert_sql = """
                   insert into zhihu_answer(url_object_id, answer_id, question_id, author_id, author_name,
                   content, praise_num, comments_num,url,create_time,
                   update_time, crawl_time)
                   VALUES (%s, %s, %s, %s, %s,
                      %s, %s, %s, %s, %s,
                      %s, %s)
                     ON DUPLICATE KEY UPDATE
                     content=VALUES(content), comments_num=VALUES(comments_num), praise_num=VALUES(praise_num),
                     update_time=VALUES(update_time), author_name=VALUES(author_name)
               """
        self.clean_data()
        sql_params = (
            self["url_object_id"], self["answer_id"], self["question_id"], self["author_id"], self["author_name"],
            self["content"], self["praise_num"], self["comments_num"], self["url"], self["create_time"],
            self["update_time"], self["crawl_time"])

        return insert_sql, sql_params

    def gen_suggest(self,index, info_tuple):
        # 根据字符串生成所搜建议数据
        # python重要性titel:10
        used_words = set()
        suggest = []
        for text, weight in info_tuple:
            if text:
                # 调用es的analyze借口分析字符串
                words = es.indices.analyze(index = index, analyzer = "ik_max_word", params = {'filter': ['lowercase']},
                                           body = text)
                anylzed_words = set([r['token'] for r in words['tokens'] if len(r["token"]) > 1])
                new_words = anylzed_words - used_words
            else:
                new_words = set()
            if new_words:
                suggest.append({"input": list(new_words), "weight": weight})
        return suggest

    def elasticsearch_es_sql(self):
        self.clean_data()
        zhihu = ZhiHuAnswerIndex()

        zhihu.meta.id = self["url_object_id"]
        zhihu.answer_id = self["answer_id"]
        zhihu.question_id = self["question_id"]
        zhihu.author_id = self["author_id"]
        zhihu.author_name = self["author_name"]

        zhihu.content = self["content"]
        zhihu.praise_num = self["praise_num"]
        zhihu.comments_num = self["comments_num"]
        zhihu.url = self["url"]
        #zhihu.create_time = self["create_time"]

        #zhihu.update_time = self["update_time"]
        zhihu.crawl_time = self["crawl_time"]

        # 在保存数据时便传入suggest
        zhihu.suggest = self.gen_suggest(ZhuhuArticleType._doc_type.index,
                                          ((zhihu.author_name, 10), (zhihu.content, 7)))
        #real_time_count("zhihu_answer_count", ZHIHU_QUESTION_COUNT_INIT)
        zhihu.save()
