# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import json

from scrapy.loader import ItemLoader
from urllib.parse import urlencode
from allfullspidersearch.dataitem.zhihu.zhihu_items import  ZhihuItemLoader

from allfullspidersearch.dataitem.zhihu.zhihulogin.zhihusigin import zhihu_login
from allfullspidersearch.dataitem.zhihu.zhihulogin.zhihuupload import cookiesupload


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    # start_urls = ['https://www.zhihu.com']
    url = 'https://www.zhihu.com/api/v3/feed/topstory/recommend?session_token=e6cd631e8aed41f5a4a7e5be48a05cce&desktop=true&limit=7&action=down&after_id=5'

    def start_requests(self):
        # meta={'dont_redirect':True,'handle_httpstatus_list':[401,301]}取消SCRAPY内过滤错误返回CODE，取消重定向处理
        yield Request(url = self.url,meta={'dont_redirect':True,'handle_httpstatus_list':[401,301]},cookies =cookiesupload(), callback = self.parse)

    def parse(self, response):
        url_detail='https://www.zhihu.com/api/v4/questions/{}/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit=5&offset=0&sort_by=default'

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
                        #yield Request(url_detail.format(id),meta={'userid':id},callback = self.parer_deltie_long)
                    except:
                        pass
            # if 'paging' in jsonlist.keys() and jsonlist['paging']['is_end']==False:
            #     nextpage=jsonlist['paging']['next']
            #     yield Request(url=nextpage,callback = self.parse)

    def parer_deltie(self, response):
        acritel_zhihu=ItemLoader(item = ZhihuItemLoader(),response=response)
        acritel_zhihu.add_value('zhihu_url_id',response.url)
        acritel_zhihu.add_css('zhihu_title','.QuestionHeader-title ::text')
        acritel_zhihu.add_css('zhihu_commer','.QuestionHeader-Comment button::text')
        acritel_zhihu.add_css('zhihu_tags','.QuestionHeader-topics ::text')
        acritel_zhihu.add_css('zhihu_itemInner',".NumberBoard-itemInner strong::attr(title)")
        acritel_zhihu.add_css('zhihu_item', ".NumberBoard-itemInner strong::attr(title)")
        acritel_zhihu.add_css('zhihu_detail', ".QuestionHeader-detail ")
        #acritel_zhihu.add_css('zhihu_headerText','')
        #acritel_zhihu.add_css('zhihu_unescapable','')
        items=acritel_zhihu.load_item()
        return items
    #
    # def parer_deltie_long(self,reponse):
    #     jsonlist=json.loads(reponse.text)
    #     for josnlists in jsonlist:
