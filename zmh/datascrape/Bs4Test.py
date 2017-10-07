#!/usr/bin/python 
# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
#规范化html,包含缩进和自动闭合部分标签
#soup.prettify()
soup = BeautifulSoup('<a class="boldest">Extremely bold</a>', 'html.parser')

#规范化html,包含缩进和自动闭合部分标签
soup.prettify()

# tag标签使用
tag = soup.a
print(type(tag))
# <class 'bs4.element.Tag'>
print(tag['class'])
# ['boldest']
print(tag.attrs)
# {'class': ['boldest']}
print(tag.name)
# b
# tag的属性可以被修改
tag['class'] = 'newboldest'
tag['id'] = 1
print(tag)
# <b class="newboldest" id="1">Extremely bold</b>
# tag属性可以被删除
del tag['class']
del tag['id']
print(tag.get('class'))
# none

rel_soup = BeautifulSoup('<p>Back to the <a rel="index">homepage</a></p>', 'html.parser')
rel_soup.a['rel']
# ['index']
rel_soup.a['rel'] = ['index', 'contents']
print(rel_soup.p)
# <p>Back to the <a rel="index contents">homepage</a></p>

# BeautifulSoup对象表示的是一个文档的全部内容，其属性和方法调用如下
print(soup.name)
# [document]
