
#elasticsearch_dsl 5.1版本
from elasticsearch_dsl import DocType, Date, Integer, Keyword, Text, connections,Completion
from datetime import datetime
connections.connections.create_connection(hosts=['192.168.7.126'])

from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer
#声明一个转换防止suggest执行init出现报错
class CustomAnalyzer(_CustomAnalyzer):
    def get_analysis_definition(self):
        return {}
#filter的大小写转换
ik_analyzer=CustomAnalyzer("ik_max_word",filter=["lowercase"])

class ZhuhuArticleType(DocType):
    suggest=Completion(analyzer=ik_analyzer)#因为会报错所以处理
    zhihu_url_id = Keyword()
    zhihu_title = Text(analyzer="ik_max_word")
    zhihu_commer = Keyword()
    zhihu_tags = Text()
    zhihu_itemInner =Integer()
    zhihu_item =Integer()
    #zhengwen=Keyword()
    #tag=Integer()

    class Meta:
        index='zhihu'
        doc_type="article"

class ZhiHuAnswerIndex(DocType):
    suggest = Completion(analyzer=ik_analyzer)
    answer_id = Keyword()
    question_id = Keyword()
    author_id = Keyword()
    author_name = Keyword()
    content = Text(analyzer="ik_smart")
    praise_num = Integer()
    comments_num = Integer()
    url = Keyword()
    #create_time = Date()
    #update_time = Date()
    #crawl_time = Date()

    class Meta:
        index = 'zhihu_answer'
        doc_type = "article"

