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

def crawler_pages(http_request, dbo_userpages, dbo_userclawer):
	up = weibo_struct.UserHomePage()
	urls = dbo_userclawer.coll.find({},{'crawled': 1, 'href': 1})
	# urls = dbo_userclawer.coll.find({'href': 'http://weibo.com/u/3867395827'},{'crawled': 1, 'href': 1})
	for url in urls:
		if int(url.get('crawled', 0)) == 1:
			continue
		else:
			href = url['href']
			htmlstr = __crawler_each_page(http_request, href)
			up.htmlstr = htmlstr
			up.pageurl = href
			# ud = userinfo_parser(htmlstr)
			up.nickname = '' # ud['screen_name']
			up.pageId = -1 # ud['page_id']
			up.userid = -1 # ud['user_id']
			up.crawlertime = datetime.datetime.now().timestamp()
			upd = up.getdict()
			upd['nickId'] = url['_id']
			dbo_userpages.insert(upd)
			dbo_userclawer.coll.update({'href': url['href']} ,{'$set': {'crawled': 1 } }, multi = True)
			log('crawler page', url['href'])


def __crawler_each_page(http_request, url):
	sleeptime = random.randint(20, 40)
	log('crawler_each_page sleep time', str(sleeptime))
	time.sleep(sleeptime)
	htmlstr = http_request.get(url)
	return htmlstr

def main():
	'''
	This function will crawler user page read from collection Nicks and insert them into collection UserHomePages from MongoDB.
	'''
	http_request = get_request()
	dbo1 = dboperator.Dboperator(collname = 'UserHomePages') # store: screen_name, page_id, user_id, htmlStr 
	dbo2 = dboperator.Dboperator(collname = 'Nicks')
	crawler_pages(http_request, dbo1, dbo2)
	dbo1.connclose()
	dbo2.connclose()

if __name__ == '__main__':
	main()

