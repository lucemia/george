# -*- coding: utf-8 -*-
import json
import json
#from models import Food, FoodDailyInfo
from itertools import groupby
from datetime import datetime


def urlget(url):
    try:
        from google.appengine.api import urlfetch
        resp = urlfetch.fetch(url, deadline=30)
        return resp.content
    except:
        import urllib2
        return urllib2.urlopen(url).read()

api = 'http://m.coa.gov.tw/OpenData/FarmTransData.aspx'
def get(date):
    item = {}
    url = api + "?StartDate={0}{1}&EndDate={0}{1}".format(date.year-1911, date.strftime(".%m.%d")) 
    content = urlget(url)
    items = sorted(json.loads(content), key=lambda x:x[u'作物名稱'])
    data = dict()
    for product in groupby(items, lambda x:x[u'作物名稱'].strip()):
        title, values = product
        total_price = 0
        total_amount = 0
        total_count = 0
        for value in values:
            total_price += float(value[u'平均價'])
            total_amount += float(value[u'交易量'])
            total_count += 1

        if not title:
            continue
        item['name'] = title
        item['wholesale_price'] = round(total_price/total_count)
        item['amount'] = total_amount
        item['date'] = date
        item['type'] = "vegetable"
        yield item






if __name__ == '__main__':
    for i in get(datetime(2014,6,1)):
        print i
