import pymongo
from pymongo import MongoClient

class Dboperator:
	'''
	Link to database

	Usage:
		Demo:
		testlist={"author":"yeah2","lala":"heihei2"}
		dbo=dboperator() 	 # Instantiating class
		dbo.insert(testlist) # insert an item into collection
		dbo.show()			 # print all the document in collection	

	'''

	collname = 'weibo' #The default collection is weibo
	def __init__(self,collname):
		self.collname = collname
		self.connectdb()

	def connectdb(self):
		collname = self.collname		
		self.client = MongoClient()
		self.db = self.client.test
		self.coll = self.db[collname]

	def insert(self,new_list):
		#insert an item
		#input:list
		#output:Objectid
		
		mongoid = self.coll.insert(new_list)
		#print('成功插入:', new_list)
		
		return mongoid, new_list

	def drop(self):
		mongoid = self.coll.drop()
		print(mongoid)

	def show(self):
		print('Show all documents in collection',self.collname,':')
		for item in self.coll.find():
			print (item)