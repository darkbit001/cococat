#
# doufunao
# 2014-03-30
#
import os
import json
import init
from weibocrawler import dboperator
from weibocrawler import log

def __read_page_file(dir_pwd_list):
	page_list = []

	for dir_pwd in dir_pwd_list:
		print(dir_pwd)
		ll = os.listdir(dir_pwd)
		for d in ll:
			f = open('/'.join([dir_pwd, d]), 'rb')
			page_str = f.read().decode('utf-8')
			page_list.append(json.loads(page_str))
			f.close()
		
	return page_list

def __parse_str(page_list):
	relation_list = []
	for x in page_list:
		user_id = x['user_id']
		followinglist = x['followinglist']
		followerlist = x['followerlist']
		dict_element = {}
		dict_element.update(x)
		dict_element.pop('followinglist')
		dict_element.pop('followerlist')
		if len(followinglist) > 0:
			log('get followinglist', len(followerlist))
			for d1 in followinglist:
				dict_fo = {}
				dict_fo.update(dict_element)
				dict_fo['followee_uid'] = d1['user_id']
				dict_fo['followee_screen_name'] = d1['screen_name']
				dict_fo['follow_type'] = 1
				dict_fo.update(dict_element)
				relation_list.append(dict_fo)
				del dict_fo
		if len(followerlist) > 0:
			log('get followerlist', len(followerlist))
			for d2 in followerlist:
				dict_fo = {}
				dict_fo.update(dict_element)
				dict_fo['follower_uid'] = d2['user_id']
				dict_fo['follower_screen_name'] = d2['screen_name']
				dict_fo['follow_type'] = 2
				dict_fo.update(dict_element)
				relation_list.append(dict_fo)
				del dict_fo
	return relation_list

def __insert_into_mongodb(data_list):
	dbo = dboperator.Dboperator('relation_iter2_0510')
	for x in data_list:
		dbo.insert(x)

def main():
	current_pwd = os.getcwd()
	initDir = init.InitDir(current_pwd)
	dir_pwd_list = initDir.get_subdirlist_per_dir('userDict')
	page_list = __read_page_file(dir_pwd_list)
	relation_list = __parse_str(page_list)
	__insert_into_mongodb(relation_list)

if __name__ == '__main__':
	main()