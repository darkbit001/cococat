from weibocrawler import dboperator
import json
import re
from bs4 import BeautifulSoup
import functools
from pprint import pprint
# dbo = dboperator.Dboperator(collname = 'UserRelationPages')
# cursor = dbo.coll.find({'userId': '2920092522'}, {'htmlStr': 1}).limit(1)
# pattern = re.compile(r'<script>parent.FM.view\((.+)\)</script>')
# print(pattern.findall(cursor[0]['htmlStr'])[0])

# dbo = dboperator.Dboperator(collname = 'UserTimelinePages')
# cursor = dbo.coll.find({'userId': '2920092522'}, {'htmlStr': 1}).limit(1)
# data = json.loads(cursor[0]['htmlStr'])['data']

# soup = BeautifulSoup(data)
# divs = soup.find_all('div', class_ = 'WB_feed_type SW_fun S_line2 ')
# div = divs[3]
# print(div)
# mid = div.get('mid', -1)
# print(mid)
# tbinfo = div.get('tbinfo', -1)
# print(tbinfo)
# minfo = div.get('minfo', -1)
# print(minfo)
# isforward = div.get('isforward', -1)
# print(isforward)
# omid = div.get('omid', -1)
# print(omid)

from weibocrawler.config import getconfig
cfg = getconfig()
Collection_UserHomePages = cfg['Collections']['UserHomePages']
Collection_UserTimelines = cfg['Collections']['UserTimelines']
Collection_UserTimelinePages = cfg['Collections']['UserTimelinePages']
dbo3 = dboperator.Dboperator(collname = Collection_UserTimelinePages)
cursor = dbo3.coll.find({'userId': '1088602681'},{'userId': 1,'pageUrl': 1, '_id': 0})
pprint(list(cursor))

dbo = dboperator.Dboperator(collname = Collection_UserHomePages)
cursor = dbo.coll.find({},{'weiboNum': 1, 'userId': 1, '_id': 0})
pprint(list(cursor))
sum2 = 0
for c in cursor:
	if int(c['weiboNum']) > 400:
		sum2 += 400
		print(400)
	else:
		sum2 += int(c['weiboNum'])
		print(int(c['weiboNum']))
# sum1 = functools.reduce(lambda x,y : int(x) + int(y), [c['weiboNum'] for c in cursor])
print(sum2)

Collection_UserTimelines = cfg['Collections']['UserTimelines']
dbo2 =  dboperator.Dboperator(collname = Collection_UserTimelines)
cursor = dbo2.coll.find({},{'userId': 1, 'mId': 1})
sum3 = 0
dict1 = {}
for c in cursor:
	try:
		dict1[c['userId']] += 1
	except:
		dict1[c['userId']] = 1
pprint(dict1)
sum4 = functools.reduce(lambda x,y : int(x) + int(y), dict1.values())
print(sum4)
