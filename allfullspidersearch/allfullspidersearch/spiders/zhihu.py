# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import json

from allfullspidersearch.dataitem.zhihu.zhihulogin.zhihusigin import zhihu_login


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    #start_urls = ['https://www.zhihu.com']
    url='https://www.zhihu.com/api/v3/feed/topstory/recommend?session_token=e6cd631e8aed41f5a4a7e5be48a05cce&desktop=true&limit=7&action=down&after_id=5'
    def start_requests(self):
        #meta={'dont_redirect':True,'handle_httpstatus_list':[401,301]}取消SCRAPY内过滤错误返回CODE，取消重定向处理
        yield Request(url=self.url,meta={'dont_redirect':True,'handle_httpstatus_list':[401,301]},callback=self.parse)
 
    def parse(self, response):
        jsonlist=json.loads(response.text)
        if 'code' in jsonlist.keys():
            yield Request(url='https://www.zhihu.com',callback=zhihu_login())#更新过期COOKIES
    def parer_deltie(self,response):
        pass
