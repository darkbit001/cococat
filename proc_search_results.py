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
from weibocrawler import weibo_struct


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
		#print(namedict)
	#print(len(nicklist))
	return nicklist

def read_search_page(pipline):
	dbo = dboperator.Dboperator('SearchPages')
	cursor = dbo.coll.find(pipline)
	# print(dbo.coll.distinct('timeBatch'))
	pagelist = list(cursor)
	dbo.connclose()
	return pagelist

def pagelist_processer(pagelist):
	nicklist = []
	for p in pagelist:
		sp = weibo_struct.SearchPage()
		sp.setdict(p)
		htmlstr = p['htmlStr']
		content = content_html_parser(htmlstr)
		nicklist_perpage = nick_parser(content)
		sd = weibo_struct.SeedUser()
		sd.superSearchPage(sp)
		sd.searchpageid = p['_id']
		for n in nicklist_perpage:
			sd.title = n['title']
			sd.href = n['href']
			sd.nickname = n['nick-name']
			nicklist.append(sd.getdict())
	return nicklist

if __name__ == '__main__':	
	dbo = dboperator.Dboperator('SearchPages')
	cursor = dbo.coll.find({},{'timeBatch': 1, 'querystring': 1})
	dbo.connclose()

	timeBatch = ''
	querystring = ''
	
	dbo2 = dboperator.Dboperator('Nicks')

	for d in cursor:
		if timeBatch == d['timeBatch'] and 	querystring == d['querystring']:
			continue
		else:
			timeBatch = d['timeBatch']
			querystring = d['querystring']
			pipline = {'timeBatch': timeBatch, 'querystring': querystring}
			pagelist = read_search_page(pipline)
			nicklist = pagelist_processer(pagelist)
			for nick in nicklist:
				if dbo2.coll.find({'href': nick['href']}).count() != 0: 
				# To make sure the same href can not be inserted into Nicks
					continue
				else:
					dbo2.insert(nick)
	dbo2.connclose()

