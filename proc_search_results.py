#
# by doufunao
#
# Find the index of the script which contain the main weibo text
#
# input:
#	Data/Keyword/searchResult/SearchResult_[pagenum]_[time]
#
# output:
#	Data/Keyword/nicklist
#	Data/Keyword/scriptContent/scriptContent_[pagenum]_[time]
#
# 2014-03-15
#
from bs4 import BeautifulSoup
import re
import json
import time
import os
import re
from init import InitDir
from weibocrawler import log
#from weibocrawler import dboperator


def __content_html_extract(htmlbody):
	'''
	Usage:
		getContent(htmlbody)
			htmlbody not jsondata
		return htmlstr
	'''
	soup = BeautifulSoup(htmlbody)
	scriptSet = soup.find_all('script')
	scriptContent = scriptSet[10].contents[0]

	start = scriptContent.find('(')
	end = len(scriptContent)
	getjson = scriptContent[(start+1): (end-1)]
	#print('get ' + str(scriptSet.index(scriptstr)) +' successed.\n')
	loadjson = json.loads(getjson)
	#print('load ' + str(scriptSet.index(scriptstr)) +'.\n')
	htmlstr = loadjson['html']
	#print('get html ' + str(scriptSet.index(scriptstr)) +'.\n')
	return htmlstr

def __nicklist_extract(htmlstr):
	soup = BeautifulSoup(htmlstr)
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
def __result_file_suffix_extract(filename):
	pattern = re.compile(r'SearchResult_(.+)_')
	suffix = pattern.findall(filename)[0]
	return suffix
def __write_str_to_file(file_pwd, str_to_write):
	f = open(file_pwd, 'w')
	str_to_write_json = json.JSONEncoder().encode(str_to_write)
	f.write(str_to_write_json)
	f.close()

def __read_str_from_file(file_pwd):
	f = open(file_pwd, 'r')
	htmlstr = json.loads(f.read())
	f.close()
	return htmlstr
def __read_extract_write_scriptContent(read_file_pwd, write_file_pwd):
	htmlstr = __read_str_from_file(read_file_pwd)				
	extract_str = __content_html_extract(htmlstr)
	__write_str_to_file(write_file_pwd, extract_str)
	return extract_str
def __get_keyword_dirs_pwd(initdir):
	'''
	return pwd_list
	pwd_list is a list of tuples
		A tuple contained keyword_dir_pwd, searchResult_dir_pwd, scriptContent_dir_pwd
	'''
	data_dir_name = initdir.dir_dict['data']
	searchResult_dir_name = initdir.dir_dict['search_Result']
	scriptContent_dir_name = initdir.dir_dict['script_Content']
	data_dir_pwd = '/'.join([current_pwd, data_dir_name])
	keyword_list = os.listdir(data_dir_pwd)
	pwd_list = []	
	for keyword in keyword_list:
		keyword_dir_pwd = '/'.join([data_dir_pwd, keyword])
		if os.path.isdir(keyword_dir_pwd):
			scriptContent_dir_pwd = '/'.join([keyword_dir_pwd, scriptContent_dir_name])
			searchResult_dir_pwd = '/'.join([keyword_dir_pwd, searchResult_dir_name])
			pwd_list_tu = tuple([keyword_dir_pwd, searchResult_dir_pwd, scriptContent_dir_pwd])
			pwd_list.append(pwd_list_tu)
	return pwd_list

def __read_htmlstr_list_from_file(keyword_dir_pwd, searchResult_dir_pwd, scriptContent_dir_pwd):
	k = keyword_dir_pwd
	r = searchResult_dir_pwd
	c = scriptContent_dir_pwd
	htmlstr_list = []
	searchResult_file_list = os.listdir(r)
	for filename in searchResult_file_list:
			suffix = __result_file_suffix_extract(filename)
			searchResult_file_pwd = '/'.join([r, filename])
			scriptContent_file_pwd = '/'.join([c, suffix])
			htmlstr = __read_extract_write_scriptContent(searchResult_file_pwd, scriptContent_file_pwd)
			htmlstr_list.append(htmlstr)
	return htmlstr_list

def __write_nicklist_to_file(nicklist_file_pwd, nicklist):
	f = open(nicklist_file_pwd, 'w')
	for n in nicklist:
		f.write('\t'.join([n['href'], n['nick-name'], n['title']]))
		f.write('\n')
	f.close()

def write_all_nicklist_to_file(initdir):
	'''
	Usage:
		write_all_nicklist_to_file(InitDir)
		get the keyword list from dir struct
	'''
	current_pwd = initdir.pwd_dict['current']
	nicklist_file_name = initdir.file_dict['nicklist']
	pwd_list = __get_keyword_dirs_pwd(initdir)
	record = []
	for k, r, c in pwd_list:
		nicklist_file_pwd = '/'.join([k, nicklist_file_name])
		if os.path.exists(nicklist_file_pwd):
			log('nicklist exists', nicklist_file_pwd)
			continue		
		htmlstr_list = __read_htmlstr_list_from_file(k, r, c)
		nicklist = __nicklist_extract('\n'.join(htmlstr_list))
		__write_nicklist_to_file(nicklist_file_pwd, nicklist)
		record.append(nicklist_file_pwd)
		#log('__write_nicklist_to_file', nicklist_file_pwd)
	if len(record) > 0:
		log('write_all_nicklist_to_file', '\n'.join(record))

if __name__ == '__main__':
		current_pwd = os.getcwd()
		initdir = InitDir(current_pwd)
		write_all_nicklist_to_file(initdir)
