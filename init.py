#
# init.py
# 	Create all the directorys which are needed.
#	
# by doufunao
#
# 2014-03-15
#


import os
import sys
from weibocrawler import log

class InitDir():
	'''
	Usage:
		current_pwd = os.path.get_cwd()
		init = InitDir(current_cwd, 'user_dict.txt')
		init.check_and_create_dir()
	'''
	def __init__(self,current_cwd):
		
		self.dir_dict = {}
		self.pwd_dict = {}
		self.file_dict = {}
		self.dir_dict['data'] = 'Data'
		self.dir_dict['search_Result'] = 'searchResult'
		self.dir_dict['weibo_Content'] = 'weiboContent'
		self.dir_dict['error_weibo_Content'] = 'error_weiboContent'
		self.dir_dict['weibo_Content_get'] = 'weiboContent_get'
		self.dir_dict['script_Content'] = 'scriptContent'
		self.dir_dict['follow_page'] = 'followPage'
		self.dir_dict['user_dict'] = 'userDict'


		self.file_dict['keyword_file'] = 'userdict.txt'
		self.file_dict['nicklist'] = 'nicklist'

		self.pwd_dict['current'] = current_cwd
		self.pwd_dict['keyword_file'] = '/'.join([self.pwd_dict['current'], self.file_dict['keyword_file']])
		self.pwd_dict['data'] = '/'.join([self.pwd_dict['current'], self.dir_dict['data']])

		self.check_and_create_dir()
	def get_pwd_per_keyword(self, keyword):
		'''
		Get keywod's all pwd which are needed
		'''
		data_pwd = self.pwd_dict['data']
		self.pwd_dict['keyword_dir'] = '/'.join([data_pwd, keyword])
		keyword_dir_pwd = self.pwd_dict['keyword_dir']
		for k, v in self.file_dict.items():
			if k == 'keyword_file':
				continue
			self.pwd_dict[k] = '/'.join([keyword_dir_pwd, v])
		
		for k,v in self.dir_dict.items():
			if k == 'data':
				continue
			self.pwd_dict[k] = '/'.join([keyword_dir_pwd, v])
		pwd_dict = self.pwd_dict
		return pwd_dict
	def get_subdirlist_per_dir(self, dir_dict_name):
		'''
		This Function list all first sub dir in the 'Data' dir
		Demo:
			get_listdir('follow_page')
			Will return 
				current_pwd/Data/subdir1/followPage
				current_pwd/Data/subdir2/followPage
				current_pwd/Data/subdir3/followPage

		'''
		pwd = self.pwd_dict['data']
		dir_list = os.listdir(pwd)
		keyword_list = []		
		for key in dir_list:
			pwd = '/'.join([self.pwd_dict['data'], key, dir_dict_name])
			keyword_list.append(pwd)
		return keyword_list
	def get_keyword_list(self):	
		'''
		This Function just read the keywords from 'userdict.txt' file;
		Note:
			The format of keyword file is like this:
				keyword  3
				key 4
				word 1
				twitter 3
				...

		This Function just get the word in the first column.
		'''
		pwd = self.pwd_dict['keyword_file']
		if os.path.exists(pwd) == 0:
			log('This file doesnt exist', pwd)
			print('The program stop')
			sys.exit()
		f = open(pwd, 'r')
		keyword_list = []		
		for line in f:
			word = line.split(' ')[0].strip()
			if word == '':
				continue
			keyword_list.append(word)
		f.close()
		return keyword_list
	def __create_dir(self, keyword, dir_name):
		dir_list = [self.pwd_dict['data'], keyword, dir_name]
		dir_pwd = '/'.join(dir_list)
		#log('create pwd', dir_pwd)
		os.makedirs(dir_pwd)

	def __check_dir(self, keyword, dir_name):
		dir_list = [self.pwd_dict['data'], keyword, dir_name]
		dir_pwd = '/'.join(dir_list)
		#log('check pwd', dir_pwd)
		if os.path.exists(dir_pwd) == 0:
			return False
		else:
			return True

	def check_and_create_dir(self):
		keyword_list = self.get_keyword_list()
		for word in keyword_list:
			create_dir_list = []
			exist_dir_list = []
			exist_dir_list.append(word)
			for k, v in self.dir_dict.items():				
				if k == 'data' or k == 'keyword_file':
					continue
				if self.__check_dir(word, v) == False:
					self.__create_dir(word, v)
					create_dir_list.append(v)
				elif self.__check_dir(word, v) == True:
					exist_dir_list.append(v)
					continue
			log('check_and_create_dir existed dir', ' '.join(exist_dir_list))
			if len(create_dir_list) > 0:
				log('check_and_create_dir created dir', ' '.join(create_dir_list))
			

			del create_dir_list
			del exist_dir_list
