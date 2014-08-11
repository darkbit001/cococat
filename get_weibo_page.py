#
# doufunao
#
# 2014-04-02
#

import json
import os
import re
import time
import random
import convert_cookies as cookie
import urllib.request
from bs4 import BeautifulSoup
from weibocrawler import log
from weibocrawler import WeiboLogin
from weibocrawler import WeiboHttpRequest

class CrawlerforForwardComment():
	def __init__(self, username, password, check_cookie_file):
		self.username = username
		self.password = password
		self.check_cookie_file = check_cookie_file

	def get_request(self):
		if self.check_cookie_file == 1:
			cookie.convert_cookies()
		username = self.username
		password = self.password
		login = WeiboLogin(username, password)
		http_request = WeiboHttpRequest(login)
		return http_request

	def get_page_str(self, http_request, urlstr, sleep_start, sleep_end):
		#default decoding utf-8
		#content has decoded
		self.make_time_sleep(sleep_start,sleep_end)
		content = http_request.get(urlstr)
		return content

	def make_time_sleep(self, random_start, random_end):
		sleeptime = random.randint(random_start, random_end)
		log('sleeptime', sleeptime)
		time.sleep(sleeptime)

	def get_weibo_forward_list(self, http_request, para_id, para_max_page, sleep_range):
		'''
		content_list data format:
			[
				[page_num, content]
			]
		'''
		content_list = []
		for page in range(1, para_max_page + 1):
			urlstr = 'http://weibo.com/aj/mblog/info/big?_wv=5&id={}&page={}'.format(para_id, page)
			content = craw.get_page_str(http_request, urlstr, sleep_range[0] ,sleep_range[1])
			content_list.append([page, content])
		return content_list

	def get_weibo_comment_list(self, http_request, para_id, para_max_page, sleep_range):
		'''
		content_list data format:
			[
				[page_num, content]
			]
		'''
		content_list = []
		for page in range(1, para_max_page + 1):
			urlstr = 'http://weibo.com/aj/comment/big?_wv=5&id={}&page={}'.format(para_id, page)
			content = craw.get_page_str(http_request, urlstr, sleep_range[0] ,sleep_range[1])
			content_list.append([page, content])
		return content_list

class AnalyserforForwardComment():
	def __init__(self, content_undecode):
		self.o_content = content_undecode
		self.allcontent = self.__load_data()
	def __load_data(self):
		content = json.loads(self.o_content)
		con_list = []
		for x in content:
			c = json.loads(x[1])
			con_list.append(c['data']['html'])
		con_list_str = '\n'.join(con_list)
		return con_list_str
	def get_text(self):
		soup = BeautifulSoup(self.allcontent)
		return soup.get_text()
	
	def get_pure_text(self):
		soup = BeautifulSoup(self.allcontent)
		text_list = []
		pattern = re.compile(r'\(\d月\d\d日 \d{1,2}:\d{1,2}\)?')
		pattern_s = re.compile(r'None')
		for s in soup('dd'):
			text = str(s.contents[4].string).strip()
			text = re.sub(pattern, '', text)
			text = re.sub(pattern_s, '', text)
			text_list.append(text)
		return '\n'.join(text_list)

def crawler_example():
	craw = CrawlerforForwardComment('', '', 1)
	http_request = craw.get_request()
	para_id = 3689787388687963
	content_list = craw.get_weibo_forward_list(http_request, para_id, 227, [8, 20])
	content_list_json = json.JSONEncoder().encode(content_list)
	f = open(str(para_id) + '_forward', 'wb')
	f.write(content_list_json.encode('utf-8'))
	f.close()
def analyser_example(file_name):
	ana = AnalyserforForwardComment(open(file_name, 'rb').read().decode('utf-8'))
	#print(ana.get_pure_text().replace('转发微博', '').replace('//', ''))
	return ana.get_pure_text().replace('举报', '').replace('回复', '').replace('评论', '').replace('同时转发到我的微博', '')
if __name__ == '__main__':
	#f1 = 'fang/3689787388687963_forward'
	#f2 = 'fang/3689425768326186_forward'
	f3 = 'fang/3689787388687963_comment'
	f4 = 'fang/3689425768326186_comment'
	#open(f1 + '_new', 'wb').write(analyser_example(f1).encode('utf-8'))
	#open(f2 + '_new', 'wb').write(analyser_example(f2).encode('utf-8'))
	open(f3 + '_new', 'wb').write(analyser_example(f3).encode('utf-8'))
	open(f4 + '_new', 'wb').write(analyser_example(f4).encode('utf-8'))
