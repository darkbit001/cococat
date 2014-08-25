import re
import json
from bs4 import BeautifulSoup
from weibocrawler import dboperator
from weibocrawler import log
def load_json(htmlStr):
	pattern = re.compile(r'<script>parent.FM.view\((.+)\)</script>')
	json_data = pattern.findall(htmlStr)[0]
	jsondic = json.loads(json_data)	
	html = jsondic.get('html')
	return html
class Soup():
	html = ''
	def __init__(self, **para):
		self.html = para['html']
		self.soup = BeautifulSoup(self.html)
	def li(self):
		soup = self.soup
		tags = soup.find_all('li', class_='clearfix S_line1')
		return tags
def user_info_parser(action_data):
	'''string like uid=5100120823&fnick=高端住宅营销&sex=m'''
	pattern = re.compile(r'uid=(\d+?)&fnick=(.+?)&sex=(\S*)')
	(uid, nickName, gender) = pattern.findall(action_data)[0]
	return uid, nickName, gender
	
def from_parser(tag):
	# pattern = re.compile(r'通过<a.*?href=\"(.+?)\".*?\" >(.+?)</a>关注')
	fromdiv = tag.find_all('div', class_='from W_textb')
	div = fromdiv[0]
	fromUrl = div.a['href']
	fromText = div.a.string
	return fromUrl, fromText
	
def parse_follow_list(html):
	s = Soup(html = html)	
	tags = s.li()
	follow_list = []
	for tag in tags:
		relation_dict = {} # keys: userId, nickName, gender, fromUrl, fromText
		
		try:
			userId, nickName, gender = user_info_parser(tag['action-data'])
			relation_dict['userId'] = userId
			relation_dict['nickName'] = nickName
			relation_dict['gender'] = gender
		except:
			relation_dict['userId'] = -1
			relation_dict['nickName'] = -1
			relation_dict['gender'] = -1
		
		try:
			fromUrl, fromText = from_parser(tag)
			relation_dict['fromUrl'] = fromUrl
			relation_dict['fromText'] = fromText	
		except:
			relation_dict['fromUrl'] = -1
			relation_dict['fromText'] = -1
			
		follow_list.append(relation_dict) # [relation_dict1, relation_dict2]
		del relation_dict
	return follow_list

def map_follower_list(follow_list, userId): # follow_list is the followers group of userId
	relation_list = []	
	for user in follow_list:
		re_dict = {}
		re_dict.update(user)
		re_dict['followeeId'] = userId
		relation_list.append(re_dict)
		del re_dict
	return relation_list

def map_followee_list(follow_list, userId):	# follow_list is the followee group of userId
	relation_list = []	
	for user in follow_list:
		re_dict = {}
		re_dict.update(user)
		re_dict['followeeId'] = re_dict['userId']
		re_dict['userId'] = userId
		relation_list.append(re_dict)
		del re_dict
	return relation_list
def map_follow_list(follow_list, userId, flag):
	if flag == 'follower':
		return map_follower_list(follow_list, userId)
	elif flag == 'followee':
		return map_followee_list(follow_list, userId)

def update_crawler(dbo_UserHomePages, userId, flag, value):
	if flag == 'follower':
		dbo_UserHomePages.coll.update({'userId': userId}, {'$set':{'followerCrawled': value}}, multi = True)
	elif flag == 'followee':
		dbo_UserHomePages.coll.update({'userId': userId}, {'$set':{'followeeCrawled': value}}, multi = True)

def parse_relation_pages(dbo1, dbo2, dbo3):	
	cursor = dbo1.coll.find({}, {'htmlStr': 1, 'userId': 1, 'flag': 1, 'pageUrl': 1})
	for page in cursor:
		flag = page['flag']
		userId = page['userId']
		try:
			html = load_json(page['htmlStr'])
		except:
			# crawler error
			update_crawler(dbo3, userId, flag, 0)			
			log('Json load error', userId + '\t' + flag)
			continue
		# print(html)
		follow_list = parse_follow_list(html)
		relation_list = map_follow_list(follow_list, userId, flag)
		# try:
		if len(relation_list) == 0:
			log('relation page has none user', userId)
			continue
		# except:
		# 	print(userId)
		# 	print(page['pageUrl'])
		# 	print(page['htmlStr'])
		for r in relation_list:
			# userId = r['userId']
			# followeeId = r['followeeId']
			dbo2.coll.update({'userId': r['userId'], 'followeeId': r['followeeId']}, {'$set': r}, upsert = True)


def main():
	from weibocrawler.config import getconfig
	cfg = getconfig()
	Collection_UserRelationPages = cfg['Collections']['UserRelationPages']
	Collection_UserRelations = cfg['Collections']['UserRelations']
	Collection_UserHomePages = cfg['Collections']['UserHomePages']
	# dbo1 = dboperator.Dboperator(collname = 'UserRelationPages')
	# dbo2 = dboperator.Dboperator(collname = 'UserRelations')
	# dbo3 = dboperator.Dboperator(collname = 'UserHomePages')
	log('proc_user_relation_pages.py', 'Running')
	dbo1 = dboperator.Dboperator(collname = Collection_UserRelationPages)
	dbo2 = dboperator.Dboperator(collname = Collection_UserRelations)
	dbo3 = dboperator.Dboperator(collname = Collection_UserHomePages)
	parse_relation_pages(dbo1, dbo2, dbo3)
	dbo3.connclose()
	dbo2.connclose()
	dbo1.connclose()
	log('proc_user_relation_pages.py', 'Finished')
# main()



