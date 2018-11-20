
import re
import requests
from scrapy.selector import Selector
import pymysql
conn=pymysql.connect(host='****',port=***,db='***',user='***',password='***')
cur=conn.cursor()
class proxy_ip_list():
    def get_ip(self):
        url='http://www.xicidaili.com/nn/{}'
        headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36'}
        proxylist=[]
        for i in range(10):
            response=requests.get(url.format(i),headers=headers)
            selector=Selector(text = response.text)
            proxyip_list=selector.css("#ip_list tr")
            for proxyip_lists in proxyip_list[1:]:
                ip=proxyip_lists.xpath("./td/text()").extract()[0]
                port = proxyip_lists.xpath("./td/text()").extract()[1]
                leixing = proxyip_lists.xpath("./td/text()").extract()[4]
                speed_list = proxyip_lists.xpath("./td/div/@title").extract_first()
                if speed_list:
                    speed=float(speed_list.replace('秒',''))
                proxylist.append((ip,port,leixing,speed))
            for proxylistsa in proxylist:
                insert_sql='''
                insert into aproxyip(ip,port,leixing,speed,http) values (%s,%s,%s,%s,%s)
                '''
                parmer=proxylistsa[0],proxylistsa[1],proxylistsa[2],proxylistsa[3],'http'
                try:
                    cur.execute(insert_sql,parmer)
                    print('ok')
                    conn.commit()
                except:
                    pass

    def load_ip(self):
        select_sql='''select ip,port from aproxyip ORDER BY RAND() limit 1'''
        cur.execute(select_sql)
        for iplist in cur.fetchall():
            print(iplist[0],iplist[1])

if __name__ == '__main__':
    iplist=proxy_ip_list()
    #iplist.get_ip()
    iplist.load_ip()
