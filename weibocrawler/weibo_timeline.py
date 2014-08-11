#
# weibo_timeline.py
#
# ling0322 2013-08-02
#

from weibocrawler.weibo_struct import Message
import re
from weibocrawler import log
import json
import datetime
import time
import random

__USER_HOMEPAGE_URL = 'http://weibo.com/{0}'
__MESSAGE_PAGE_URL = 'http://weibo.com/p/aj/mblog/mbloglist?page={page}&id={page_id}'

__re_page_id = re.compile(r"\$CONFIG\['page_id'\]='(\d+?)';")
__re_screen_name = re.compile(r"\$CONFIG\['onick'\]='(.+?)'; ")
__re_text = re.compile(r'<div class="WB_detail">.*?<div class="WB_text" .*?>(.*?)</div>', re.DOTALL)
__re_forward = re.compile(r'<a  action.*?>转发\((\d+)\)</a>', re.DOTALL)
__re_reply = re.compile(r'<a suda.*?>评论\((\d+)\)</a>', re.DOTALL)
__re_create_at = re.compile(r'<a name.+?date="(\d+)"')
__re_mid = re.compile(r'<a name=(\d+) target')
__re_tag = re.compile(r'<.*?>', re.DOTALL)

__zh_timezone = datetime.timezone(datetime.timedelta(hours = 8))

def __timestamp_to_datetime_str(timestamp):
    d = datetime.datetime.fromtimestamp(timestamp, __zh_timezone)
    return d.strftime("%Y-%m-%d %H:%M:%S")

def get_timeline_page(http_request, page_id, page):
    page_json = http_request.get(__MESSAGE_PAGE_URL.format(page = page, page_id = page_id))
    page_obj = json.loads(page_json)
    page_html = page_obj['data']

    text_list = __re_text.findall(page_html)
    text_list = list(map(lambda text: __re_tag.sub('', text).strip(), text_list))

    forward_list = __re_forward.findall(page_html)
    forward_list = list(map(lambda x: int(x), forward_list))

    reply_list = __re_reply.findall(page_html)
    reply_list = list(map(lambda x: int(x), reply_list))

    create_at_list = __re_create_at.findall(page_html)
    create_at_list = list(map(lambda x: __timestamp_to_datetime_str(int(x) / 1000), create_at_list))

    mid_list = __re_mid.findall(page_html)
    mid_list = list(map(lambda x: int(x), mid_list))
    
    #print(len(text_list), len(forward_list), len(reply_list), len(create_at_list), len(mid_list))
    count = len(text_list) + len(create_at_list) + len(mid_list)
    if len(text_list) * 3 != count:
        raise Exception('Extract timeline message error')

    return text_list, create_at_list, mid_list


def get_weibo_user_timeline(http_request, user_id, max_count = 100):
    user_homepage_html = http_request.get(__USER_HOMEPAGE_URL.format(user_id))

    # Get page_id from user's homepage

    match = __re_page_id.search(user_homepage_html)
    if match == None:
        raise Exception("Unable to get user's page_id")

    page_id = match.group(1)
    log("weibo_timeline", "user's page_id is : " + page_id)

    # Get screen_name from user's homepage

    match = __re_screen_name.search(user_homepage_html)
    if match == None:
        raise Exception("Unable to get user's screen_name")

    screen_name = match.group(1)
    log("weibo_timeline", "user's screen_name is : " + screen_name) 

    message_list = []
    print('Have a rest in 5 second.')
    for x in range(1,6):
        print(str(6-x) + ' s')
        time.sleep(1)

    for page in range(1, 100):
        text_list, create_at_list, mid_list = get_timeline_page(http_request, page_id, page)
        print('The length of text_list : ' + str(len(text_list)))
        if len(text_list) == 0:
            print('No more text_list in page '+ str(page))
            return message_list
        else:
            for i in range(len(text_list)):
                message = Message(
                    user_id = user_id,
                    screen_name = screen_name,
                    create_time = create_at_list[i],
                    url = "",
                    mid = mid_list[i],
                    forward_count = 0,
                    reply_count = 0,
                    text = text_list[i])
                message_list.append(message)
                print('Page ' + str(page) + '. The length of message_list : ' +str(len(message_list)))

        if max_count < len(message_list):
            print('The message_list has over 100 items.')
            return message_list

        sleeptime = random.randint(10,40)
        print('Sleeptime : ' + str(sleeptime) +' s')
        time.sleep(sleeptime)

    return message_list





