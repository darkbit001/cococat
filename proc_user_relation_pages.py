import re
import json
from bs4 import BeautifulSoup
from weibocrawler import dboperator

def load_json(htmlStr):
	pattern = re.compile(r'<script>parent.FM.view\((.+)\)</script>')
	json_data = pattern.findall(htmlStr)[0]
	jsondic = json.loads(json_data)
	return jsondic.get('html', -1)
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
		relation_dict = {}
		
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
			
		follow_list.append(relation_dict)
		del relation_dict
	return follow_list
def map_follow_list(follow_list, userId, flag):
	if flag == 'follower':
		

def main():
	dbo1 = dboperator.Dboperator(collname = 'UserRelationPages2')
	cursor = dbo1.coll.find({}, {'htmlStr': 1, 'userId': 1, 'flag': 1})
	for page in cursor:
		flag = page['flag']
		userId = page['userId']
		html = load_json(page['htmlStr'])
		# print(html)
		follow_list = parse_follow_list(html)
			relation
	dbo1.connclose()
main()