#
# dboperator.py
#
# Author: doufunao
#
#
from pymongo import MongoClient
# from config import getconfig
from weibocrawler.config import getconfig

class Dboperator:
	'''
	Link to database

	Usage:
		Demo:
		testlist={"author":"yeah2","lala":"heihei2"}
		dbo=Dboperator('timeline') 	 # Instantiating class
		dbo.insert(testlist) # insert an item into collection
		dbo.show()			 # print all the document in collection	

	'''
	cfg = getconfig()
	port = cfg['MongoDBConnection']['port'] # read mongodb connection port from config file
	host = cfg['MongoDBConnection']['host'] # read mongodb connection host from config file
	db = cfg['MongoDBConnection']['db'] # read mongodb connection host from config file
	collname = 'weibo' #The default collection is weibo
	def __init__(self, collname = collname, dbname = db, host = host, port = int(port)):
		self.collname = collname
		self.connectdb(host, port, dbname)

	def connectdb(self, host, port, dbname):
		collname = self.collname		
		self.client = MongoClient(host = host, port = port)
		self.db = self.client[dbname]
		self.coll = self.db[collname]

	def insert(self,new_list):
		#insert an item
		#input:list
		#output:Objectid
		
		mongoid = self.coll.insert(new_list)
		#print('成功插入:', new_list)
		
		return mongoid

	def drop(self):
		mongoid = self.coll.drop()
		print(mongoid)

	def connclose(self):
		self.client.close()
	def show(self):
		print('Show all documents in collection',self.collname,':')
		for item in self.coll.find():
			print (item)
def test():
	db2 = Dboperator()
	db2.show()

# test()