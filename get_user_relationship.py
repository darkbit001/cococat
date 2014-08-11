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


def crawl_user_follow_page(http_request, pageid):
	'''
	输入的urlstr返回的值应为script脚本信息
	urlstr example:		
		http://weibo.com/p/1002061618051664/follow?pids=Pl_Official_LeftHisRelation__33&page=4&ajaxpagelet=1
		http://weibo.com/p/1005051330747684/follow?pids=Pl_Official_LeftHisRelation__32&page=1&ajaxpagelet=1
	write_flag 控制是否写入文件
	'''
	sleeptime = random.randint(3,8)	
	weibocrawler.log('get_user_following_html sleeptime', sleeptime)
	time.sleep(sleeptime)
	html_str = None
	html_raw = request.get(urlstr)
	if len(html_raw) < 500 :
		weibocrawler.log('get follow page', 'Len of html_raw < 500')
		if html_raw.find('\"html\"') == -1:
			weibocrawler.log('get follow page', 'Cant find key [html]')
			print(html_raw)
			return html_str
		weibocrawler.log('get follow page', 'Will sleep 20s')
		print(html_raw)
		time.sleep(20)
		html_raw = request.get(urlstr)
	soup = BeautifulSoup(html_raw)
	script_content = soup.script.string
	start_loc = script_content.find('(')+1
	end_loc = len(script_content)-1

	if json.loads(script_content[start_loc:end_loc]).get('ns') != 'pl.content.followTab.index':
		html_str = None
		return html_str

	html_str = json.loads(script_content[start_loc:end_loc]).get('html')

	if write_flag == True:
		current_pwd = os.getcwd()
		weibocrawler.log('write to file', open(current_pwd + '\\SampleData\\user_follower_list_example', 'w').write(html_raw))
	return html_str
