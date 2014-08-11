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
import random
import re
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

def __crawl_each_timeline_page(http_request, para_dict):
	sleeptime = random.randint(5,10)
	log('Ready to get each json data. Just have a rest', 'sleeptime: ' + str(sleeptime))
	time.sleep(sleeptime)		
	json_urlstr = 'http://weibo.com/p/aj/mblog/mbloglist?pre_page=%(prePage)s&page=%(page)s&pagebar=%(pageBar)s&id=%(pageId)s' % (para_dict)
	jsonstr = http_request.get(json_urlstr)
	para_dict['pageUrl'] = json_urlstr
	para_dict['htmlStr'] = jsonstr
	return

def crawl_timeline_pages(http_request, pageId, end_page_num):
	'''
	输入：获得cookie的request、pageId、end_page_num
	输出：此人的前五页timeline内容
	'''
	user_timeline_pages = []
	para_dict = {}
	para_dict['prePage'] = 0
	para_dict['page'] = 1 # page number
	para_dict['pageBar'] = 0 # section number
	para_dict['pageId'] = pageId

	for page in range(1, end_page_num):
		#url para : page_id = default, page = page, pre_page = 0, pagebar = 0
		para_dict['page'] = page
		para_dict['prePage'] = 0
		para_dict['crawlerTime'] = datetime.datetime.now().timestamp()
		__crawl_each_timeline_page(http_request, para_dict)
		user_timeline_pages.append(para_dict)
		#url para : page_id = default, page = page, pre_page = page, pagebar = 0
		para_dict['prePage'] = page
		para_dict['pageBar'] = 0
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

def get_user_timeline_pages(http_request, dbo_userpages, dbo_timelinepages, end_page_num = 6):
	dbo1 = dbo_userpages
	dbo2 = dbo_timelinepages
	pid_cursor = dbo1.coll.find({},{'crawled': 1, 'pageId': 1, 'userId': 1})
	timebatch = datetime.datetime.now().timestamp()
	for user in pid_cursor:
		userid = user['userId']
		pageid = user['pageId']
		crawled = int(user.get('crawled', 0))
		if crawled == 1:
			continue
		if pageid == '':
			continue
		tlp = TimelinePage(userid = userid, pageid = pageid)
		user_timeline_pages = crawl_timeline_pages(http_request, pageid, end_page_num)
		for timeline in user_timeline_pages:
			tlp.page = timeline['page']
			tlp.pagebar = timeline['pageBar']
			tlp.prepage = timeline['prePage']
			tlp.pageurl = timeline['pageUrl']
			tlp.htmlstr = timeline['htmlStr']
			tlp.crawlertime = timeline['crawlerTime']
			timelinedict = tlp.getdict()
			timelinedict['timeBatch'] = timebatch
			dbo2.coll.insert(timelinedict)
			del timelinedict
		log('get_user_timeline_pages', 'userid: ' + str(userid) + 'pageid: ' + str(pageid))

def main():
	http_request = get_request()
	dbo1 = dboperator.Dboperator(collname = 'UserHomePages')
	dbo2 = dboperator.Dboperator(collname = 'UserTimelinePages')
	get_user_timeline_pages(http_request, dbo1, dbo2, end_page_num = 6)
	dbo1.connclose()
	dbo2.connclose()
