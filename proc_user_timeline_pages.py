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
	cursor = dbo.coll.find({'userId': '1088602681'},{'htmlStr': 1, 'userId': 1, 'pageUrl': 1})
	# cursor2 = dbo2.coll.distinct('mId')
	log('Total pages', str(cursor.count()))
	counter = 0
	for c in cursor:
		# if counter%200 == 0:
			# log('counter', str(counter))
		try:
			data = load_json(c['htmlStr'])
		except:
			# log('error', '1')
			continue
		try:
			tags = divs_parser(data)
		except:
			# log('error', '2')
			continue
		print(c['pageUrl'])
		counter2 = 0
		for tag in tags:
			timeline_dic = parse_timeline_full(tag)
			# print(timeline_dic)
			mid = timeline_dic['mId']
			# result = dbo2.coll.find({'mId': mid}, {'mId': 1}).count()
			# if mid in cursor2:
				# continue
			# dbo2.coll.update({'mId': mid}, {'$set': timeline_dic}, upsert = True)
			
			counter2 += 1
		print(counter2)
		counter += 1
	log('Processed pages', str(counter))
def main():
	from weibocrawler.config import getconfig
	cfg = getconfig()
	Collection_UserTimelinePages = cfg['Collections']['UserTimelinePages']
	Collection_UserTimelines = cfg['Collections']['UserTimelines']
	log('parse_user_timeline_pages', 'Running')
	# dbo = dboperator.Dboperator(collname = 'UserTimelinePages')
	# dbo2 = dboperator.Dboperator(collname = 'UserTimelines')
	dbo1 = dboperator.Dboperator(collname = Collection_UserTimelinePages)
	dbo2 = dboperator.Dboperator(collname = Collection_UserTimelines)
	parse_user_timeline_pages(dbo1, dbo2)
	dbo1.connclose()
	dbo2.connclose()
	log('parse_user_timeline_pages', 'Finished')
main()
