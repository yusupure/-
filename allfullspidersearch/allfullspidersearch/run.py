#实现同时执行多个spiders内项目，不是同步执行是分布顺序方式执行
# 通过CrawlerProcess同时运行几个spider
from scrapy.crawler import CrawlerProcess
# 导入获取项目配置的模块
from scrapy.utils.project import get_project_settings
# 导入蜘蛛模块(即自己创建的spider)
from allfullspidersearch.spiders.jobber import JobberSpider
from allfullspidersearch.spiders.lagou import LagouSpider

# get_project_settings() 必须得有，不然"HTTP status code is not handled or not allowed"
process = CrawlerProcess(get_project_settings())
process.crawl(JobberSpider)
process.crawl(LagouSpider)# 注意引入
#process.crawl(Test2Spider) # 注意引入
process.start()
