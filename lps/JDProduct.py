#encoding:UTF-8
import requests
import urllib
import re
from bs4 import BeautifulSoup
import json
from SQL import save_mysql
import Product
import datetime

class JDProduct:
	def __init__(self,url,id):
		self.url = url
		self.id = id
		self.scriptUrl = self.getScriptUrl()
		self.soup = self.getSoup()
		self.sql = save_mysql()
		self.pro = Product
		
	#下载网页
	def getHtml(self,url):
		html = None
		num_retries = 2
		if url is not None:  #检查url是否为空
			if self.isLegal(url):  #检查url是否合法
				while  num_retries > 0 :
					try:
						req = urllib.request.Request(url)
						req.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)') 
						html= urllib.request.urlopen(req).read()
						break
					except urllib.error.HTTPError as e:   #url请求出错
						print("Download error: ",e.reason)
						if  500<=e.code and e.code < 600:  #5XX:当错误发生在服务端时,重新发送2次
							num_retries = num_retries-1
						else :
							break
			else:
				print("The url is illegal.")
				exit()
		else:
			print("The url is None.")
			exit()
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
		
	#获取各种不同的script url
	def getScriptUrl(self):
		scriptUrl = ""
		if self.id is not None:
			scriptUrl = "https://club.jd.com/comment/productCommentSummaries.action?referenceIds="+self.id
		else:
			print("The id is None. ")
		return scriptUrl
		
	#获取商品介绍
	def crawlProductDescription(self,names=[]):
		if self.soup is None :
			self.soup = self.getSoup()
		results = {}
		try:
			strings = self.soup.find("ul",class_="parameter2 p-parameter-list").strings  
			#print (strings)
			if strings is not None:
				for string in strings:  #遍历每一个商品介绍内容
					if len(names)>0 :
						for index in range( len(names) ):
							if re.search( names[index],string):  #遍历每个要匹配的name
								results[ names[index] ] = string[len(names[index]):]
								del names[index]
								break
					else :
						break
				#将剩余的name设置为null
				for name in names:
					results[name] = "null"
			else:
				for name in names:
					results[name] = "null"
		except AttributeError as e:
			for name in names:
				results[name] = "null"
		return results
		
	#获取商品规格
	def crawlProductFormat(self,names=[]): 
		results = {}
		try :
			items = self.soup.find("div",class_="Ptable-item").find_all("dt")
			if items is not None :
				for item in items:
					for index in range(len(names)):
						if names[index] in item.string:
							results[names[index]] = item.next_sibling.string
							del names[index]
							break
				#将剩余的没有被匹配到的数据全部设置为null
				for name in names:   
					results[name] = "null"
			else:
				for name in names:
					results[name] = "null"
		except AttributeError as e:
			for name in names:
				results[name] = "null"
		return results

	#获取价格
	def crawlJdPrice(self):
		if self.id is not None:
			price_url = "https://p.3.cn/prices/mgets?skuIds=J_" + self.id
			result = ""
			content = json.loads( self.getHtml(price_url).decode("utf-8") )
			result = content[0]['op']
			'''
			try:
				req = urllib.request.Request(price_url)
				response = urllib.request.urlopen(req)
				content = json.loads(response.read().decode("utf-8"))
			except urllib.error.HTTPError as e :
				print(e.reason)
			'''
		else :
			print("The id is None.")
		return result
		
	#获取评论总数和好评率
	def crawlProductComment(self):
		#url = self.scriptUrl
		result = {}
		if self.scriptUrl is not None:
			try:
				#jsondata = urllib.request.urlopen(url).read().decode("gbk")  #返回的是json
				#jsondata = html[0:-2]
				jsondata = self.getHtml(self.scriptUrl).decode("gbk")
				data = json.loads(jsondata)
				commentNum = data['CommentsCount'][0]["CommentCountStr"]
				favourableComment = data['CommentsCount'][0]["GoodRateShow"]
				result["评价总数"] = commentNum
				result["好评率"] = favourableComment
			except urllib.error.URLError as e:
				print(e.reason)
		return result
	
	#获取商品品牌
	def crawlProductBrand(self):
		if self.soup is None:
			self.soup = self.getSoup()
		try:
			brand = self.soup.find("ul",id="parameter-brand").a.string
		except AttributeError as e:
			brand = "null"
		return brand
	
	#获取商品全称
	def crawlTotalName(self):
		data = ""
		if self.soup is None:
			self.soup = self.getSoup()
		element = self.soup.find("div",class_="sku-name",recursive=True)
		for string in element.stripped_strings:
			data = string
		#print("商品全称：\t"+data)
		return data
		
	def saveProduct(self):
		now = datetime.datetime.now()  
		insertStrings="insert into jd_products (first_category,second_category,third_category,\
		price,description,name,brand,produce_address,kg,\
		good_for_who,expiration_date,color,result_effectiveness,category,\
		makeup_effectiveness,who_handly,get_time,number,good_comment_percentage,comment_count) values \
		('美妆个户','香水彩妆','底妆','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(self.pro.price,self.pro.totalName,self.pro.productName,self.pro.brand,self.pro.address,self.pro.height,self.pro.suitPeople,self.pro.liveLife,self.pro.color,self.pro.beautiEffect,self.pro.type,self.pro.functionEffect,"Nancyse",now,self.pro.id,self.pro.favourableComment,self.pro.commentNum)
		self.sql.save_product(insertStrings)
				
	#获取京东商品的流程
	def crawlProductDetail(self):	
		
		#获取商品介绍
		results = self.crawlProductDescription(["商品名称：","商品毛重：","商品编号：","商品产地：","妆效：","分类：","功效：","颜色：","适合肤质："])
		self.pro.productName = results["商品名称："]
		self.pro.id = results["商品编号："]
		self.pro.address = results["商品产地："]
		self.pro.height = results["商品毛重："]
		self.pro.beautiEffect = results["妆效："]
		self.pro.type = results["分类："]
		self.pro.functionEffect = results["功效："]
		self.pro.color = results["颜色："]
		self.pro.suitPeople = results["适合肤质："]
		print(results)
		
		#获取商品品牌
		self.pro.brand = self.crawlProductBrand()
		print("品牌： ",self.pro.brand )
		
		#获取商品规格
		results = self.crawlProductFormat(["保质期"])
		self.pro.liveLife = results["保质期"]
		#self.pro.suitPeople = results["适合肤质"]
		print(results)
		
		#获取商品价格
		#price = float(s.crawlJdPrice("1458843"))
		self.pro.price = float(self.crawlJdPrice())
		print("商品价格："+str(self.pro.price))
		
		#获取商品的好评率和评论总数
		#url = "https://club.jd.com/comment/productCommentSummaries.action?referenceIds=1458843"
		results = self.crawlProductComment()
		self.pro.commentNum = results["评价总数"]
		self.pro.favourableComment = results["好评率"]
		print(results)
		
		#获取商品的全称
		self.pro.totalName = self.crawlTotalName()
		print("商品全称："+self.pro.totalName)
		
		#保存数据到数据库
		self.saveProduct()
		
	