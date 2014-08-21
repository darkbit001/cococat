from weibocrawler import dboperator
import json
import re
from bs4 import BeautifulSoup
# dbo = dboperator.Dboperator(collname = 'UserRelationPages')
# cursor = dbo.coll.find({'userId': '2920092522'}, {'htmlStr': 1}).limit(1)
# pattern = re.compile(r'<script>parent.FM.view\((.+)\)</script>')
# print(pattern.findall(cursor[0]['htmlStr'])[0])

dbo = dboperator.Dboperator(collname = 'UserTimelinePages')
cursor = dbo.coll.find({'userId': '2920092522'}, {'htmlStr': 1}).limit(1)
data = json.loads(cursor[0]['htmlStr'])['data']

soup = BeautifulSoup(data)
divs = soup.find_all('div', class_ = 'WB_feed_type SW_fun S_line2 ')
div = divs[3]
print(div)
mid = div.get('mid', -1)
print(mid)
tbinfo = div.get('tbinfo', -1)
print(tbinfo)
minfo = div.get('minfo', -1)
print(minfo)
isforward = div.get('isforward', -1)
print(isforward)
omid = div.get('omid', -1)
print(omid)