#
# doufunao
# 2014-03
#
import re
import os
import json
import shutil
import init
from bs4 import BeautifulSoup
from weibocrawler import dboperator
from weibocrawler import log
def __weibo_struct_extract(feed_div_Tag, weibo_dict):
	'''
	input
		feed_div_Tag
	output
		weibo_dict
	'''
	div = feed_div_Tag
	weibo_dict['mid'] = div['mid']
	weibo_dict['tbinfo_text'] = div['tbinfo']
	weibo_dict['ouid'] = __find_child_attr('ouid', div['tbinfo'])
	weibo_dict['rouid'] = __find_child_attr('rouid', div['tbinfo'])

	if div.has_attr('omid'):
		weibo_dict['omid'] = div['omid']
	else:
		weibo_dict['omid'] = None

	if div.has_attr('isforward'):
		weibo_dict['isforward'] = div['isforward']
		#print('has_attr isforward   '+str(weibo_dict['isforward']))
	else:
		weibo_dict['isforward'] = None

	if div.has_attr('minfo'):
		weibo_dict['minfo_text'] = div['minfo']
		weibo_dict['ru'] = __find_child_attr('ru', div['minfo'])
		weibo_dict['rm'] = __find_child_attr('rm', div['minfo'])
	else:
		weibo_dict['minfo_text'] = None
		weibo_dict['ru'] = None
		weibo_dict['rm'] = None
	
	string = str(div)
	div_soup = BeautifulSoup(string)
	#获得原创微博正文
	content_div = div_soup('div', attrs = {'class':'WB_text', 'node-type':'feed_list_content'})[0]	
	__weibo_text_extract(content_div, weibo_dict)
	weibo_from_div_Tag = div_soup('div', attrs = {'class':'WB_from'})
	
	#log('len',len(weibo_from_div_Tag))
	if len(weibo_from_div_Tag) > 2:
		#if len > 2, this may not a normal weibo. may be ad!
		weibo_dict['WB_from'] = None
		return 
	for w in weibo_from_div_Tag:
		#log('index',weibo_from_div_Tag.index(w))
		try:
			if w.parent.parent['class'][0] == 'WB_detail':
				__weibo_from_extract(w, weibo_dict)
		except:
			#log('error',weibo_from_div_Tag.index(w))
			continue
	#获得转发的微博正文
	try:
		if weibo_dict['isforward'] == "1":
			original_div_Tag = div_soup('div', attrs = {'class':'WB_media_expand SW_fun2 S_line1 S_bg1'})[0]
			original_div_soup = BeautifulSoup(str(original_div_Tag))
			original_text_div_Tag = div_soup('div', attrs = {'class':'WB_text'})[0]
			__weibo_text_extract(original_text_div_Tag, True)
			from_weibo_Tag = original_div_soup('div', attrs = {'class':'WB_from'})[0]
			__weibo_from_extract(from_div_Tag, weibo_dict, True)
	except:
		#原始微博已被删除
		weibo_dict['original_content'] = None

	return weibo_dict

def __weibo_text_extract(text_div_Tag, weibo_dict, isforward = False):
	if isforward == False:
		weibo_dict['content'] = text_div_Tag.get_text()
	elif isforward == True:	
		weibo_dict['original_content'] = text_div_Tag.get_text()

	return weibo_dict
def __weibo_from_extract(from_div_Tag, weibo_dict, isforward = False):
	'''
	Extract weibo_from weibo_from_href from class='WB_from' div Tag
	'''
	string = str(from_div_Tag)
	div_soup = BeautifulSoup(string)
	date_a = div_soup('a', attrs = {'node-type':'feed_list_item_date'})[0]
	try:
		from_a = div_soup('a', attrs = {'action-type':'app_source'})[0]
		href = from_a['href']
		from_string = from_a.string
	except:
		href = None
		from_string = None

	if isforward == False:
		weibo_dict['date_format'] = date_a['title']
		weibo_dict['date'] = date_a['date']
		weibo_dict['from_href'] = href
		weibo_dict['from'] = from_string
	elif isforward == True:
		weibo_dict['original_date_format'] = date_a['title']
		weibo_dict['original_date'] = date_a['date']
		weibo_dict['original_from_href'] = href
		weibo_dict['original_from'] = from_string

	return weibo_dict
def __weibo_handle_extract(handle_div_Tag, weibo_dict):
	'''
	Extract forward_num favorite_num comment_num from class='WB_handle' div Tag
	'''
def weibo_file_parse(weibo_content_str):
	'''
	input:
		微博文件字符串
	ouput:
		微博内容词典 编码后
		timeline_dict
			user_info
			weibo_content_list
	'''

	#----weibo_content_list_raw = weibo_content_str.split('=+=+=\n')	
	#----if len(weibo_content_list_raw)<3:
	#----	weibo_content_list_raw = weibo_content_str.split('<!--break-->')
	#---- The lines has ----mark is contributed in the page files before
	#JUST INGORE!!

	weibo_content_list = []
	#----for weibo in weibo_content_list_raw:
	soup = BeautifulSoup(weibo_content_str)
	#print(str(weibo_content_list.index(weibo)))
	results = soup('div', attrs = {'class':'WB_feed_type SW_fun S_line2 '})
	for div in results:
		'''
		获得微博基本信息weibo_info_dict
		'''
		weibo_dict = {}
		__weibo_struct_extract(div, weibo_dict)
		#log('weibo_dict', repr(weibo_dict))
		#json编码
		#print(json.dumps(weibo_dict, sort_keys=True, indent=4 * ' '))
		#print(div.prettify())
		#print(repr(weibo_dict))
		#weibo_dict_json = json.JSONEncoder().encode(weibo_dict)
		weibo_content_list.append(weibo_dict)
		del weibo_dict
	
	return weibo_content_list

def __find_child_attr(attr_name, text):
	'''
	attr_name 
		minfo has ru rm
		mid has ouid rouid 
	text
		input text string
	'''
	pattern_ouid = re.compile(r'ouid=(\d+)')
	pattern_rouid = re.compile(r'rouid=(\d+)')
	pattern_ru = re.compile(r'ru=(\d+)')
	pattern_rm = re.compile(r'rm=(\d+)')

	if attr_name == 'ouid':
		if pattern_ouid.search(text):
			return pattern_ouid.findall(text)[0]
		else:
			return None
	if attr_name == 'rouid':
		if pattern_rouid.search(text):
			return pattern_rouid.findall(text)[0]
		else:
			return None
	if attr_name == 'ru':
		if pattern_ru.search(text):
			return pattern_ru.findall(text)[0]
		else:
			return None
	if attr_name == 'rm':
		if pattern_rm.search(text):
			return pattern_rm.findall(text)[0]
		else:
			return None
def __insert_list_to_collection(collname, weibo_list):
	dbo = dboperator.Dboperator(collname)
	for weibo in weibo_list:
		dbo.insert(weibo)
def __load_weibo_page_str(weibo_page_dict_list):
	weibo_page_str_list = []
	for pdict in weibo_page_dict_list:
		weibo_page_str_list.append(pdict['htmlstr'])
	weibo_page_str = '\n'.join(weibo_page_str_list)
	log('weibo_page_str_list', len(weibo_page_str_list))
	return weibo_page_str
def insert_weibolist_to_mongodb(initdir, collname):
	'''
	read htmlstr from file
	after analysing them, insert weibo into mongodb
	'''
	data_pwd = initdir.pwd_dict['data']
	for key_dir in os.listdir(data_pwd):
		pwd_dict = initdir.get_pwd_per_keyword(key_dir)
		file_read_pwd = pwd_dict['weibo_Content']
		error_weiboContent_pwd = pwd_dict['error_weibo_Content']
		weiboContent_get_pwd = pwd_dict['weibo_Content_get']
	#	if os.path.exists(error_weiboContent_pwd) != 1:
	#		log('create dir error_weiboContent', os.mkdir(error_weiboContent_pwd))		
	#	if os.path.exists(weiboContent_get_pwd) != 1:
	#		log('create dir weiboContent_get', os.mkdir(weiboContent_get_pwd))
		for page_file in os.listdir(file_read_pwd):
			#try:
			page_file_pwd = '/'.join([file_read_pwd, page_file])
			f = open(page_file_pwd, 'r')
			weibo_page_dict_list = json.loads(f.read())
			f.close()
			#log('Find', weibo_content_str.find('This page has no'))
			weibo_content_str = __load_weibo_page_str(weibo_page_dict_list)
			if weibo_content_str.find('This page has no') != -1:
				error_page_file_pwd = error_weiboContent_pwd + page_file
				log('move file ' + page_file, shutil.move(page_file_pwd, error_page_file_pwd))
				continue
			log('Start to get', page_file)			
			weibo_list = weibo_file_parse(weibo_content_str)			
			__insert_list_to_collection(collname, weibo_list)
			log('insert ',page_file)
			page_file_get_pwd = weiboContent_get_pwd + page_file
			log('Got ' + page_file, shutil.move(page_file_pwd, page_file_get_pwd))
	
if __name__ == '__main__':
	current_pwd = os.getcwd()
	initdir = init.InitDir(current_pwd)
	insert_weibolist_to_mongodb(initdir, 'timeline0324')