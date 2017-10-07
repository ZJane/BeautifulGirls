#encoding:UTF-8
import requests
import urllib
import re
from bs4 import BeautifulSoup
import json
#import Product
from JDProduct import JDProduct
from SQL import save_mysql

class JDSpiders:
	
	def __init__(self,url):
		self.url = url #下载的网址
		self.productUrls = set()	#所有的商品地址
		#self.searchPage = page+1  #查找的网页
		self.sql = save_mysql()
		self.soup = None #当前商品对应的BeautifulSoup 对象
	
	#下载网页
	def getHtml(self,url):
		html = None
		num_retries = 2
		if url is not None:  #检查url是否为空
			if self.isLegal(url):  #检查url是否合法
				while  num_retries > 0 :
					try:
						req = urllib.request.Request(url)
						req.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')  #添加头部
						html= urllib.request.urlopen(req).read()
						break
					except urllib.error.HTTPError as e:   #url请求出错
						print("Download error: ",e.reason)
						if  500<=e.code and e.code < 600:  #当发生5XX错误时，重复访问2次
							num_retries = num_retries-1
						else :
							break
			else:
				print("The url is illegal.")
		else:
			print("The url is None.")
		return html
	
	
	#检查url是否合法
	def isLegal(self,url):
		flag = False
		reg = "^https?:/{2}\w+(\.\w+)+([/?].*)?$"
		if re.match(reg,url):
			flag = True
		return flag
	
	#获取BeautifulSoup对象
	def getSoup(self):  
		if self.url is None:
			print("The url is None.")
			exit()  #中断
		html = self.getHtml(self.url)
		self.soup = BeautifulSoup(html,'lxml')
		return self.soup

	
	#获取各种不同的url
	def getProductUrls(self):
		'''
		html = self.getHtml(self.url)
		soup = BeautifulSoup(html,"lxml")
		'''
		if self.soup is None:
			self.soup = self.getSoup()
		elements = self.soup.find_all("div",class_="p-img")
		for element in elements:
			self.productUrls.add("https:"+element.a["href"])
		return self.productUrls

	#获取商品的id
	def getId(self,url):
		id = ""
		if url is not None :
			if self.isLegal(url):
				id = url.split("/")[-1].strip(".html")
			else :
				print("The url is illegal.")
		else:
			print("The url is None.")
		return id
	
	def main(self):
		
		urls = self.getProductUrls()  #获取所有的url
		#print(urls)
		print()
		for url in urls:
			id = self.getId(url)
			print(url+" "+id)
			jdProduct = JDProduct(url,id)
			jdProduct.crawlProductDetail()
		'''
		jdProduct = JDProduct(self.url,"305552")
		jdProduct.crawlProductDetail()
		'''
		
			
#s = JDSpiders("https://item.jd.com/305552.html")
s = JDSpiders("https://coll.jd.com/list.html?sub=12488")
s.main()

