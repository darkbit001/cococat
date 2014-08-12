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
def relation_parser(htmlStr):
	user_dict = {}
	user_dict['follower_num'] = -1
	user_dict['followee_num'] = -1
	user_dict['weibo_num'] = -1
	pattern_follower_num = re.compile(r'<strong node-type=\\"fans\\">(.+?)<\\/strong>\\r\\n\\t\\t\\t<span>粉丝<\\/span>')
	pattern_followee_num = re.compile(r'<strong node-type=\\"follow\\">(.+?)<\\/strong>\\r\\n\\t\\t\\t<span>关注 <\\/span>')
	pattern_weibo_num = re.compile(r'<strong node-type=\\"weibo\\">(.+?)<\\/strong>\\r\\n\\t\\t\\t<span>微博<\\/span>')
	if pattern_follower_num.search(html_str) != None:
		user_dict['follower_num'] = pattern_follower_num.findall(html_str)[0]
	if pattern_followee_num.search(html_str) != None:
		user_dict['followee_num'] = pattern_followee_num.findall(html_str)[0]
	if pattern_weibo_num.search(html_str) != None:
		user_dict['weibo_num'] = pattern_weibo_num.findall(html_str)[0]
	return user_dict
	
def parse_user_relation(dbo_userpages):
	cursor = dbo_userpages.coll.findOne({}, {'htmlStr': 1})
	for c in cursor:
		_id = c['_id']
		htmlStr = c['htmlStr']
		ud = relation_parser(htmlStr)
		follower_num = ud['follower_num']
		followee_num = ud['follower_num']
		weibo_num = ud['weibo_num']
		print(follower_num)
		print(followee_num)
		print(weibo_num)
		#dbo_userpages.coll.update({'_id': _id} ,{'$set': {'followerNum': follower_num, 'followeeNum': followee_num, 'weiboNum': weibo_num} }, multi = True)
	return
def main():
	dbo = dboperator.Dboperator(collname = 'UserHomePages')
	parse_user_base_infos(dbo)
	parse_user_relation(dbo)
	dbo.connclose()

main()