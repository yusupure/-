import re
import requests
from scrapy.selector import Selector
import pymysql
conn=pymysql.connect(host='127.0.0.1',port=3339,db='test',user='root',password='root')
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
                insert into proxyiplist(ip,port,niming,htp,speed) values (%s,%s,%s,%s,%s)
                '''
                parmer=proxylistsa[0],proxylistsa[1],proxylistsa[2],'http',proxylistsa[3]
                try:
                    cur.execute(insert_sql,parmer)
                    print('ok')
                    conn.commit()
                except:
                    pass

    def delete_ip(self,ip):
        delete_sql='''delete from proxyiplist where ip='{}' '''.format(ip)
        cur.execute(delete_sql)
        conn.commit()
        return True
    def check_ip(self,ip,port):
        iplist='http://{}:{}'.format(ip,port)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36'}
        try:
            proxy={
                'http':iplist,'https':iplist
            }
            reposon=requests.get('http://www.baidu.com',headers=headers,proxies=proxy,timeout=3)
        except Exception as e:
            print('代理IP失败')
            self.delete_ip(ip)
            return False
        else:
            code=reposon.status_code
            if code>=200 and code<300:
                print(iplist)
                return True
            else:
                print('代理IP失败2')
                self.delete_ip(ip)
                print(False)

    def load_ip(self):
        select_sql='''select ip,port from proxyiplist ORDER BY RAND() limit 1'''
        cur.execute(select_sql)
        for iplist in cur.fetchall():
            ip=str(iplist[0])
            port=str(iplist[1])
            just=self.check_ip(ip,port)
            if just:
                return 'http://{0}:{1}'.format(ip,port)
            else:
                return self.load_ip()

if __name__ == '__main__':
    iplist=proxy_ip_list()
    #iplist.get_ip()
    iplist.load_ip()
