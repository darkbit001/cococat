# Covert_cookies.py
# 为了应对无法从weibo获取cookie的问题，手工制作cookies
# 	输入：cookies_copy  手工把Chrome中的cookies信息复制到cookies_copy中
#   输出: cookies.json 抽取cookies_copy中的信息生成新的cookies.json
# 原有的cookies.json备份到cookies.json_backup中 
# doufunao
# 2014-03-13
# 
import json
import shutil
def convert_cookies():
	shutil.copyfile('cookies.json', 'cookies.json_backup')
	string = open('cookies_copy', 'r').read()
	cookies_dict_new = {}
	cookies_dict_old = json.loads(open('cookies.json', 'r').read())

	for a_dict_string in string.split(';'):
		loc = a_dict_string.find('=')
		key = a_dict_string[0:loc].strip()
		value = a_dict_string[loc+1:len(a_dict_string)]
		if key in cookies_dict_old:
			cookies_dict_new[key] = value

	dict_dumps = json.dumps(cookies_dict_new)
	open('cookies.json', 'w').write(dict_dumps)
	print('>.< Have successfully created cookies.json by hand!')
#if __name__ == '__main__':
#	convert_cookies()