import weibocrawler
from weibocrawler import log
from weibocrawler import dboperator
from weibocrawler import weibo_struct
import time
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

def __crawler_each_page(http_request, url):
	sleeptime = random.randint(30, 50)
	log('crawler_each_page sleep time', str(sleeptime))
	time.sleep(sleeptime)
	htmlstr = http_request.get(url)
	return htmlstr

def crawler_pages(http_request, dbo_userpages, dbo_userclawer):
	# up = weibo_struct.UserHomePage()
	urls = dbo_userclawer.coll.find({},{'crawled': 1, 'href': 1})
	# urls = dbo_userclawer.coll.find({'href': 'http://weibo.com/u/3867395827'},{'crawled': 1, 'href': 1})
	timebatch = datetime.datetime.now().timestamp()
	for url in urls:
		if int(url.get('crawled', 0)) == 1:
			continue
		else:
			pagedic = {}
			pagedic['pageId'] = -1
			pagedic['userId'] = -1
			pagedic['nickName'] = ''
			pagedic['pageUrl'] = url['href']
			pagedic['nickId'] = url['_id']
			pagedic['timeBatch'] = timebatch
			htmlstr = __crawler_each_page(http_request, url['href'])
			pagedic['htmlStr'] = htmlstr
			pagedic['crawlerTime'] = datetime.datetime.now().timestamp()

			dbo_userpages.coll.update({'href': pagedic['href']},{'$set': pagedic}, upsert = True)
			dbo_userclawer.coll.update({'href': url['href']} ,{'$set': {'crawled': 1 } }, multi = True)
			log('crawler page', url['href'])



def main():
	'''
	This function will crawler user page read from collection Nicks and insert them into collection UserHomePages from MongoDB.
	'''
	from weibocrawler.config import getconfig
	cfg = getconfig()
	Collection_UserHomePages = cfg['Collections']['UserHomePages']
	Collection_Nicks = cfg['Collections']['Nicks']

	# dbo1 = dboperator.Dboperator(collname = 'UserHomePages') # store: screen_name, page_id, user_id, htmlStr 
	# dbo2 = dboperator.Dboperator(collname = 'Nicks')
	dbo1 = dboperator.Dboperator(collname = Collection_UserHomePages) # store: screen_name, page_id, user_id, htmlStr 
	dbo2 = dboperator.Dboperator(collname = Collection_Nicks)
	http_request = get_request()
	crawler_pages(http_request, dbo1, dbo2)
	dbo1.connclose()
	dbo2.connclose()

main()

