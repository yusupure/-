#elasticsearch_dsl 5.1版本
from elasticsearch_dsl import DocType, Date, Integer, Keyword, Text, connections,Completion
from datetime import datetime
connections.connections.create_connection(hosts=['127.0.0.1'])
from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer
#声明sugest执行INIT出现报错行为
class CustomAnalyzer(_CustomAnalyzer):
    def get_analysis_definition(self):
        return {}
#对英文字母进行转换
ik_analyzer=CustomAnalyzer("ik_max_word",filter=["lowercase"])
#创建库表名称
class es_save_to(DocType):
    suggest = Completion(analyzer=ik_analyzer)  # 因为会报错所以处理
    title = Text(analyzer="ik_max_word")
    datalist = Keyword()
    dianzang = Integer()
    shouchang = Integer()
    pinglunshu = Integer()

    # zhengwen=Keyword()
    # tag=Integer()

    class Meta:
        index = 'jobberly'#库
        doc_type = "article"#表


if __name__ == '__main__':
    es_save_to.init()
