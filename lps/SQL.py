#encoding=UTF-8
import pymysql
import datetime  

class save_mysql:
	def __init__(self):
		self.user = "root"
		self.passwd = "1234"
		self.host = "39.108.185.66"
		self.database = "beautyGirls_database"
		db = None
	
	def get_connection(self):
		return pymysql.connect(self.host,self.user,self.passwd,self.database,charset="utf8")
	
	def save_product(self,sql):
		db = self.get_connection()
		#localtime = time.asctime(time.localtime(time.time()))

		#print(pro.color)
		cursor = db.cursor()		
		cursor.execute(sql)
		db.commit()
		
		
	
		