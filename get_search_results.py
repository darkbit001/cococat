import weibocrawler
from weibocrawler import log
import urllib.parse
import os
import time
import random
import sys
import init
import re
import json
from bs4 import BeautifulSoup
from convert_cookies import convert_cookies

def get_request():
	username = 'e1441430@drdrb.com'
	password = 'e1441430'
	login = weibocrawler.WeiboLogin(username, password)
	http_request = weibocrawler.WeiboHttpRequest(login)
	return http_request
def findSearchNum(content):
	soup = BeautifulSoup(content)
	scriptSet = soup.find_all('script')
	scriptContent = scriptSet[10].contents[0]

	start = scriptContent.find('(')
	end = len(scriptContent)

	getjson = scriptContent[(start+1): (end-1)]
	#print('get ' + str(scriptSet.index(scriptstr)) +' successed.\n')

	loadjson = json.loads(getjson)

	#print(loadjson)
	#print('load ' + str(scriptSet.index(scriptstr)) +'.\n')

	#print(type(loadjson))	
	gethtml = loadjson['html']
	#print(gethtml)
	soupHtml = BeautifulSoup(gethtml)
	search_num = 0
	if soupHtml.find_all('div', attrs = {'class' : 'search_num'}):
		resultSet = soupHtml.find_all('div', attrs = {'class' : 'search_num'})
		soupSearchNum = BeautifulSoup(str(resultSet))
		s = str(soupSearchNum.span.string)
		pattern = re.compile(r'[0-9]+')
		match = pattern.search(s)
		search_num = int(match.group(0))
		#print('findSearchNum says : Find '+ str(search_num) + ' results.')
	
	return search_num
'''
def create_searchResult_dir(current_pwd, keyword):
	keyword_dir_pwd = current_pwd + '/Data/' + keyword
	search_Result_dir_pwd = keyword_dir_pwd + '/searchResult'
	#print(os.getcwd())
	if os.path.exists(keyword_dir_pwd) == 0:
		log('Create dir', keyword_dir_pwd)
	else:
		os.mkdir(search_Result_pwd)
		if os.path.exists('searchResult'):
			log('Create dir searchResult', search_Result_pwd)
'''

def crawler_all_Page(http_request, queryString, start_num, end_num):
	#htmlstr = http_request.get('http://s.weibo.com/wb/' + urllib.parse.quote(queryString) + '&xsort=hot&page=1')
	htmlstr_list = []
	htmlstr = __crawler_each_Page(http_request, queryString, 1)
	search_num = findSearchNum(htmlstr)

	if search_num == 0:
		log('crawlerPage says: No search result','search_num == ' + str(search_num))
		return htmlstr_list
	else:
		end_num = int(search_num/50)
		if end_num > 50:
			end_num = 50
	
	log(' '.join(['\n', 'crawlerPage','Begin to get', str(end_num), 'pages']), ' '.join(['Got', queryString, 'search_num', str(search_num), '\n']))

	for x in range(start_num,end_num+1):
		#htmlstr = http_request.get('http://s.weibo.com/wb/' + urllib.parse.quote(queryString) + '&xsort=hot&page='+ str(x))
		htmlstr_dict = {}
		htmlstr = __crawler_each_Page(http_request, queryString, x)
		htmlstr_dict['htmlstr'] = htmlstr
		htmlstr_dict['index'] = x
		htmlstr_list.append(htmlstr_dict)

	log('crawler_all_Page finished', len(htmlstr_list))
	return htmlstr_list

def __crawler_each_Page(http_request, queryString, page_num):
	sleeptime = random.randint(10,40)
	log('__crawler_each_Page sleep time', str(sleeptime))
	time.sleep(sleeptime)
	url_str = 'http://s.weibo.com/wb/' + urllib.parse.quote(queryString) + '&xsort=hot&page=' + str(page_num)
	htmlstr = http_request.get(url_str)
	return htmlstr

def page_all_write_to_file(current_pwd, word, htmlstr_list, write_to_per_file = True):
	dir_list = [current_pwd, 'Data', word, 'searchResult']
	searchResult_pwd = '/'.join(dir_list)

	if write_to_per_file:
		log('page_all_write_to_file', 'one file per page')
		for htmlstr_dict in htmlstr_list:
			htmlstr_json = json.JSONEncoder().encode(htmlstr_dict['htmlstr'])
			page_index_num = htmlstr_dict['index']
			__page_each_write_to_file(searchResult_pwd, htmlstr_json, page_index_num)
	else:
		log('page_all_write_to_file', 'all pages in one file')
		htmlstr_list_json = json.JSONEncoder().encode(htmlstr_list)
		file_pwd = searchResult_pwd + '/SearchResultAll'
		open(file_pwd, 'w').write(htmlstr_list_json)
	log('page_all_write_to_file finished', '\t'.join([word, str(len(htmlstr_list)), searchResult_pwd]))

def __page_each_write_to_file(searchResult_pwd, htmlstr, page_index_num):
	x = page_index_num
	file_pwd = searchResult_pwd + '/SearchResult_' + str(x) + '_' + str(time.time())[12:17]
	f = open(file_pwd, 'w')
	f.write(htmlstr)
	f.close()

def main():
	'''
	This function will crawler search page of weibo and write them into files.
	Usage:
		python3 get_search_results.py 1
		The para is the cookie_bool. 1 
	'''
	if len(sys.argv) < 2 :
		log('para error', 'please enter cookie_bool [0,1]')
		sys.exit()
	cookie_bool = sys.argv[1]
	if cookie_bool == '1':
		convert_cookies()
		log('convert_cookies', 'on')
	elif cookie_bool == '0':
		log('convert_cookies', 'off')
	else:
		log('convert_cookies para error', 'please enter the right para 0 or 1')
		sys.exit()
	current_pwd = os.getcwd()
	O_init = init.InitDir(current_pwd)
	wordlist = O_init.get_keyword_list()
	http_request = get_request()
	f = open('userdict_got' ,'w')
	for word in wordlist:
		htmlstr_list = crawler_all_Page(http_request, word, 1, 50)
		log('crawlerPage ' + word, str(len(htmlstr_list)))
		if len(htmlstr_list) == 0:
			f.write(word + '\n')
			continue
		page_all_write_to_file(current_pwd, word, htmlstr_list, True)
		print('\nWord Complete ===============================================\n')
		f.write(word + '\n')
	f.close()
if __name__ == '__main__':
	main()

