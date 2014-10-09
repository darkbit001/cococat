import weibocrawler
from weibocrawler import log
from weibocrawler import dboperator
import time
import math
import random
import datetime
from convert_cookies import convert_cookies


def get_request(check_cookie_file = True):
	username = 'e1441430@drdrb.com'
	password = 'e1441430'
	if check_cookie_file == True:
		convert_cookies()
	login = weibocrawler.WeiboLogin(username, password)
	http_request = weibocrawler.WeiboHttpRequest(login)
	return http_request


def crawl_follow_page(http_request, para_dict, flag = 'follower'):
	'''
	输入的urlstr返回的值应为script脚本信息
	urlstr example:		
		followee list http://weibo.com/p/1005051330747684/follow?pids=Pl_Official_LeftHisRelation&page=1&ajaxpagelet=1
		follower list http://weibo.com/p/1005051330747684/follow?pids=Pl_Official_LeftHisRelation&page=1&ajaxpagelet=1&relate=fans	
	'''
	returndic = {}
	sleeptime = random.randint(5,10)
	log('get_user_following_html sleeptime', sleeptime)
	time.sleep(sleeptime)
	# url = ''
	if flag == 'follower':
		url = 'http://weibo.com/p/%(pageId)s/follow?pids=Pl_Official_LeftHisRelation&page=%(page)s&ajaxpagelet=1&relate=fans' % (para_dict)
	elif flag == 'followee':
		url = 'http://weibo.com/p/%(pageId)s/follow?pids=Pl_Official_LeftHisRelation&page=%(page)s&ajaxpagelet=1' % (para_dict)
	para_dict['crawlerTime'] = datetime.datetime.now().timestamp()
	htmlstr = http_request.get(url)
	para_dict['htmlStr'] = htmlstr
	para_dict['pageUrl'] = url
	returndic.update(para_dict)
	return returndic

def crawl_user_follow_pages(http_request, pageid, end_page_num, flag = 'follower'):
	followlist = []
	para_dict = {}
	para_dict['pageId'] = pageid
	for page in range(1, end_page_num):
		para_dict['page'] = page
		followlist.append(crawl_follow_page(http_request, para_dict, flag))
	return followlist

def cal_page_num(num):
	end_page_num = math.ceil(int(num) / 20) + 1
	if end_page_num > 10:
		end_page_num = 11
	return end_page_num

def get_users_follow_pages(http_request, dbo_userhomepages, dbo_relationpages, flag = 'follower'):
	'''one page one document'''
	dbo1 = dbo_userhomepages
	dbo2 = dbo_relationpages
	pid_cursor = dbo1.coll.find({}, {'followerCrawled': 1, 'followeeCrawled': 1, 'pageId': 1, 'userId': 1, 'followerNum': 1, 'followeeNum': 1}, timeout = False)
	# print(len(list(pid_cursor)))
	timebatch = datetime.datetime.now().timestamp()
	pid_list = list(pid_cursor)
	for user in pid_list:
		_id = user['_id']
		pageid = user['pageId']
		userid = user['userId']
		numflag = flag + 'Num'
		num = int(user.get(numflag, -1))
		carwlerflag = flag + 'Crawled'
		crawled = int(user.get(carwlerflag, 0))

		if pageid == -1:
			continue
		if num == -1:
			continue
		if crawled == 1:
			continue

		end_page_num = cal_page_num(num)
		followlist = crawl_user_follow_pages(http_request, pageid, end_page_num, flag)
		for f in followlist:
			newdic = {}
			newdic.update(f)
			newdic['userId'] = userid
			newdic['timeBatch'] = timebatch
			newdic['UserHomePageId'] = _id
			newdic['flag'] = flag
			dbo2.coll.insert(newdic)
			dbo1.coll.update({'userId': userid} ,{'$set': {str(carwlerflag): 1 } }, multi = True)
			del newdic
		log('got_users_follow_pages', 'userid: ' + str(userid) + ' pageid: ' + str(pageid) + ' flag: ' + flag)
	return

def main():
	'''
	This function will crawler user relationship page read from collection Nicks and insert them into collection UserHomePages from MongoDB.
	'''
	from weibocrawler.config import getconfig
	cfg = getconfig()
	Collection_UserHomePages = cfg['Collections']['UserHomePages']
	Collection_UserRelationPages = cfg['Collections']['UserRelationPages']
	
	# dbo1 = dboperator.Dboperator(collname = 'UserHomePages')
	# dbo2 = dboperator.Dboperator(collname = 'UserRelationPages')
	dbo1 = dboperator.Dboperator(collname = Collection_UserHomePages)
	dbo2 = dboperator.Dboperator(collname = Collection_UserRelationPages)
	http_request = get_request()	
	get_users_follow_pages(http_request, dbo1, dbo2, 'follower')
	get_users_follow_pages(http_request, dbo1, dbo2, 'followee')
	dbo1.connclose()
	dbo2.connclose()
# main()

