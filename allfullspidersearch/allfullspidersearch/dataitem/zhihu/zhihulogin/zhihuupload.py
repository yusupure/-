import json
import os
def cookiesupload():
    jsonlist=open('zhihucookies.json','r')
    cookiesjson={}
    jsonload=json.load(jsonlist)
    for jsonlists in jsonload:
        name=jsonlists['name']
        value=jsonlists['value']
        cookiesjson.setdefault(name,value)
    return cookiesjson

if __name__ == '__main__':
    cookiesupload()

