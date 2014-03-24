import urllib.request
import weibocrawler
import json
import os
import re
from bs4 import BeautifulSoup
import time
import random
from weibocrawler import log
import get_weibo_follow
import init


def get_request():
	username = 'e1441430@drdrb.com'
	password = 'e1441430'
	login = weibocrawler.WeiboLogin(username, password)
	http_request = weibocrawler.WeiboHttpRequest(login)
	return http_request

def write_error_nicklist(user_id, urlstr):
	f = open('error_nicklist', 'a')
	f.write(str(user_id)+ '\t' + urlstr + '\n')
	f.close()
	log('error_nicklist add a mew url',user_id + '\t' + urlstr)

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

def __get_each_timeline_page(http_request, para_dict):
	print_dict = {}
	print_dict.update(para_dict)
	print_dict['htmlstr'] = ''
	log('Will get page', repr(print_dict))
	del print_dict
	sleeptime = random.randint(5,10)
	log('Ready to get each json data. Just have a rest', 'sleeptime: ' + str(sleeptime))
	time.sleep(sleeptime)
		
	json_urlstr = 'http://weibo.com/p/aj/mblog/mbloglist?pre_page=%(pre_page)s&page=%(page)s&pagebar=%(pagebar)s&id=%(page_id)s' % (para_dict)
	jsonstr = http_request.get(json_urlstr)
	json_load = json.loads(jsonstr)
	htmlstr = json_load['data']
	break_para = False
	if len(htmlstr) < 1000:
		log('Error : json[\'data\'] has got none', str(len(htmlstr)))
		break_para = True
	para_dict['json_urlstr'] = json_urlstr
	return htmlstr, break_para
def __list_append_more_dicts(timeline_list, para_dict_list):
	temp_dict = {}
	for d in para_dict_list:
		temp_dict.update(d)
	timeline_list.append(temp_dict)
	return timeline_list
def __get_page_and_add_to_list(http_request, timeline_page_list, para_dict):
	htmlstr, break_para = __get_each_timeline_page(http_request, para_dict)
	if break_para == True:
		write_error_nicklist(para_dict['user_id'], para_dict['urlstr'])
		return timeline_page_list, break_para
	#log('para_dict', str(para_dict.items()))
	para_dict['htmlstr'] = htmlstr
	timeline_page_list = __list_append_more_dicts(timeline_page_list, [para_dict])
	return timeline_page_list, break_para

def get_all_timeline_page(http_request, urlstr):
	'''
	输入：获得cookie的request、个人主页地址、待写入的user_dict
	输出：此人的前五页timeline内容
	'''
	user_dict = {}
	timeline_page_list = []

	weibo_html_str = http_request.get(urlstr)

	log('get_user_id_nickname', get_weibo_follow.get_user_id_nickname(user_dict, weibo_html_str))
	header_html_str = get_weibo_follow.get_user_header_html_str(http_request, user_dict)
	log('get_user_profile', get_weibo_follow.get_user_profile(user_dict, header_html_str))
	
	if int(user_dict['user_id']) == -1:
		timeline_page_dict = {}
		timeline_page_dict.update(user_dict)
		timeline_page_list.append(timeline_page_dict)
		#print('user_id = -1 , break')
		return timeline_page_list
	
	end_page_num = int((int(user_dict['weibo_num']) / 45) + 1)
	log('end_page_num', end_page_num)
	if 	end_page_num > 5:
		end_page_num = 11

	para_dict = {}
	para_dict['pre_page'] = 0
	para_dict['page'] = 1 #page number
	para_dict['pagebar'] = 0 #section number
	para_dict['urlstr'] = urlstr
	para_dict.update(user_dict)
	del user_dict
	'''
	para_dict['page_id'] = user_dict['page_id']
	para_dict['user_id'] = user_dict['user_id']
	para_dict['screen_name'] = user_dict['screen_name']
	para_dict['weibo_num'] = user_dict['weibo_num']
	'''
	user_id = para_dict['user_id']

	try:
		for page in range(1, end_page_num):
			#url para : page_id = default, page = page, pre_page = 0, pagebar = 0
			para_dict['page'] = page
			para_dict['pre_page'] = 0
			para_dict['fetch_time'] = time.time()
			if __get_page_and_add_to_list(http_request, timeline_page_list, para_dict)[1]:
				break
			
			#url para : page_id = default, page = page, pre_page = page, pagebar = 0
			para_dict['pre_page'] = page
			para_dict['pagebar'] = 0			
			if __get_page_and_add_to_list(http_request, timeline_page_list, para_dict)[1]:
				break

			#url para : page_id = default, page = page, pre_page = page, pagebar = 1
			para_dict['pagebar'] = 1
			if __get_page_and_add_to_list(http_request, timeline_page_list, para_dict)[1]:
				break
			#log('Url para','Page: ' + str(page) + ' len(jsondata[\'timeline_page\']) : ' + str(len(jsondata['timeline_page'])))
	
	except Exception as err:
		log('para_dict', repr(para_dict))
		log('err', err)

	return timeline_page_list

def write_page_to_file(request, initdir):
	'''
	从Data/Keyword/下读取nicklist_new中的urlstr
	将获取的page存入Data/Keyword/weiboContent下
	文件名格式：userid_top_5_page
	文件数据格式
		timeline_page_list
		[timeline_page_dict, timeline_page_dict, ...]
		timeline_page_dict keys:
		[pre_page, page, pagebar, urlstr, user_id, page_id, screen_name, weibo_num, htmlstr, json_urlstr]
	'''
	data_pwd = initdir.pwd_dict['data']
	dir_in_data = os.listdir(data_pwd)
	nicklist_filename = 'nicklist'
	#pattern = re.compile(r'http://weibo.com/(.+)')
	for dirname in dir_in_data:
		nicklist_pwd = '/'.join([data_pwd, dirname, nicklist_filename])
		timeline_page_got_pwd = '/'.join([data_pwd, dirname, nicklist_filename +'_timeline_page_got'])
		log('nicklist_pwd', nicklist_pwd)
		f = open(nicklist_pwd, 'r')
		fp = open(timeline_page_got_pwd, 'a')

		for line in f:
			weibo_timeline_urlstr = line.split('\t')[0]
			weibo_timeline_nickname = line.split('\t')[1]
			weiboContent_pwd = '/'.join([data_pwd, dirname, initdir.dir_dict['weibo_Content']])
			if os.path.exists(weiboContent_pwd) == False:
				#os.mkdir(weiboContent_pwd)
				log('write_page_to_file', weiboContent_pwd+' doesnt exist')
				sys.exit(0)
			print('==================================================================================')
			timeline_page_list = get_all_timeline_page(request, weibo_timeline_urlstr)			
			if int(timeline_page_list[0]['user_id']) == -1:
				log('Write error nicklist', write_error_nicklist(timeline_page_list[0]['user_id'] ,weibo_timeline_urlstr))
				continue
			else:
				timeline_page_list_json = json.JSONEncoder().encode(timeline_page_list)
				file_pwd = '/'.join([weiboContent_pwd, str(timeline_page_list[0]['user_id']) + '_top_5_page'])
				log('Write weibo to file' + file_pwd, open(file_pwd, 'w').write(timeline_page_list_json))
			
			fp.write(line)
	
		fp.close()
		f.close()



def data_convert_to_json(current_pwd):
	'''
	处理之前抓取的页面
	之前抓取的页面采用 =+=+= 的分隔符
	处理后的htmlstr保存在 /weiboContent/weibo_timeline_json/ 下
	'''
	data_pwd = current_pwd + '/Data/'
	dirnames = os.listdir(data_pwd)
	for dirname in dirnames:
		dir_pwd =  data_pwd + dirname + '/'
		if os.path.isfile(dir_pwd):
			continue
		weiboContent_pwd = dir_pwd + 'weiboContent/'
		if os.path.exists(dir_pwd + '/weibo_timeline_json') == False:
			os.mkdir(dir_pwd + '/weibo_timeline_json')	
		for page in os.listdir(weiboContent_pwd):
			raw_page_pwd = weiboContent_pwd + page
			if os.path.isdir(raw_page_pwd):
				continue
			else:
				f = open(raw_page_pwd, 'r')
				#
				raw_page_1st_line = f.readline()
				if raw_page_1st_line.find('This page has no page_id.'):
					urlstr = raw_page_1st_line.split(' ')[0]
					log('no page_id ' +urlstr, open(weiboContent_pwd + 'error_page', 'a').write(urlstr+'\t'))
					f.close()
					continue
				else:	
					raw_page = f.read()
					f.close()
					pattern = re.compile(r'(.+?)_top_5_page')
					url = pattern.findall(page)[0]
					html_str = {}
					html_str['url'] = url
					html_str['weibo_timeline_page'] = []
					for p in raw_page.split('=+=+='):
						html_str['weibo_timeline_page'].append(p)
					log('len of weibo timeline', len(html_str['weibo_timeline_page']))
					timeline_json = json.JSONEncoder().encode(html_str)
					log('write to file', open(dir_pwd + '/weibo_timeline_json/' + page +'_json', 'w').write(timeline_json))

						
				

if __name__ == '__main__':


	request = get_request()
	current_pwd = os.getcwd()
	initdir = init.InitDir(current_pwd)
	write_page_to_file(request, initdir)
	#data_convert_to_json(current_pwd)