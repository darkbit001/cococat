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
	# pattern = re.compile(r'通过<a href="(.+?)" class="S_link2" >(.+?)</a>')
	print(tag.find_all('a', class_='S_link2'))
	return
	
def main():
	dbo1 = dboperator.Dboperator(collname = 'UserRelationPages')
	cursor = dbo1.coll.find({'userId': '2920092522'}, {'htmlStr': 1}).limit(1)
	html = load_json(cursor[0]['htmlStr'])
	s = Soup(html = html)	
	tags = s.li()
	for tag in tags:
		userId, nickName, gender = user_info_parser(tag['action-data'])
		from_parser(tag)
	dbo1.connclose()
main()