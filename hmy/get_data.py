import urllib.request
import urllib
import re
import json
from bs4 import BeautifulSoup
import requests
from django.http import HttpResponse
from Girls.models import JdProductParfum,JdHkProductParfume,JdHkProductFragrantBodyMilk,JdProductFragrantBodyMilk,JdHkProductSolidPerfume,JdProductSolidPerfume,JdHkProductCologne,JdProductCologne
#-*- coding:utf-8 -*-
import os

def jd_price(url):
    sku=url.split('/')[-1].strip(".html")
    #print(sku)
    price_url = "https://p.3.cn/prices/mgets?skuIds=J_" + sku
    req = urllib.request.Request(price_url)
    response = urllib.request.urlopen(req)
    #print(response)
    content = response.read().decode("ascii")
    #print(content)
    content=eval(content)
    #print(content)
    return content

def jd_detail(url):
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(response, "html.parser")
    if '全球购' in soup.find('div', {'class': 'dt cw-icon'}).text:
        detail=soup.find('div',{'id':'item-detail'}).findAll("li")
    else:
        detail=soup.find('div',{'class':'p-parameter'}).findAll("li")
    #print(detail)
    return detail

def get_picture(url):
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(response, "html.parser")
    p=soup.find('div', {'id':'spec-list'}).findAll("img")
    pic_list=[]
    for i in p:
        pic_list.append("https:"+i['src'])
    #print(pic_list)
    return pic_list


def crawlProductComment(url):
    #url="https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv1573&productId=1970372209&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1"
    html=urllib.request.urlopen(url).read().decode('gbk')
    index1=html.find("{")
    good=html.find("goodRateShow")
    poor=html.find("poorRateShow")
    goodrate=html[good+14:poor-2]
    jsondata=html[index1:-2]
    data=json.loads(jsondata)
    comments_list=[]
    for i in data['comments']:
        productId=i['referenceId']
        productName = i['referenceName']
        commentTime = i['creationTime']
        content = i['content']
        comments_list.append(content)

        # 输出商品评论关键信息
        '''
        print("商品编号:{}".format(productId))
        print("商品全名:{}".format(productName))
        print("用户评论时间:{}".format(commentTime))
        print("用户评论内容:{}".format(content))
        print("-----------------------------")
        '''
    return (goodrate,comments_list)

def get_product_info():
    os.environ.update({"DJANGO_SETTINGS_MODULE": "Girls.settings"})
    #香精列表的url(共三页)
    #url = r'https://coll.jd.com/list.html?sub=12478&page='
    #香体乳的url（共一页）
    #url=r'https://coll.jd.com/list.html?sub=12484&page='
    #固体香水(共一页)
    #url=r'https://coll.jd.com/list.html?sub=12479&page='
    #古龙水(共一页)
    url=r'https://coll.jd.com/list.html?sub=12485&page='
    for i in range(1, 2):
        print("第", i, "页")
        htmlpage = urllib.request.urlopen(url + str(i)).read()
        htmlpage = htmlpage.decode('UTF-8')
        soup = BeautifulSoup(htmlpage, "html.parser")# 实例化一个BeautifulSoup对象
        rep = soup.find("div", {'id': "plist"}).find("ul")
        rep=rep.findAll("li")
        for i in rep:
            address = r'https:' + i.find("div",{'class':'p-name'}).find('a')['href']
            data = {
                '链接':'',
                '品牌':'',
                '商品名称': '',
                '商品编号': '',
                '商品产地':'',
                '香调': '',
                '性别': '',
                '图片1': '',
                '图片2': '',
                '图片3': '',
                '图片4': '',
                '图片5': '',
                '店铺': '',
                '适用场景': '',
                '商品毛重': '',
                '净含量':'',
                '包装':'',
                '分类':'',
                '评论':'',
                '好评率':'',
                '价格':'',
                '抓取人': 'nicole',
                '一级目录':'美妆个护',
                '二级目录':'香水彩妆',
                '三级目录':'全身',
            }
            price=jd_price(address)
            data['价格']=price[0]['op']
            data['链接']=address
            detail = jd_detail(address)
            for i in detail:
                data[i.text.split('：')[0].strip()] = i.text.split('：')[1].strip()
            pic_list = get_picture(address)
            for i in range(0, len(pic_list)):
                data["图片" + str(i+1)] = pic_list[i]
            comment_address="https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv1573&productId="+data['商品编号']+"&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1"
            comments = crawlProductComment(comment_address)
            if comments[0]:
                data['好评率']=comments[0]
            else:
                data['好评率']=' '
            if comments[1]:
                data['评论']=comments[1]
            else:
                data['评论']=' '
            #print(data)
            #print('-----')
            if(data['品牌']):
                test=JdProductCologne(brand=data['品牌'],name=data['商品名称'],number=data['商品编号'],store=data['店铺'],
            perfume_note=data['香调'],packing=data['包装'],whole_kg=data['商品毛重'],gender=data['性别'],kg=data['净含量'],classify=data['分类'],good_for_who=data['适用场景'],comment_count=data['好评率'],
            img1_address=data['图片1'],img2_address=data['图片2'],img3_address=data['图片3'],img4_address=data['图片4'],img5_address=data['图片5'],comments=data['评论'],price=data['价格'],address=data['链接'],
                                     first_category=data['一级目录'],second_category=data['二级目录'],third_category=data['三级目录'],who_handly=data['抓取人'])
                test.save()
            else:
                test=JdHkProductCologne(name=data['商品名称'],number=data['商品编号'],store=data['店铺'],whole_kg=data['商品毛重'],
                                        produce_address=data['商品产地'],packing=data['包装'],perfume_note=data['香调'],kg=data['净含量'],classify=data['分类'],gender=data['性别'],
                                        good_for_who=data['适用场景'],price=data['价格'],comments=data['评论'],comment_count=data['好评率'],
                                        img1_address=data['图片1'],img2_address=data['图片2'],img3_address=data['图片3'],
                                        img4_address=data['图片4'],img5_address=data['图片5'],address=data['链接'],
                                        first_category=data['一级目录'], second_category=data['二级目录'],
                                        third_category=data['三级目录'], who_handly=data['抓取人']
                                        )
                test.save()
