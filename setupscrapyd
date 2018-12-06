1)pip install scrapyd
# 2)pip install scrapyd-client
# 3)在虚拟环境内的\Scripts文件夹内添加scrapy-deploy.bat文档
# 信息如下：
# @echo off
# "D:\Evns\py3scrapy\Scripts\python.exe" "D:\Evns\py3scrapy\Scripts\scrapyd-deploy" %1 %2 %3 %4 %5 %6 %7 %8 %9
# 测试方法(py3scrapy) D:\jobber>scrapyd-deploy -l）
# 4)在scrapy项目内添加路径设定settings
# BASE_DIR=os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
# sys.path.insert(0,os.path.join(BASE_DIR,'jobber'))
# 
# 5)在对应的虚拟环境内并进入项目的根目录：
# 1.0：首先需要在scrapy.cfg设定信息
# [settings]
# default = jobber.settings
# 
# [deploy:localhost]（原始内是没有:localhost）
# url = http://localhost:6800/（原来是用#号注释掉，把#去掉即可）
# project = jobber
# 
# 信息：(py3scrapy) D:\jobber>scrapyd-deploy localhost -p jobber
# 创建一个egg项目文档
# 
# 6） 安装curl
# https://curl.haxx.se/windows/dl-7.62.0_1/openssl-1.1.1a_1-win32-mingw.zip
# 配置环境：
# 新建：CURL_HOME  ，解压上面下载文件路径
# path:%CURL_HOME%\bin
# 测试方法：curl --help没有报错代表正常安装了
# 
# 7)启动爬虫方法
# curl http://localhost:6800/schedule.json -d project=localhost -d spider=jobber
# PROJECT_NAME填入你爬虫工程的名字#爬虫主目录的名称
# SPIDER_NAME填入你爬虫的名字#爬虫的spiders名称
# =========================================================================
# 把scrapyd放置到其他执行文件中方法
# 新建一个文件夹，在新文件内添加scrapyd
# 在cmd找到对应的目录，启动scrapyd。
