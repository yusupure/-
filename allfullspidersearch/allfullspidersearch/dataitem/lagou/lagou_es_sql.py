#elasticsearch_dsl 5.1版本
from elasticsearch_dsl import DocType, Date, Integer, Keyword, Text, connections,Completion
from datetime import datetime
connections.connections.create_connection(hosts=['192.168.7.126'])#外网连接

from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer
#声明一个转换防止suggest执行init出现报错
class CustomAnalyzer(_CustomAnalyzer):
    def get_analysis_definition(self):
        return {}
#filter的大小写转换
ik_analyzer=CustomAnalyzer("ik_max_word",filter=["lowercase"])

class ArticleType(DocType):
    suggest=Completion(analyzer=ik_analyzer)#因为会报错所以处理
    job_company = Text()
    job_position = Text(analyzer="ik_max_word")
    job_salary = Keyword()
    job_address = Text()
    job_experience =Keyword()
    job_education = Keyword()
    job_request = Keyword()
    job_detail = Keyword()
    publish_time = Keyword()
    work_addr = Text()
    fourSquare =Keyword()
    trend = Keyword()
    figure = Keyword()
    home = Keyword()

    class Meta:
        index='lagou'
        doc_type="article"


if __name__ == '__main__':
    ArticleType.init()
