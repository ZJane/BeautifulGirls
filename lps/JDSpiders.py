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
		
		#print (self.html)
	
	
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
						if  500<=e.code and e.code < 600:  #5XX:当错误发生在服务端时
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






'''
#print(s.getHtml("https://coll.jd.com/list.html"))
#获取商品介绍
results = s.crawlProductDescription(["商品名称：","商品编号：","商品产地：","妆效：","分类：","功效：","颜色："])
#print(results)
#获取品牌
s.pro.brand = s.soup.find("ul",id="parameter-brand").a.string

#获取商品规格
results = s.crawlProductFormat(["保质期","适用人群"])
#print (results)

#获取商品价格
price = float(s.crawlJdPrice("1458843"))
print("商品价格："+str(price))

#获取商品的好评率和评论总数
url = "https://club.jd.com/comment/productCommentSummaries.action?referenceIds=1458843"
result = s.crawlProductComment(url)
print(result)

'''





'''
s = spider("https://coll.jd.com/list.html")
s.get_url("https://coll.jd.com/list.html?sub=12488")
'''
		
		
'''
s = spider("https://item.jd.com/1458843.html")


#品牌、商品名称、商品编号、商品毛重、商品产地、妆效、分类、功效、颜色
s.pro.brand = s.soup.find("ul",id="parameter-brand").a.string
element = s.soup.find("ul",class_="parameter2 p-parameter-list")  #Tag对象
s.pro.productName = s.crawlProductDescription(element,"商品名称：")
s.pro.id = s.crawlProductDescription(element,"商品编号：")
s.pro.height = s.crawlProductDescription(element,"商品毛重：")
s.pro.address = s.crawlProductDescription(element,"商品产地：")
s.pro.beautiEffect = s.crawlProductDescription(element,"妆效：")
s.pro.type = s.crawlProductDescription(element,"分类：")
s.pro.functionEffect = s.crawlProductDescription(element,"功效：")
s.pro.color = s.crawlProductDescription(element,"颜色：")

print("品牌：\t\t"+s.pro.brand)
print("商品名称：\t"+s.pro.productName)
print("商品编号：\t"+s.pro.id)
print("商品毛重：\t"+s.pro.height)
print("商品产地：\t"+s.pro.address)
print("妆效：\t\t"+s.pro.beautiEffect)
print("分类：\t\t"+s.pro.type)
print("功效：\t\t"+s.pro.functionEffect)
print("颜色：\t\t"+s.pro.color)


element = s.soup.find("div",class_="Ptable-item")
s.pro.liveLife = s.crawlProductFormat(element,"保质期")
s.pro.suitPeople = s.crawlProductFormat(element,"适用人群")
print ("保质期:\t\t"+s.pro.liveLife)
print ("适用人群:\t"+s.pro.suitPeople)



#获取商品全称
s.pro.totalName = "None"
element = s.soup.find("div",class_="sku-name",recursive=True)
for string in element.stripped_strings:
	s.pro.totalName = string
print("商品全称：\t"+s.pro.totalName)


#获取商品价格
s.pro.price = float(s.crawlJdPrice())
print ("商品价格：\t "+str(s.pro.price))

#获取评价总数和好评度
url = "https://club.jd.com/comment/productCommentSummaries.action?referenceIds=305551&callback=jQuery2442817&_=1507273894520"
result = s.crawlProductComment(url)
s.pro.commentNum = result["评价总数"]
s.pro.favourableComment = result["好评率"]

sql = save_mysql()
sql.save_product(s.pro)

'''




