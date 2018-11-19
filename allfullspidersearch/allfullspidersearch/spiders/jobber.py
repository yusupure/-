# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.loader import ItemLoader

from allfullspidersearch.dataitem.jobboler.jobboler_item import jobboleSearchItem, NewjobboleItemload


class JobberSpider(scrapy.Spider):
    name = 'jobber'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        porurl=response.css("#archive .post-thumb a")
        for porurls  in porurl:
            image_url_list=porurls.css("img::attr(src)").extract_first()
            data_list=porurls.css("::attr(href)").extract_first()

            yield Request(data_list,meta = {"image_url_list":image_url_list},callback = self.deltie_parer)
        # nextpage=response.css("#archive .navigation .next::attr(href)").extract()
        # if nextpage:
        #     yield Request(nextpage,callback = self.parse)
        # else:
        #     pass

    def deltie_parer(self,response):
        image_url_list=response.meta.get("image_url_list","")
        jober_list=NewjobboleItemload(item = jobboleSearchItem(),response=response)
        jober_list.add_css("title",".entry-header h1::text")
        jober_list.add_css("datelist",".entry-meta p::text")
        jober_list.add_css("category",".entry-meta p a::text")
        jober_list.add_css("mainbody",".entry p::text")
        jober_list.add_css("zang",".post-adds h10::text")
        jober_list.add_css("sc",".post-adds .bookmark-btn ::text")
        jober_list.add_css("pl", ".post-adds a span::text")
        jober_list.add_value("image_list_url",image_url_list)
        jober_list.add_value("image_list_id", image_url_list)
        items=jober_list.load_item()
        yield items

