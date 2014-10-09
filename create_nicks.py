from weibocrawler import dboperator

def create_nicks(file_name, dbo):
	fr = open(file_name, "r", encoding = "utf-8")
	for l in fr.readlines():
		uid = l.strip()
		href = "http://weibo.com/u/" + str(uid)
		dbo.coll.update({'href': href},{'$set': {'href': href}}, upsert = True)


'''
This function will crawler user page read from collection Nicks and insert them into collection UserHomePages from MongoDB.
'''
def main():
	from weibocrawler.config import getconfig
	cfg = getconfig()
	# 把文件中的userid导入数据库
	# file_name = "iter02/uid_iter02_10_06"
	file_name = "iter03/uid_iter03_10_07"

	Collection_Nicks = cfg['Collections']['Nicks'] #"Nicks_iter02_10_06"# get href	
	dbo = dboperator.Dboperator(collname = Collection_Nicks)
	create_nicks(file_name, dbo)
	dbo.connclose()
main()

