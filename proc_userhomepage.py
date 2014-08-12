#
# Parse the data which 'get_user_pages.py' crawled and is stored in collection UserHomePages.
# Upate collection UserHomePages with new parsed data.
# doufunao
#
# 2014-08-11

import re
from weibocrawler import dboperator

def userinfo_parser(html_str):
	user_dict = {}
	pattern_uid = re.compile(r'\[\'oid\'\]=\'(\d+?)\'')
	pattern_nickname = re.compile(r'\[\'onick\'\]=\'(.+?)\'')
	pattern_page_id = re.compile(r'\[\'page_id\'\]=\'(.+?)\'')
	
	if pattern_uid.search(html_str) != None:
		user_dict['user_id'] = pattern_uid.findall(html_str)[0]
		user_dict['screen_name'] = pattern_nickname.findall(html_str)[0]
		user_dict['page_id'] = pattern_page_id.findall(html_str)[0]
	else:
		user_dict['user_id'] = -1
		user_dict['screen_name'] = "None"
		user_dict['page_id'] = -1
	
	return user_dict
def parse_user_base_infos(dbo_userpages):
	cursor = dbo_userpages.coll.find({}, {'htmlStr': 1, 'pageUrl': 1})
	for c in cursor:
		_id = c['_id']
		htmlStr = c['htmlStr']
		pageUrl = c['pageUrl']
		ud = userinfo_parser(htmlStr)
		nickName = ud['screen_name']
		pageId = ud['page_id']
		userId = ud['user_id']
		dbo_userpages.coll.update({'_id': _id} ,{'$set': {'userId': userId, 'pageId': pageId, 'nickName': nickName} }, multi = True)
		if pageId == -1:
			print(pageUrl)
	return
def parse_user_relation(dbo_userpages):
	cursor = dbo_userpages.coll.find({}, {'htmlStr': 1, 'pageUrl': 1})
	for c in cursor:
		_id = c['_id']
	pass
def main():
	dbo = dboperator.Dboperator(collname = 'UserHomePages')
	parse_user_base_infos(dbo)
	dbo.connclose()

main()