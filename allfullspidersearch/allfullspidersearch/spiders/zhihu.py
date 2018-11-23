# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import json

from allfullspidersearch.dataitem.zhihu.zhihu_items import zhihunewItemloader, ZhihuItemLoader
from allfullspidersearch.dataitem.zhihu.zhihulogin.cookiesupload import cookiesupload
from allfullspidersearch.dataitem.zhihu.zhihulogin.zhihusigin import zhihu_login


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    # start_urls = ['https://www.zhihu.com']
    url = 'https://www.zhihu.com/api/v3/feed/topstory/recommend?session_token=e6cd631e8aed41f5a4a7e5be48a05cce&desktop=true&limit=7&action=down&after_id=5'

    def start_requests(self):
        # meta={'dont_redirect':True,'handle_httpstatus_list':[401,301]}取消SCRAPY内过滤错误返回CODE，取消重定向处理
        yield Request(url = self.url,meta={'dont_redirect':True,'handle_httpstatus_list':[401,301]},cookies =cookiesupload(), callback = self.parse)

    def parse(self, response):
        jsonlist = json.loads(response.text)
        if 'code' in jsonlist.keys():
            yield Request(url = 'https://www.zhihu.com', callback = zhihu_login())  # 更新过期COOKIES
            yield Request(url=self.url,callback =self.start_requests)
        else:
            if 'data' in jsonlist.keys():
                for jsonlists in jsonlist.get('data'):
                    try:
                        id=jsonlists['target']['question']['id']
                        urldata='https://www.zhihu.com/question/{}'.format(id)
                        yield Request(url='https://www.zhihu.com/question/27182640',callback = self.parer_deltie)
                    except:
                        pass
            # if 'paging' in jsonlist.keys() and jsonlist['paging']['is_end']==False:
            #     nextpage=jsonlist['paging']['next']
            #     yield Request(url=nextpage,callback = self.parse)

    def parer_deltie(self, response):
        acritel_zhihu=zhihunewItemloader(item = ZhihuItemLoader(),response=response)
        acritel_zhihu.add_value('zhihu_url_id',response.url)
        acritel_zhihu.add_css('zhihu_title','.QuestionHeader-title ::text')
        acritel_zhihu.add_css('zhihu_commer','.QuestionHeader-Comment button::text')
        acritel_zhihu.add_css('zhihu_tags','.QuestionHeader-topics ::text')
        acritel_zhihu.add_css('zhihu_itemInner',".NumberBoard-itemInner strong::attr(title)")
        #acritel_zhihu.add_xpath('zhihu_item',"button .NumberBoard-itemInner strong::attr(title)")
        #acritel_zhihu.add_css('zhihu_headerText','')
        #acritel_zhihu.add_css('zhihu_unescapable','')
        items=acritel_zhihu.load_item()
        return items
