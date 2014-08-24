#
# 1. Parse the data which is crawled by 'get_search_results.py'and stored in collection SearchPages.
# 2. Insert parser seed user data into collection Nicks.
# 
# by doufunao
#
# 2014-03-15
#
import json
from bs4 import BeautifulSoup
from weibocrawler import dboperator
from weibocrawler import log

def content_html_parser(htmlbody):
	'''
	Usage:
		getContent(htmlbody)
			htmlbody not jsondata
		return htmlstr
	'''
	soup = BeautifulSoup(htmlbody)
	scriptSet = soup.find_all('script')
	scriptContent = scriptSet[9].contents[0]

	start = scriptContent.find('(')
	end = len(scriptContent)
	getjson = scriptContent[(start+1): (end-1)]
	loadjson = json.loads(getjson)
	content = loadjson['html']
	return content

def nick_parser(content):
	soup = BeautifulSoup(content)
	#Attribute 'nick-name'&'usercard' exist
	result = soup.find_all("a", attrs = {"nick-name": True,"usercard": True})
	nicklist = []
	for n in result:
		href = n['href']
		nick_name = n['nick-name']
		title = n['title']
		namedict = {}
		namedict['href'] = href
		namedict['nick-name'] = nick_name
		namedict['title'] = title
		nicklist.append(namedict)
	return nicklist

def read_search_page(dbo, pipline):
	cursor = dbo.coll.find(pipline)
	# print(dbo.coll.distinct('timeBatch'))
	pagelist = list(cursor)
	return pagelist

def search_page_parser(p):
	nicklist = []
	htmlstr = p['htmlStr']
	content = content_html_parser(htmlstr)
	nicklist_perpage = nick_parser(content)
	for n in nicklist_perpage:
		n.update(p)			
		n['searchPageId'] = n['_id']
		del n['_id']
		del n['htmlStr']
		nicklist.append(n)
	return nicklist


def parse_search_pages(dbo_SearchPages, dbo_Nicks):
	dbo = dbo_SearchPages
	dbo2 = dbo_Nicks
	cursor = dbo.coll.find()
	for page in cursor:
		nicklist = search_page_parser(page)
		for nick in nicklist:
			dbo2.coll.update({'href': nick['href']}, {'$set': nick}, upsert = True)
def main():
	log('parse_search_pages', 'Running')
	dbo = dboperator.Dboperator(collname = 'SearchPages')
	dbo2 = dboperator.Dboperator(collname = 'Nicks')
	parse_search_pages(dbo, dbo2)
	dbo.connclose()
	dbo2.connclose()
	log('parse_search_pages', 'Finished')
main()
