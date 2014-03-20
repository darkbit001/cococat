#
# get_weibo_follow.py
# 
# Date:2014-02
#
# By:doufunao
#
# This Program cann only run under Ubuntu
import os
import re
import urllib.request
import weibocrawler
from bs4 import BeautifulSoup
import json
import time
import random
def get_request():
	username = 'e1248698@drdrb.com'
	password = 'e1248698'
	login = weibocrawler.WeiboLogin(username, password)
	http_request = weibocrawler.WeiboHttpRequest(login)
	return http_request

def get_user_follow_html_str(request, urlstr, write_flag = False):
	'''
	输入的urlstr返回的值应为script脚本信息
	urlstr example:		
		http://weibo.com/p/1002061618051664/follow?pids=Pl_Official_LeftHisRelation__33&page=4&ajaxpagelet=1
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

def get_user_header_html_str(request, user_dict, write_flag = False):
	'''
	输入的urlstr返回的值应为script脚本信息
	urlstr example:
		http://weibo.com/p/1001062712816941?pids=Pl_Core_Header__1&ajaxpagelet=1
	write_flag 控制是否写入文件

	'''

	urlstr = 'http://weibo.com/p/{0}?pids=Pl_Core_Header__1&ajaxpagelet=1'.format(user_dict['page_id'])

	sleeptime = random.randint(3,8)	
	weibocrawler.log('get_user_header_html_str sleeptime', sleeptime)
	time.sleep(sleeptime)
	html_str = None
	html_raw = request.get(urlstr)
	if len(html_raw) < 500 :
		weibocrawler.log('get header page', 'Len of html_raw < 500')
		if html_raw.find('\"html\"') == -1:
			weibocrawler.log('get header page', 'Cant find key [html]')
			print(html_raw)
			return html_str
		weibocrawler.log('get header page', 'Will sleep 20s')
		time.sleep(20)
		html_raw = request.get(urlstr)
	soup = BeautifulSoup(html_raw)
	script_content = soup.script.string
	start_loc = script_content.find('(')+1
	end_loc = len(script_content)-1
	if json.loads(script_content[start_loc:end_loc]).get('ns') != 'pl.header.head.index':
		html_str = None
		return html_str
	html_str = json.loads(script_content[start_loc:end_loc]).get('html')
	if write_flag == True:
		current_pwd = os.getcwd()
		weibocrawler.log('write to file', open(current_pwd + '/SampleData/user_info_example_loaded', 'w').write(html_str))
	return html_str
	
def get_follow_list(user_dict, html_str, follow_flag  = 'following'):
	result_list = []
	follow_re_list = {'uid_nickname_sex': r'action-type="itemClick" action-data="uid=(\d+?)&fnick=([^&]+?)&sex=([fm]?)"',
		'followurl_path': r'通过<a href="(http://[^"]+?)" class="S_link2" >([^<]+?)</a>关注'
             }
	try:
		pattern_uid_nickname_sex = re.compile(follow_re_list['uid_nickname_sex'])
		pattern_followurl_path = re.compile(follow_re_list['followurl_path'])
		if len(pattern_uid_nickname_sex.findall(html_str)) == len(pattern_followurl_path.findall(html_str)):
			for r, z in zip(pattern_uid_nickname_sex.findall(html_str), pattern_followurl_path.findall(html_str)):
				following_dict = {}
				following_dict['user_id'] = r[0]
				following_dict['screen_name'] = r[1]
				following_dict['sex'] = r[2]
				following_dict['path_url'] = z[0]
				following_dict['path'] = z[1]
				result_list.append(following_dict)
		#weibocrawler.log('pattern follow list', 're methond')
	except:
		del result_list[:]
		soup = BeautifulSoup(html_str)
		pattern = re.compile(r'uid=(\d+?)&fnick=(.*?)&sex=(.+?)')
		for ul in soup.find_all('ul', 'cnfList'):
			for li in ul.find_all('li', attrs = {"action-type":"itemClick"}):
				user_id_str = li["action-data"]
				follow_dict = {}
				follow_dict['path'] = li('div','from W_textb')[0].a.string
				follow_dict['path_url'] = li('div','from W_textb')[0].a['href']
				follow_dict['uid'] = pattern.findall(user_id_str)[0][0]
				follow_dict['screen_name'] = pattern.findall(user_id_str)[0][1]
				follow_dict['gender'] = pattern.findall(user_id_str)[0][2]
				result_list.append(follow_dict)
		weibocrawler.log('pattern follow list', 'soup methond')

	if follow_flag == 'following':
		user_dict['followinglist'].extend(result_list)
	elif follow_flag == 'follower':
		user_dict['followerlist'].extend(result_list)

	return user_dict

def get_user_id_nickname(user_dict, html_str):
	pattern_uid = re.compile(r'\[\'oid\'\]=\'(\d+?)\'')
	pattern_nickname = re.compile(r'\[\'onick\'\]=\'(.+?)\'')
	pattern_page_id = re.compile(r'\[\'page_id\'\]=\'(.+?)\'')
	if pattern_uid.search(html_str) != None:
		user_dict['user_id'] = pattern_uid.findall(html_str)[0]
		user_dict['screen_name'] = pattern_nickname.findall(html_str)[0]
		user_dict['page_id'] = pattern_page_id.findall(html_str)[0]
	else:
		user_dict['user_id'] = -1
		user_dict['screen_name'] = "None"
		user_dict['page_id'] = -1

	return user_dict

def get_user_profile(user_dict, html_str):
	home_re_list = {'uid': r'\[\'oid\'\]=\'(\d+?)\'',
			'nickname': r'\[\'onick\'\]=\'(.+?)\'',
			'followingnum': r'node-type=\"follow\">(\d+?)</strong>',
			'followernum': r'node-type=\"fans\">(\d+?)</strong>',
			'weibonum': r'node-type=\"weibo\">(\d+?)</strong>',
			'membertype': r'class=\"W_ico16 (\w+?)\"',
			'memberlevel': r'class=\"W_level_num l(\d+?)\"',
			'gender': r'class=\"W_ico12 (?:male|female)\" title=\"(.+?)\">'}	
	
	pattern_following_num = re.compile(home_re_list['followingnum'])
	pattern_follower_num = re.compile(home_re_list['followernum'])
	pattern_weibo_num = re.compile(home_re_list['weibonum'])
	pattern_member_type = re.compile(home_re_list['membertype'])
	pattern_member_level = re.compile(home_re_list['memberlevel'])
	pattern_gender = re.compile(home_re_list['gender'])

	soup = BeautifulSoup(html_str)
	'''
	包含“<!--//用户信息-->”的页面使用xml解析方法找到关注数、粉丝数、微博数
	比如：http://weibo.com/p/1001062712816941/ 通常为政府、媒体版微博
	包含“<!--个人基本信息-->”的页面使用正则解析
	比如：http://weibo.com/u/1668675013 http://weibo.com/u/2730988193

	'''
	user_dict['following_num'] = -1
	user_dict['follower_num'] = -1
	user_dict['weibo_num'] = -1
	user_dict['gender'] = -1 #如果为政府版或媒体版微博，gender=-1

	if soup.get_text().find('//用户信息') != -1:
		for s in soup.find_all(attrs = {'class':'S_line1'}):
			if str(s.span.string).strip() == '关注':
				user_dict['following_num'] = int(str(s.strong.string))
			if str(s.span.string).strip() == '粉丝':
				user_dict['follower_num'] = int(str(s.strong.string))
			if str(s.span.string).strip() == '微博':
				user_dict['weibo_num'] = int(str(s.strong.string))
	else:
		user_dict['following_num'] = pattern_following_num.findall(html_str)[0]
		user_dict['follower_num'] = pattern_follower_num.findall(html_str)[0]
		user_dict['weibo_num'] = pattern_weibo_num.findall(html_str)[0]
		user_dict['gender'] = pattern_gender.findall(html_str)[0]
	if pattern_member_type.search(html_str) != None:
		user_dict['member_type'] = pattern_member_type.findall(html_str)[0]
	else:
		user_dict['member_type'] = 'None'
		
	if pattern_member_level.search(html_str) != None:
		user_dict['member_level'] = pattern_member_level.findall(html_str)[0]
	else:
		user_dict['member_level'] = 0
	return user_dict

def get_all_user_follow_page_html_str(request, user_dict, html_str_dict, follow_flag = 'following'):
	'''
	user_dict已经初始化
	html_str_dict需要在外部定义
	'''
	page_id = user_dict['page_id']
	html_str_dict['user_info'] = user_dict
	html_str_dict[follow_flag + '_page'] = []

	if int(user_dict[follow_flag + '_num']) > 1000:
		weibocrawler.log('get all user follow page', 'follow flag num > 1000')
		html_str_dict[follow_flag + '_page'].append({'error_info':follow_flag + '_num > 1000'})
		return

	pl_num = 33
	start_page = 1
	if follow_flag == 'following':
		urlstr = 'http://weibo.com/p/{0}/follow?pids=Pl_Official_LeftHisRelation__{1}&page={2}&ajaxpagelet=1'.format(page_id, pl_num, start_page)
	elif follow_flag == 'follower':
		urlstr = 'http://weibo.com/p/{0}/follow?pids=Pl_Official_LeftHisRelation__{1}&page={2}&ajaxpagelet=1&relate=fans'.format(page_id, pl_num, start_page)

	def get_html_str(page = 1):		
		flag = True
		err_count = 0
		html_str = None
		while flag:
			try:
				weibocrawler.log(follow_flag + ' page err_count',str(err_count) + '\tpage:\t' + str(page))
				html_str = get_user_follow_html_str(request, urlstr, follow_flag)
				flag = False
			except:
				if err_count == 2:
					weibocrawler.log(follow_flag + ' page err_count',str(err_count) + '\tpage:\t' + str(page))
					flag = False
					weibocrawler.log('Error The html str', html_str)
					html_str = None
					return html_str

				else:
					err_count += 1
		return html_str

	html_str = get_html_str()

	if html_str == None:
		pl_num = 25
		weibocrawler.log('****change pl_num to', pl_num)
	else:
		html_str_dict[follow_flag + '_page'].append(html_str)
		start_page = 2
		weibocrawler.log('start_page', start_page)

	for page in range(start_page, 11):
		if follow_flag == 'following':
			urlstr = 'http://weibo.com/p/{0}/follow?pids=Pl_Official_LeftHisRelation__{1}&page={2}&ajaxpagelet=1'.format(page_id, pl_num, page)
		elif follow_flag == 'follower':
			urlstr = 'http://weibo.com/p/{0}/follow?pids=Pl_Official_LeftHisRelation__{1}&page={2}&ajaxpagelet=1&relate=fans'.format(page_id, pl_num, page)

		html_str = get_html_str(page)
		if html_str == None:
			break
		weibocrawler.log('The len of html_str', len(html_str))
		weibocrawler.log('page_id ' + str(page_id)+ ' ' + str(page), html_str_dict[follow_flag + '_page'].append(html_str))
	#return html_str_dict

def write_follow_page_to_file(request, current_pwd):
	'''	
	input:
		request
		current_pwd
		从nicklist_new读取需要爬取的用户url
	output:
		followpage in current_pwd/Data/Keyword/followPage/follow_page_[user_id]
		data format : json 
	'''	
	data_pwd = current_pwd + '/Data/'
	dir_in_data = os.listdir(data_pwd)
	nicklist_filename = 'nicklist_new'
	html_str_dict = {}			
	for dirname in dir_in_data:
		dir_pwd = data_pwd + dirname + '/'
		
		followPage_pwd = dir_pwd + 'followPage/'
		if os.path.exists(followPage_pwd) == False:
			weibocrawler.log('Creating dir in ' + followPage_pwd, os.mkdir(followPage_pwd))

		new_nicklist_pwd =  dir_pwd + nicklist_filename
		f = open(new_nicklist_pwd, 'r')

		for line in f:

			user_dict = {}
			user_dict['followerlist'] = []
			user_dict['followinglist'] = []
			user_dict['home_page'] = line
			urlstr = line.split(' ')[0]
			time.sleep(3)
			print('==================================================================================')
			html_str_raw = request.get(urlstr)
			weibocrawler.log('Begin to get', urlstr + '\tin\t' + new_nicklist_pwd + '\tfrom\t' + dirname)
			weibocrawler.log('get_user_id_nickname', get_user_id_nickname(user_dict, html_str_raw))
			if user_dict['user_id'] == -1:
				weibocrawler.log('Error follow page write to file', open(followPage_pwd + 'error_follow_page', 'a').write(line))
				f2 = open(new_nicklist_pwd + '_follow_page_got', 'a')#将已经爬取的url写入此文件，查错使用
				f2.write(line)
				f2.close()
			else:
				if user_dict['user_id'] == 3679537124:
					weibocrawler.log('user_id got error, the thread will sleep','60s')
					time.sleep(20)
					html_str_raw = request.get(urlstr)
					weibocrawler.log('get_user_id_nickname', get_user_id_nickname(user_dict, html_str_raw))
				#head_url = 'http://weibo.com/p/{0}?pids=Pl_Core_Header__1&ajaxpagelet=1'.format(user_dict['page_id'])
				head_html_str = get_user_header_html_str(request, user_dict)
				weibocrawler.log('get_user_profile', get_user_profile(user_dict, head_html_str))
				#html_str_dict = json.loads(str(open('follow_page_2712816941.json', 'r').read()))
				weibocrawler.log('get_all_follower_list', get_all_user_follow_page_html_str(request, user_dict, html_str_dict , 'follower'))
				weibocrawler.log('get_all_following_list', get_all_user_follow_page_html_str(request, user_dict, html_str_dict , 'following'))

				html_str_dict_json = json.JSONEncoder().encode(html_str_dict)
				weibocrawler.log('follow page write to file', open(followPage_pwd + 'follow_page_' + user_dict['user_id'], 'w').write(html_str_dict_json))
				f2 = open(new_nicklist_pwd + '_follow_page_got', 'a')#将已经爬取的url写入此文件，查错使用
				f2.write(line)
				f2.close()
	
		f.close()

def write_follow_list_to_file(current_pwd):
	'''
	current_pwd : py's current path
	input:
	followpage in current_pwd/Data/Keyword/followPage/follow_page_[user_id]
	data format : json 

	output:
	followlist in current_pwd/Data/Keyword/userDict/user_dict_[user_id]
	data format : json 
	'''
	data_pwd = current_pwd + '/Data/'
	dir_in_data = os.listdir(data_pwd)
	for dirname in dir_in_data:
		dir_pwd = data_pwd + dirname + '/'
		followPage_pwd = dir_pwd + 'followPage/'
		#如果Keyword下不存在followPage文件夹，则跳过此Keyword继续遍历下一个
		if os.path.exists(followPage_pwd) == False:
			weibocrawler.log('This dir has no followPage_pwd', dirname)
			continue
		#如果Keyword下不存在userDict文件夹，则创建一个	
		if os.path.exists(dir_pwd +'userDict/') == False:
			weibocrawler.log('os.mkdir', os.mkdir(dir_pwd +'userDict/'))

		file_in_followPage = os.listdir(followPage_pwd)
		for page_file in file_in_followPage:
			if os.path.isdir(followPage_pwd + page_file):
				continue
			jsondata = json.loads(open(followPage_pwd + page_file, 'r').read())
			user_dict = jsondata['user_info']
			user_id = user_dict['user_id']
			#f1 = open(followPage_pwd + 'html_str/following_html_str_' + user_id, 'a')	
			#f2 = open(followPage_pwd + 'html_str/follower_html_str_' + user_id, 'a')
			if type(jsondata['following_page'][0]) is dict:
				user_dict['followinglist'] = jsondata['following_page'][0]
			else:								
				for p in jsondata['following_page']:
					#f1.write(p)
					get_follow_list(user_dict, p, 'following')
			if type(jsondata['follower_page'][0]) is dict:
				user_dict['followerlist'] = jsondata['follower_page'][0]
			else:				
				for p in jsondata['follower_page']:
					#f2.write(p)
					get_follow_list(user_dict, p, 'follower')		
			#f1.close()
			#f2.close()
			f = open(dir_pwd + 'userDict/user_dict_' + str(user_id), 'w')
			user_dict_json = json.JSONEncoder().encode(user_dict)
			weibocrawler.log(str(user_id) + ' user dict write to file', f.write(user_dict_json))
			f.close()

if __name__ == '__main__':
	current_pwd = os.getcwd()
	request = get_request()
	write_follow_page_to_file(request, current_pwd)
	#write_follow_list_to_file(current_pwd)