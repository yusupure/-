#elasticsearch_dsl 5.1版本
from elasticsearch_dsl import DocType, Date, Integer, Keyword, Text, connections,Completion
from datetime import datetime
connections.connections.create_connection(hosts=['127.0.0.1'])

from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer
#声明一个转换防止suggest执行init出现报错
class CustomAnalyzer(_CustomAnalyzer):
    def get_analysis_definition(self):
        return {}
#filter的大小写转换
ik_analyzer=CustomAnalyzer("ik_max_word",filter=["lowercase"])

class ArticleType(DocType):
    suggest=Completion(analyzer=ik_analyzer)#因为会报错所以处理
    title=Text(analyzer="ik_max_word")
    datalist=Keyword()
    dianzang=Integer()
    shouchang=Integer()
    pinglunshu=Integer()
    #zhengwen=Keyword()
    #tag=Integer()

    class Meta:
        index='jobberly'
        doc_type="article"
