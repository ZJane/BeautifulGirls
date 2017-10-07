#!/usr/bin/python
# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import os

htmlfile = "item_11536082308.html"
if not os.path.exists(htmlfile):
    pass
with open(htmlfile,'rb') as file:
    htmlcontent = file.read()
htmlcontent = htmlcontent.decode('gbk','ignore')
# print(htmlcontent)

soup = BeautifulSoup(htmlcontent, 'html.parser')
# print(soup.prettify())
allclass = soup.find_all('class')
# print(soup.title)
# print(soup.find(id="parameter-brand"))
# divSoup = soup.find(id="parameter-brand")  #通过分析，发现规格参数所在部分id
# lis = divSoup.find_all('li')
# print(lis[0].getText())
# 商品介绍
divSoup = soup.find('div',class_="p-parameter")
print(divSoup)
lis=divSoup.find_all('li')
for li in lis:
    print(li.getText())
# 规格与包装
divSoup = soup.find('div',class_="Ptable-item")
print(divSoup)
# 商品描述
divSoup = soup.find('div',class_="sku-name")
product_decsription = divSoup.getText()
product_decsription = product_decsription.strip(" ").strip()
print(product_decsription)

# 图片
divSoup = soup.find('div', id ="spec-list").find('ul')
print(divSoup)
imgSoup = divSoup.find_all('li')
imgAddresses = []
for li in imgSoup:
    # print(li)
    imgsrc = li.find('img')['src']
    # print(imgsrc)
    imgAddresses.append(r'https:'+imgsrc)
print(imgAddresses)
