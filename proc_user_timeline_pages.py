import re
import json
from bs4 import BeautifulSoup
from weibocrawler import dboperator
from weibocrawler import log

def load_json(htmlstr):
	jsondict = json.loads(htmlstr)
	data = jsondict.get('data')
	return data

def tbinfo_parser(string):
	pattern = re.compile(r'ouid=(\d+)&?[a-z]{0,5}=?(\d*)')
	ouid, rouid = pattern.findall(str(string))[0]
	return ouid, rouid

# def minfo_parser(string):
# 	rm = ''
# 	pattern = re.compile(r'ru=\d+&rm=(\d+)')
# 	if pattern.search(str(string)) != None:
# 		rm = pattern.findall(str(string))[0]
# 	return rm

def time_from_parser(div):
	fromUrl = ''
	fromText = '未通过审核应用'
	div = div.find('div', 'WB_from')
	a1 = div.a
	date = a1.get('date', -1)
	dateFormart = a1.get('title', -1)
	a2 = a1.find_next_sibling('a')
	if a2 != None:
		fromUrl = a2.get('href')
		fromText = a2.string

	return date, dateFormart, fromUrl, fromText

def content_parser(div):
	div = div.find('div', class_ = 'WB_text')
	text = div.get_text(strip = True)
	return text

def info_parser(div):
	mid = div.get('mid', -1)
	tbInfo = div.get('tbinfo', -1)
	mInfo = div.get('minfo', -1)
	isForward = div.get('isforward', -1)
	omid = div.get('omid', -1)
	return mid, tbInfo, mInfo, isForward, omid


def divs_parser(data):
	soup = BeautifulSoup(data, 'lxml')
	tags = soup('div', class_ = 'WB_feed_type SW_fun S_line2 ')
	return tags

def parse_timeline(div):
	mid, tbInfo, mInfo, isForward, omid = info_parser(div)
	date, dateFormart, fromUrl, fromText = time_from_parser(div)
	text = content_parser(div)
	ouid, rouid = tbinfo_parser(tbInfo)
	timeline_dic = dict(
		zip(
			['mId', 'tbInfo', 'mInfo', 'isForward', 'oMId', 'date', 'dateFormart', 'fromUrl', 'fromText', 'text', 'userId', 'oUserId'],
			[mid, tbInfo, mInfo, isForward, omid, date, dateFormart, fromUrl, fromText, text, ouid, rouid]))
	return timeline_dic

def forward_weibo_parser(div):
	forward_div = div.find('div', class_ = 'WB_media_expand SW_fun2 S_line1 S_bg1')
	return forward_div

def parse_forward(forward_div):
	text = content_parser(forward_div)
	date, dateFormart, fromUrl, fromText = time_from_parser(forward_div)
	forward_dic = dict(
		zip(
			['oText', 'oDate', 'oDateFormart', 'oFromUrl', 'oFromText'],
			[text, date, dateFormart, fromUrl, fromText]))
	return forward_dic
def parse_timeline_full(div):
	timeline_dic = parse_timeline(div)
	if timeline_dic['isForward'] == 1:
		forward_div = forward_weibo_parser(div)
		forward_dic = parse_forward(forward_div)
		timeline_dic.update(forward_dic)
	return timeline_dic

def parse_user_timeline_pages(dbo_UserTimelinePages, dbo_UserTimelines):
	dbo = dbo_UserTimelinePages
	dbo2 = dbo_UserTimelines
	cursor = dbo.coll.find({},{'htmlStr': 1, 'userId': 1, 'pageUrl': 1})
	i = 0
	for c in cursor:
		if i%200 == 0:
			log('counter', str(i))
		data = load_json(c['htmlStr'])
		tags = divs_parser(data)
		for tag in tags:
			try:
				timeline_dic = parse_timeline_full(tag)
			except:
				print(data)
				print(tag)
				print(c['userId'])
				print(c['pageUrl'])
				raise
			# print(timeline_dic)
			mid = timeline_dic['mId']
			dbo2.coll.update({'mId': mid}, {'$set': timeline_dic}, upsert = True)
		i += 1
def main():
	log('parse_user_timeline_pages', 'running')
	dbo = dboperator.Dboperator(collname = 'UserTimelinePages')
	dbo2 = dboperator.Dboperator(collname = 'UserTimelines')
	parse_user_timeline_pages(dbo, dbo2)
	dbo.connclose()
	dbo2.connclose()
	log('parse_user_timeline_pages', 'finished')
main()
