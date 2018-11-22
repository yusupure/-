from selenium import webdriver
import json
from time import sleep
import requests
import re
from PIL import Image
import base64
#自动浏览器模拟登陆获取当前登陆后COOKIES
#保存为json等待spider登陆调用登陆
def zhihu_login():
    url='https://www.zhihu.com/signup?next=%2F'
    headers={'user-agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36'}
    session=requests.Session()
    session.headers.clear()
    brown = webdriver.Chrome()
    brown.get(url)
    brown.find_element_by_css_selector(".SignContainer-switch span").click()
    sleep(3)
    brown.find_element_by_css_selector(".SignFlow-accountInput input").send_keys('13560414027')
    brown.find_element_by_css_selector(".SignFlow-password .SignFlowInput .Input-wrapper input").send_keys('abc.12345')
    sleep(5)
    try:
        img=brown.find_element_by_css_selector(".Captcha-chineseContainer img")
    except:
        img=brown.find_element_by_css_selector(".Captcha-englishImage .Captcha-englishContainer img").get_attribute('src')
        imagebase64=re.findall(r'base64,(.*)',img,re.S)[0]
        print(imagebase64)
        if imagebase64!='null':
            with open('yzm.jpg','wb')as fb:
                fb.write(base64.b64decode(imagebase64))
                fb.close()
            try:
                im=Image.open('yzm.jpg','r')
                im.show()
                im.close()
            except:
                pass
            yzm=input('输入验证码\n')
            sleep(5)
            brown.find_element_by_css_selector(".SignFlowInput .Input-wrapper input").send_keys(yzm)
    else:
        pass
    sleep(2)
    brown.find_element_by_xpath("//*[@id='root']/div/main/div/div/div/div[2]/div[1]/form/button").click()
    sleep(5)
    cookies=brown.get_cookies()
    brown.quit()
    with open('zhihucookies.json','w')as jn:
        json.dump(cookies,jn)


if __name__ == '__main__':
    zhihu_login()
