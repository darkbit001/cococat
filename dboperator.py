import pymongo
from pymongo import MongoClient

class dboperator:
	'''
	Link to database

	Usage:
		Demo:
		testlist={"author":"yeah2","lala":"heihei2"}
		dbo=dboperator() 	 # Instantiating class
		dbo.insert(testlist) # insert an item into collection
		dbo.show()			 # print all the document in collection	

	'''
	def __init__(self):
		self.connectdb()

	def connectdb(self):		
		self.client = MongoClient()
		self.db = self.client.test
		self.coll = self.db.weibo

	def insert(self,new_list):
		#insert an item
		#input:list
		#output:Objectid
		mongoid = self.coll.insert(new_list)
		print('成功插入:', new_list)
		return mongoid, new_list

	def show(self):
		print('显示全部信息')
		for item in self.coll.find():
			print (item)

