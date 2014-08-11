import weibocrawler
from weibocrawler import log
from weibocrawler import dboperator
from weibocrawler import weibo_struct
import urllib.parse
import time
import random
import re
import json
import datetime
from bs4 import BeautifulSoup
from convert_cookies import convert_cookies

def get_request(check_cookie_file = True):
	'''get a weibo http request'''
	username = 'e1441430@drdrb.com'
	password = 'e1441430'
	if check_cookie_file == True:
		convert_cookies()
	login = weibocrawler.WeiboLogin(username, password)
	http_request = weibocrawler.WeiboHttpRequest(login)
	return http_request
	
def findSearchNum(content):
	'''Parse the searchpage and get the total number of the search results'''
	soup = BeautifulSoup(content)
	scriptSet = soup.find_all('script')
	scriptContent = scriptSet[9].contents[0]

	start = scriptContent.find('(')
	end = len(scriptContent)
	getjson = scriptContent[(start+1): (end-1)]
	loadjson = json.loads(getjson)
	gethtml = loadjson['html']
	soupHtml = BeautifulSoup(gethtml)
	search_num = 0
	if soupHtml.find_all('div', attrs = {'class' : 'search_num'}):
		resultSet = soupHtml.find_all('div', attrs = {'class' : 'search_num'})
		soupSearchNum = BeautifulSoup(str(resultSet))
		s = str(soupSearchNum.span.string)
		pattern = re.compile(r'[0-9]+')
		match = pattern.search(s)
		search_num = int(match.group(0))
	return search_num

def crawler_pages(http_request, dboperator, queryStrings, end_num_input = 0):
	'''crawler_pages will crawler the SearchPages from Weibo Search Engine with queryStrings and insert them into MongoDB'''
	# htmlstr = http_request.get('http://s.weibo.com/wb/' + urllib.parse.quote(queryString) + '&xsort=hot&page=1')
	# end_num_input in range(1,50)
	# dboperator is a instance of class Dboperator
	start_num = 1
	sp = weibo_struct.SearchPage()
	timebatch = str(datetime.datetime.now().strftime("%Y%m%d%H%M"))
	sp.timebatch = timebatch
	page_list = []
	end_num = end_num_input
	for queryString in queryStrings:
		log('Begin to get', queryString)
		page_tuple = __crawler_each_page(http_request, queryString, start_num)
		urlstr = page_tuple[0]
		htmlstr = page_tuple[1]
		search_num = findSearchNum(htmlstr)

		sp.pageurl = urlstr
		sp.htmlstr = htmlstr
		sp.pageindex = start_num
		sp.crawlertime = datetime.datetime.now().timestamp()
		
		
		if search_num == 0:
			log('crawlerPage says: No search result' + str(queryString),'search_num == 0')
			return page_list
		else:
			if end_num == 0:
				end_num = int(search_num/50)
				if end_num > 50:
					end_num = 50
			start_num = start_num + 1

		log(' '.join(['\n', 'crawler_pages', str(end_num), 'pages']), ' '.join(['Got', queryString, 'search_num', str(search_num), '\n']))

		sp.resulttotal = search_num
		sp.querystring = queryString
		sp.pagetotal = end_num
		pagedict = sp.getdict()
		dboperator.insert(pagedict)
		page_list.append(pagedict)

		for x in range(start_num, end_num + 1):
			page_tuple = __crawler_each_page(http_request, queryString, x)
			urlstr = page_tuple[0]
			htmlstr = page_tuple[1]
			sp.pageurl = urlstr
			sp.htmlstr = htmlstr
			sp.pageindex = x
			sp.crawlertime = datetime.datetime.now().timestamp()
			pagedict = sp.getdict()
			dboperator.insert(pagedict)
			page_list.append(pagedict)
		
		end_num = end_num_input
	
	log('crawler_all_Page finished', len(page_list))

	return page_list


def __crawler_each_page(http_request, queryString, page_num):
	'''only one page at a time'''
	sleeptime = random.randint(30,60)
	log('crawler_each_page sleep time', str(sleeptime))
	time.sleep(sleeptime)
	url_str = 'http://s.weibo.com/wb/' + urllib.parse.quote(queryString) + '&xsort=hot&nodup=1&page=' + str(page_num)
	htmlstr = http_request.get(url_str)
	return (url_str, htmlstr)

def main():
	'''
	This function will crawler search page of weibo and write them into MongoDB.
	Usage:

	'''
	http_request = get_request()
	dbo = dboperator.Dboperator(collname = 'SearchPages', port = 27123) # get database connection and the collection is 'SearchPages' ,database make weibo as default
	queryStrings = 	['test'] # give a query string 'test' to Weibo Search Engine
	crawler_pages(http_request, dbo, queryStrings, 1)
	dbo.connclose()

if __name__ == '__main__':
	main()

