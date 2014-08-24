#
# Parse the data which 'get_user_pages.py' crawled and is stored in collection UserHomePages.
# Upate collection UserHomePages with new parsed data.
# doufunao
#
# 2014-08-11

import re
from weibocrawler import dboperator
from weibocrawler import log

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

	log('parse_user_base_infos', 'Finished')

	return
def find_num(pattern, htmlstr):
	s1 = set(pattern.findall(htmlstr)[0])
	# print(pattern.findall(htmlstr)[0])
	s2 = set([''])
	num = list(s1-s2)
	return num[0]

def relation_parser(htmlStr):
	user_dict = {}
	user_dict['follower_num'] = -1
	user_dict['followee_num'] = -1
	user_dict['weibo_num'] = -1 
	pattern_follower_num = re.compile(r'<strong node-type=\\"fans\\">([\d\s]+?)<\\/strong>|<strong class=\\+"W_f20\\+">([\d\s]+?)<\\+/strong><span>粉丝<\\/span>|<strong class=\\+"\\+">([\d\s]+?)<\\+/strong><span>粉丝<\\+/span>')
	pattern_followee_num = re.compile(r'<strong node-type=\\"follow\\">([\d\s]+?)<\\/strong>|<strong class=\\+"W_f20\\+">([\d\s]+?)<\\+/strong><span>关注<\\/span>|<strong class=\\+"\\+">([\d\s]+?)<\\+/strong><span>关注<\\+/span>')
	pattern_weibo_num = re.compile(r'<strong node-type=\\"weibo\\">([\d\s]+?)<\\/strong>|<strong class=\\+"W_f20\\+">([\d\s]+?)<\\+/strong><span>微博<\\/span>|<strong class=\\+"\\+">([\d\s]+?)<\\+/strong><span>微博<\\+/span>')

	if pattern_follower_num.search(htmlStr) != None:
		user_dict['follower_num'] = find_num(pattern_follower_num, htmlStr)

	if pattern_followee_num.search(htmlStr) != None:
		user_dict['followee_num'] = find_num(pattern_followee_num, htmlStr)

	if pattern_weibo_num.search(htmlStr) != None:
		user_dict['weibo_num'] = find_num(pattern_weibo_num, htmlStr)
	
	return user_dict
	
def parse_user_relation(dbo_userpages):
	cursor = dbo_userpages.coll.find({}, {'htmlStr': 1, 'pageUrl': 1})
	for c in cursor:
		_id = c['_id']
		# pageurl = c['pageUrl']
		htmlstr = c['htmlStr']
		ud = relation_parser(htmlstr)
		follower_num = ud['follower_num']
		followee_num = ud['followee_num']
		weibo_num = ud['weibo_num']
		if follower_num == -1 or followee_num == -1 or weibo_num == -1:			
			# print(pageurl)
			# print(re.search('抱歉，', htmlstr))
			continue
		dbo_userpages.coll.update({'_id': _id} ,{'$set': {'followerNum': follower_num, 'followeeNum': followee_num, 'weiboNum': weibo_num} }, multi = True)
	log('parse_user_relation', 'Finished')
	return

def main():
	from weibocrawler.config import getconfig
	cfg = getconfig()
	Collection_UserHomePages = cfg['Collections']['UserHomePages']
	# dbo = dboperator.Dboperator(collname = 'UserHomePages')
	dbo = dboperator.Dboperator(collname = Collection_UserHomePages)	
	parse_user_base_infos(dbo)
	parse_user_relation(dbo)
	dbo.connclose()

main()