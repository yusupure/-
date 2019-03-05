# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import json
import datetime
from scrapy.loader import ItemLoader
from urllib.parse import urlencode
from allfullspidersearch.dataitem.zhihu.zhihu_items import zhihusjsonItemLoader, ZhihuItemLoader
from allfullspidersearch.dataitem.zhihu.zhihulogin.zhihusigin import zhihu_login
from allfullspidersearch.dataitem.zhihu.zhihulogin.zhihuupload import cookiesupload
from allfullspidersearch.dataset.dataset import MD5_sh


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    # start_urls = ['https://www.zhihu.com']
    #登录后获取登录页面动态的新闻信息
    #url = 'https://www.zhihu.com/api/v3/feed/topstory/recommend?session_token=e6cd631e8aed41f5a4a7e5be48a05cce&desktop=true&limit=7&action=down&after_id=5'
    #获取地址更新2019
    url='https://www.zhihu.com/api/v3/feed/topstory/recommend?session_token=b68e5e3d94ea0963738730ec6b0f443d&desktop=true&page_number=6&limit=6&action=down&after_id=3'
    def start_requests(self):
        # meta={'dont_redirect':True,'handle_httpstatus_list':[401,301]}取消SCRAPY内过滤错误返回CODE，取消重定向处理
        #读取页面URL地址，由于未知是否已经登录，强制通过meta取消重定向获取当前json信息，放到parse内执行
        yield Request(url = self.url,meta={'dont_redirect':True,'handle_httpstatus_list':[401,302]},cookies =cookiesupload(), callback = self.parse)

    def parse(self, response):
        #信息地址更2019
        url_detail='https://www.zhihu.com/api/v4/questions/{}/similar-questions?include=data%5B*%5D.answer_count%2Cauthor%2Cfollower_count&limit=5'
        #读取JSONlist 判断是否有存在code的这个字典key，判断当然登录cookies是否已经失效
        jsonlist = json.loads(response.text)
        if 'code' in jsonlist.keys():
            #如果失效就调用zhihu_login重新更新一次cookies
            yield Request(url = 'https://www.zhihu.com', callback = zhihu_login())  # 更新过期COOKIES
            #更新后的cookies后返回到开始访问重新访问链接
            yield Request(url=self.url,callback =self.start_requests)
        else:
            #判断当前是data代表cookies正常使用
            if 'data' in jsonlist.keys():
                #循环提档期data内存放的每一个信息的ID信息
                for jsonlists in jsonlist.get('data'):
                    try:
                        #获取ID
                        id=jsonlists['target']['question']['id']
                        #ID于当前地址进行组合获取新的地址
                        urldata='https://www.zhihu.com/question/{}'.format(id)
                        #组合的URL来提取到一下详细数据提取页面
                        #获取页面主题的信息
                        yield Request(url=urldata,callback = self.parer_deltie)
                        #回答的详细内容
                        yield Request(url_detail.format(id),callback = self.parer_deltie_long)
                    except:
                        pass
            # if 'paging' in jsonlist.keys() and jsonlist['paging']['is_end']==False:
            #     nextpage=jsonlist['paging']['next']
            #     yield Request(url=nextpage,callback = self.parse)

    def parer_deltie(self, response):#主题内的
        #调用SCRAPY内置方法itemloader传入ITEMS内的CLASS名称，把获取的数据往里面传入特定ITEM里面
        acritel_zhihu=ItemLoader(item = ZhihuItemLoader(),response=response)
        acritel_zhihu.add_value('zhihu_url_id',response.url)#访问的URL地址
        acritel_zhihu.add_css('zhihu_title','.QuestionHeader-title ::text')#标题
        acritel_zhihu.add_css('zhihu_commer','.QuestionHeader-Comment button::text')#评论数
        acritel_zhihu.add_css('zhihu_tags','.QuestionHeader-topics ::text')#主题上的分类
        acritel_zhihu.add_css('zhihu_itemInner',".NumberBoard-itemInner strong::attr(title)")#关注数据
        acritel_zhihu.add_css('zhihu_item', ".NumberBoard-itemInner strong::attr(title)")#被浏览数
        items=acritel_zhihu.load_item()
        return items

    def parer_deltie_long(self,reponse):
        jsonlist=json.loads(reponse.text)
        is_end=jsonlist['paging']['is_end']#获取当前是否最后一页获取为FALSE
        nextpage=jsonlist['paging']['next']#获取下一个动态获取的详细回答数
        if 'data' in jsonlist and jsonlist.keys():
            for jsonlists in jsonlist.get('data'):
                #第二种传入ITMES值方法直接调入对应需要传入的方法CLASS名称
                answer_item = zhihusjsonItemLoader()
                #部分字段缺失，视乎通过js无法获取原来数据
                answer_item["url_object_id"] = MD5_sh(jsonlists["url"])#对当前地址进行MD5编码，调用md5函数
                answer_item["answer_id"] = jsonlists["id"]#提取回复人ID
                answer_item["question_id"] = jsonlists["question"]["id"]#当前主题的ID值
                answer_item["author_id"] = jsonlists["author"]["id"] if "id" in jsonlists["author"] else None #判断当前ID值有可能为空所以如果为空就为NONE
                answer_item["author_name"] = jsonlists["author"]["name"] if "name" in jsonlists["author"] else None #回复人的名称

                answer_item["content"] = jsonlists["content"] if "content" in jsonlists else None #详细回复内容
                answer_item["praise_num"] = jsonlists["voteup_count"]#回复总数
                answer_item["comments_num"] = jsonlists["comment_count"]#回复条数
                answer_item["url"] = "https://www.zhihu.com/question/{0}/answer/{1}".format(jsonlists["question"]["id"],jsonlists["id"])#当前ID的和详细页面信息ID
                answer_item["update_time"] = jsonlists["updated_time"]#更新时间
                answer_item["crawl_time"] = datetime.datetime.now()#更新日期

                yield answer_item#返回所有数据会ITEMS里面


        # if not is_end:#如果为ture
        #     yield Request(nextpage,callback = self.parer_deltie_long)#获取的下一页地址，递归函数重新访问链接，循环处理
