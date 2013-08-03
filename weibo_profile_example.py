#
# weibo_profile_example.py
#
# doufunao 2013-08-02
#

import sys

from weibocrawler import WeiboProfile
from weibocrawler import WeiboLogin
from weibocrawler import WeiboHttpRequest

def main():

	username = 'f641679@rmqkr.net'
	password = 'f641679'
	url = 'http://weibo.com/u/'+sys.argv[1]
	#url = 'http://weibo.com/p/1005051697142574/follow'
	#print(url)
	login = WeiboLogin(username, password)
	http_request = WeiboHttpRequest(login)
	text = http_request.get(url)
	
	#Instantiate class profile
	#text is the input strings
	'''
	with open('profile_temple.txt', mode = 'w', encoding = 'utf-8') as a_file:
		num = a_file.write(text)
	print(num)

	'''
	# Instantiating class
	p = WeiboProfile(text)

	profilelist = p.get_profile()
	
	# insert an item into collection
	# print all the document in collection	
	for x in profilelist:
		print(x)

	#This function is used in http://weibo.com/p/pageid
	#or http://weibo.com/nickname
	#or http://weibo.com/u/uid
	followlist = p.get_list(flag = True)

	for x in followlist:
		print(x)

	
if __name__ == "__main__":
    main()