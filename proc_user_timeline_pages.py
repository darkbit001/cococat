import re
import json
from bs4 import BeautifulSoup
from weibocrawler import dboperator
from weibocrawler import log

def load_json(htmlstr):
	jsondict = json.loads(htmlstr)
	data = jsondict.get('data')
	return data
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
	if len(weibo_from_div_Tag) > 2:
		weibo_dict['WB_from'] = None
		return 
	for w in weibo_from_div_Tag:
		try:
			if w.parent.parent['class'][0] == 'WB_detail':
				__weibo_from_extract(w, weibo_dict)
		except:
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

def divs_parser(data):
	# list1 = []
	soup = BeautifulSoup(data)
	tags = soup('div', class_ = 'WB_feed_type SW_fun S_line2 ')
	# for i in range(len(tags)):
		# list1.append(tags[i].extract())
	return tags

def time_from_parser(div):
	div = div.find('div', 'WB_from')
	a1 = div.a
	a2 = a1.find_next_sibling('a')
	date = a1.get('date', -1)
	dateFormart = a1.get('title', -1)
	fromUrl = a2.get('href')
	fromText = a2.string
	return date, dateFormart, fromUrl, fromText

def info_parser(div):
	mid = div.get('mid', -1)
	tbInfo = div.get('tbinfo', -1)
	mInfo = div.get('minfo', -1)
	isForward = div.get('isforward', -1)
	omid = div.get('omid', -1)
	return mid, tbInfo, mInfo, isForward, omid

def content_parser(div):
	div = div.find('div', class_ = 'WB_text')
	text = div.get_text(strip = True)
	return text

def main():
	log('main', 'running')
	dbo = dboperator.Dboperator(collname = 'UserTimelinePages')
	# dbo2 = dboperator.Dboperator(collname = 'UserTimelines')
	cursor = dbo.coll.find({},{'htmlStr': 1, 'userId': 1}).limit(100)
	for c in cursor:
		data = load_json(c['htmlStr'])
		tags = divs_parser(data)
		# tag = tags[3]
		for tag in tags:
			content_parser(tag)
		# page_list = list(cursor)
		# print(len(page_list))
		# i = 1
		# for page in page_list:
		# 	htmlstr = page['htmlStr']
		# 	data = load_json(htmlstr)
		# 	weibo_list = weibo_file_parse(data)
		# 	for weibo in weibo_list:
		# 		mid = weibo['mid']
		# 		# if dbo2.coll.find({'mid': mid},{'mid': 1}).count() > 0:
		# 		#	continue
		# 		dbo2.coll.update({'mid': mid}, {'$set': weibo}, upsert = True)
		# 	print(i)
		# 	i +=1
	dbo.connclose()
	log('main', 'finished')

	# dbo2.connclose()
	
main()
