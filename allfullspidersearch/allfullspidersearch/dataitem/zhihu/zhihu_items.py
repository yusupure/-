import scrapy
from elasticsearch_dsl import connections
from allfullspidersearch.dataitem.zhihu.zhihu_es_sql import ZhuhuArticleType
from allfullspidersearch.dataset.dataset import MD5_sh
import re
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



# class zhihusjsonItemLoader(scrapy.item):
#     zhihuid=scrapy.Field()
#     zhihu_content=scrapy.Field()
#     zhihu_title=scrapy.Field()
#     url_token=scrapy.Field()
#     follow_name=scrapy.Field()
