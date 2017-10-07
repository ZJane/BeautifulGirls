#!/usr/bin/python 
# -*- coding:utf-8 -*-
import  os
import  sys
import urllib.request
import urllib
import socket
import json
import re
from bs4 import BeautifulSoup



def gethtml(url,savefile):
    #定义http头部，很多网站对于你不携带User-Agent及Referer等情况，是不允许你爬取。
    #具体的http的头部有些啥信息，你可以看chrome，右键审查元素，点击network，点击其中一个链接，查看request header
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req).read()
    print(response)
    htmltemp = ""
    try:
        response = urllib.request.urlopen(req)
        htmltemp = response.read()
        # htmltemp = htmltemp.decode('utf-8')
    except Exception as e:
        print(e)
    try:
        with open(savefile, 'wb') as file_object:
            file_object.write(htmltemp)
            file_object.flush()
    except Exception as e:
        print(e)
    return htmltemp


def jd_price(url):
        sku = url.split('/')[-1].strip(".html")
        print(sku)
        price_url = "https://p.3.cn/prices/mgets?skuIds=J_" + sku
        #
        req = urllib.request.Request(price_url)
        response = urllib.request.urlopen(req)
        # content = response.read()
        price_json = json.loads(response.read().decode('utf-8'))
        # print(price_json[0].get('op'))
        return price_json[0].get('op')


def get_html_ids(url,htmlfile):
    # 有待改进
    if not os.path.exists(htmlfile):
        htmlcontent = gethtml(url,url.split('?')[1]+".html")
    with open(htmlfile,'rb') as file:
        htmlcontent = file.read()
    htmlcontent = htmlcontent.decode('utf-8')
    # print(htmlcontent)
    res=re.search(r'^(.*)var attrList(.*?) .*',htmlcontent,re.M | re.I)
    attrString = res.group().strip(';')
    attrString = attrString.split("=")[1]
    attrDict = eval(attrString)
    # print(type(attrDict))
    keys = attrDict.keys()
    # print(keys)
    return keys


def get_product_data(url,htmlfile):
    if not os.path.exists(htmlfile):
        htmlcontent = gethtml(url,htmlfile)
    with open(htmlfile,"rb") as file:
        htmlcontent = file.read()
    try:
        htmlcontent = htmlcontent.decode('utf_8','ignore')
        print(htmlcontent)
    except Exception as e:
        print(e)
if __name__=="__main__":
    # 获取ids
    listurl = "https://coll.jd.com/list.html?sub=12469"
    htmlfile = listurl.split('?')[1] + ".html"
    ids = get_html_ids(listurl,htmlfile)
    # 将ids转换成list
    idlist = []
    for url_id in ids:
        print(url_id)
        idlist.append(url_id)
    # 获取目标数据（循环中的内容）
    url = "https://item.jd.com/"+str(idlist[2])+".html"
    print(url)
    itemfile = url.split(r'/')[3]
    itemfile = 'item_'+itemfile
    print(itemfile)
    get_product_data(url,itemfile)

    # price = jd_price(url)
    # print(price)
    # 爬取多页数据的整体思路
    # 1，获得女士香水的商品列表的url，发现共125页，规则是https://coll.jd.com/list.html?sub=12469&page=%d&JL=6_0_0
    # d>=1,d<=125
    # 2，获得每件商品的商品详情页面的标识id，在每页的商品详情列表中，由attrList数组可得
    # 比如 var attrList = {1024127744:{"mcat3Id":11932,"soldOS":-1},234431:{"mcat3Id":11932,"soldOS":0},207991:{"mcat3Id":11932,"soldOS":0},1026011773:{"mcat3Id":11932,"soldOS":-1},2273740:{"mcat3Id":11932,"soldOS":0},402498:{"mcat3Id":11932,"soldOS":0},517756:{"mcat3Id":11932,"soldOS":0},1953350872:{"mcat3Id":11932,"soldOS":-1},1992431674:{"mcat3Id":11932,"soldOS":-1},323519:{"mcat3Id":11932,"soldOS":0},517849:{"mcat3Id":11932,"soldOS":0},1703479061:{"mcat3Id":11932,"soldOS":-1},517762:{"mcat3Id":11932,"soldOS":0},14186005469:{"mcat3Id":11932,"soldOS":-1},10794132592:{"mcat3Id":11932,"soldOS":-1},10702140306:{"mcat3Id":11932,"soldOS":-1},323522:{"mcat3Id":11932,"soldOS":0},1060064024:{"mcat3Id":11932,"soldOS":-1},10608533739:{"mcat3Id":11932,"soldOS":-1},1032300606:{"mcat3Id":11932,"soldOS":-1},10255149962:{"mcat3Id":11932,"soldOS":-1},1952907761:{"mcat3Id":11932,"soldOS":-1},2301179:{"mcat3Id":11932,"soldOS":0},1950211446:{"mcat3Id":11932,"soldOS":-1},2274867:{"mcat3Id":11932,"soldOS":0},207983:{"mcat3Id":11932,"soldOS":0},207886:{"mcat3Id":11932,"soldOS":0},323548:{"mcat3Id":11932,"soldOS":0},1514922277:{"mcat3Id":11932,"soldOS":-1},10608997927:{"mcat3Id":11932,"soldOS":-1},1968229496:{"mcat3Id":11932,"soldOS":-1},11339584810:{"mcat3Id":11932,"soldOS":-1},1989819231:{"mcat3Id":11932,"soldOS":-1},4648550:{"mcat3Id":11932,"soldOS":0},1011083447:{"mcat3Id":11932,"soldOS":-1},1373706217:{"mcat3Id":11932,"soldOS":-1},319826:{"mcat3Id":11932,"soldOS":0},14125277957:{"mcat3Id":11932,"soldOS":-1},1967497958:{"mcat3Id":11932,"soldOS":-1},1967388484:{"mcat3Id":11932,"soldOS":-1},11348824273:{"mcat3Id":11932,"soldOS":-1},502909:{"mcat3Id":11932,"soldOS":0},1985705530:{"mcat3Id":11932,"soldOS":-1},729738:{"mcat3Id":11932,"soldOS":0},10226007163:{"mcat3Id":11932,"soldOS":-1},11536082308:{"mcat3Id":11932,"soldOS":-1},14116595659:{"mcat3Id":11932,"soldOS":-1},10702140308:{"mcat3Id":11932,"soldOS":-1},11728032260:{"mcat3Id":11932,"soldOS":-1},10729079914:{"mcat3Id":11932,"soldOS":-1},1019729984:{"mcat3Id":11932,"soldOS":-1},1976838269:{"mcat3Id":11932,"soldOS":-1},517717:{"mcat3Id":11932,"soldOS":0},4384502:{"mcat3Id":11932,"soldOS":0},958435:{"mcat3Id":11932,"soldOS":0},265482:{"mcat3Id":11932,"soldOS":0},358203:{"mcat3Id":11932,"soldOS":0},1383257813:{"mcat3Id":11932,"soldOS":-1},958431:{"mcat3Id":11932,"soldOS":0},10983471236:{"mcat3Id":11932,"soldOS":-1}};
    # 3，获得每件商品的商品详情页面的url，如下：
    # https://item.jd.com/%d.html
    # 4，由url获得价格，（代码如上）
    # 5，由内容提取器获得商品介绍、规格、评价等
    # list_url = "https://coll.jd.com/list.html?sub=12469&page=3&JL=6_0_0"
    # id=1024127744
    # 测试获取价格的方法
    # jd_price("https://item.jd.com/1024127744.html")
    # socket.setdefaulttimeout(5)#设置全局超时时间
    # global judgeurl_all_lines#设置全局变量
    # #不存在文件就创建文件,该文件用于记录哪些url是爬取过的，如果临时中断了，可以直接重启脚本即可
    # if not os.path.exists("judgeurl.txt"):
    #         with open("judgeurl.txt","w") as judgefile:
    #                 judgefile.close()
    # #每次运行只在开始的时候读取一次，新产生的数据（已怕去过的url）也会保存到judgeurl.txt
    # with open("judgeurl.txt","r") as judgefile:
    #         judgeurl_all_lines = judgefile.readlines()
    # gotted_url = judgeurl_all_lines.sort()
    # print(gotted_url)
    # #排序，因为后面需要使用到二分查找，必须先排序
    # partlists = {'http://list.jd.com/list.html?cat=737,794,870': '空调',"d ":"df "}
    # partlistskeys = partlists.keys()
    #
    # print(partlists)