#!/usr/bin/python
# -*- coding:utf-8 -*-
# -*- coding:utf-8 -*-
import urllib.request
import urllib


# 返回http接口的返回值，为byte类型
def url_get_uniqueid(url):
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req)
    # 接口返回值
    res = response.read()
    return res

if __name__ == '__main__':
    print(int(url_get_uniqueid("http://192.168.0.130:8080/database/rest/ID/getId")))