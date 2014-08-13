#
# 1. Crawl the user timeline pages using the pageid get from collection UserHomePages
# 2. Insert the timeline pages into collection TimelinePages
#
# doufunao
# 2014-08-11
#

import weibocrawler
from weibocrawler import log
from weibocrawler import dboperator
from weibocrawler import weibo_struct
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

def get_domain(pageid, userid):
	return pageid.replace(userid, '')
	
def __crawl_each_timeline_page(http_request, para_dict):
	sleeptime = random.randint(3,8)
	log('Ready to get each json data. Just have a rest', 'sleeptime: ' + str(sleeptime))
	time.sleep(sleeptime)		
	json_urlstr = 'http://weibo.com/p/aj/mblog/mbloglist?domain=%(domain)s&pre_page=%(prePage)s&page=%(page)s&pagebar=%(pageBar)s&id=%(pageId)s' % (para_dict)
	jsonstr = http_request.get(json_urlstr)
	para_dict['pageUrl'] = json_urlstr
	para_dict['htmlStr'] = jsonstr
	return

def crawl_timeline_pages(http_request, userid, pageid, end_page_num):
	'''
	输入：获得cookie的request、pageId、end_page_num
	输出：此人的前五页timeline内容
	'''
	user_timeline_pages = []
	para_dict = {}
	para_dict['prePage'] = 0
	para_dict['page'] = 1 # page number
	para_dict['pageBar'] = 0 # section number
	para_dict['pageId'] = pageid
	para_dict['userId'] = userid
	para_dict['domain'] = get_domain(pageid, userid)
	for page in range(1, end_page_num):
		#url para : page_id = default, page = page, pre_page = 0, pagebar = 0
		para_dict['page'] = page
		para_dict['prePage'] = 0
		para_dict['pageBar'] = 0
		para_dict['crawlerTime'] = datetime.datetime.now().timestamp()
		__crawl_each_timeline_page(http_request, para_dict)
		user_timeline_pages.append(para_dict)
		#url para : page_id = default, page = page, pre_page = page, pagebar = 0
		para_dict['prePage'] = page
		para_dict['crawlerTime'] = datetime.datetime.now().timestamp()
		__crawl_each_timeline_page(http_request, para_dict)
		user_timeline_pages.append(para_dict)

		#url para : page_id = default, page = page, pre_page = page, pagebar = 1
		para_dict['pageBar'] = 1
		para_dict['crawlerTime'] = datetime.datetime.now().timestamp()
		__crawl_each_timeline_page(http_request, para_dict)
		#log('Url para','Page: ' + str(page) + ' len(jsondata[\'timeline_page\']) : ' + str(len(jsondata['timeline_page'])))
		user_timeline_pages.append(para_dict)

	return user_timeline_pages
def cal_page_num(weibonum, page_num_upper_bound):
	end_page_num = math.ceil(int(weibonum) / 45) + 1
	if end_page_num > page_num_upper_bound:
		end_page_num = page_num_upper_bound + 1
	return end_page_num

def get_user_timeline_pages(http_request, dbo_userpages, dbo_timelinepages, end_page_num = 10):
	dbo1 = dbo_userpages
	dbo2 = dbo_timelinepages
	pid_cursor = dbo1.coll.find({},{'timelineCrawled': 1, 'pageId': 1, 'userId': 1, 'weiboNum': 1})
	timebatch = datetime.datetime.now().timestamp()
	for user in pid_cursor:
		_id = user['_id']
		userid = user['userId']
		pageid = user['pageId']
		# print(userid)
		# print(user.get('weiboNum', -1))
		# return
		weibonum = int(user.get('weiboNum', -1))
		crawled = int(user.get('timelineCrawled', 0))
		if crawled == 1:
			continue
		if pageid == -1 or pageid == '':
			continue
		if weibonum == -1:
			continue
		tlp = weibo_struct.TimelinePage(userid = userid, pageid = pageid)
		end_page_num = cal_page_num(weibonum, 10) # get the first 10 timeline page
		user_timeline_pages = crawl_timeline_pages(http_request, userid, pageid, end_page_num)
		for timeline in user_timeline_pages:
			tlp.page = timeline['page']
			tlp.pagebar = timeline['pageBar']
			tlp.prepage = timeline['prePage']
			tlp.pageurl = timeline['pageUrl']
			tlp.htmlstr = timeline['htmlStr']
			tlp.crawlertime = timeline['crawlerTime']
			timelinedict = tlp.getdict()
			timelinedict['timeBatch'] = timebatch
			timelinedict['userHomePageId'] = _id
			dbo2.coll.insert(timelinedict)
			dbo1.coll.update({'userid': userid} ,{'$set': {'timelineCrawled': 1 } }, multi = True)
			del timelinedict
		log('get_user_timeline_pages', 'userid: ' + str(userid) + 'pageid: ' + str(pageid))

def main():
	http_request = get_request()
	dbo1 = dboperator.Dboperator(collname = 'UserHomePages')
	dbo2 = dboperator.Dboperator(collname = 'UserTimelinePages')
	get_user_timeline_pages(http_request, dbo1, dbo2, end_page_num = 10)
	dbo1.connclose()
	dbo2.connclose()
main()