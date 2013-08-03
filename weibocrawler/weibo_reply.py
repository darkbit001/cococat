#
# weibo_reply.py
#
# ling0322 2013-08-01
#

from weibocrawler.weibo_struct import Reply
import re
from weibocrawler.log import log
import json
import time
import datetime



__REPLY_URL_BASE = 'http://www.weibo.com/aj/comment/big?id={0}&page={1}'
__re_weibo_mid = re.compile(r'&mid=(\d+)&')
__re_dd = re.compile(r'<dd>.*?</dd>', re.DOTALL)
__re_reply_user = re.compile(r'<a href="/.*?" title="(.*?)" usercard="id=(\d+)">.*?</a>')
__re_reply_text = re.compile(r'</a>：(.*?)<span class="S_txt2">', re.DOTALL)
__re_tag = re.compile(r'<.*?>', re.DOTALL)
__re_reply_time = re.compile(r'<span class="S_txt2">\((.*?)\)</span>')

__re_time_second = re.compile(r'(\d+)秒前')
__re_time_minute = re.compile(r'(\d+)分钟前')
__re_time_today = re.compile(r'今天 (\d+):(\d+)')
__re_time_full_no_year = re.compile(r'(\d+)月(\d+)日 (\d+):(\d+)')
__re_time_full = re.compile(r'(\d+)-(\d+)-(\d+) (\d+):(\d+)')

def __extract_mid(html_content):
    """
    Return mid as string from weibo page
    """

    match = __re_weibo_mid.search(html_content)
    if match == None:
        raise Exception('Unable to extrace mid from page')

    return match.group(1)

def __extrace_html_from_json(json_text):
    json_obj = json.loads(json_text)
    return json_obj.get("data", {}).get("html", "")

def __calculate_reply_time(reply_time_str):
    current_timespamp = int(time.time() * 1000)
    zh_timezone = datetime.timezone(datetime.timedelta(hours = 8))
    now = datetime.datetime.now(zh_timezone)
    reply_datetime = None

    # XX秒前
    match = __re_time_second.match(reply_time_str)
    if match != None:
        seconds_before = int(match.group(1))
        reply_datetime = now - datetime.timedelta(seconds = seconds_before)

    # XX分钟前
    match = __re_time_minute.match(reply_time_str)
    if match != None:
        minutes_before = int(match.group(1))
        reply_datetime = now - datetime.timedelta(minutes = minutes_before)

    # 今天 XX:XX
    match = __re_time_today.match(reply_time_str)
    if match != None:
        hour = int(match.group(1))
        minute = int(match.group(2))
        reply_datetime = datetime.datetime(
            now.year,
            now.month,
            now.day,
            hour,
            minute,
            tzinfo = zh_timezone)

    # X月X日 XX:XX
    match = __re_time_full_no_year.match(reply_time_str)
    if match != None:
        month = int(match.group(1))
        day = int(match.group(2))
        hour = int(match.group(3))
        minute = int(match.group(4))
        reply_datetime = datetime.datetime(
            now.year,
            month,
            day,
            hour,
            minute,
            tzinfo = zh_timezone)

    # XXXX-XX-XX XX:XX
    match = __re_time_full.match(reply_time_str)
    if match != None:
        year = int(match.group(1))
        month = int(match.group(2))
        day = int(match.group(3))
        hour = int(match.group(4))
        minute = int(match.group(5))
        reply_datetime = datetime.datetime(
            year,
            month,
            day,
            hour,
            minute,
            tzinfo = zh_timezone)   

    if reply_datetime == None:
        raise Exception('Unable to parse reply time')

    return reply_datetime.strftime("%Y-%m-%d %H:%M:%S")


def __get_reply_at_page(http_request, mid, page):
    url = __REPLY_URL_BASE.format(mid, page)
    content_json = http_request.get(url)
    content_html = __extrace_html_from_json(content_json)

    dd_list = __re_dd.findall(content_html)
    reply_list = []
    for dd_text in dd_list:
        match = __re_reply_user.search(dd_text)
        if match == None:
            raise Exception('Unable to extract user information from page')

        user_id = int(match.group(2))
        screen_name = match.group(1)

        match = __re_reply_text.search(dd_text)
        if match == None:
            raise Exception('Unable to extract text from page')

        text = match.group(1)
        text = __re_tag.sub('', text).strip()

        match = __re_reply_time.search(dd_text)
        if match == None:
            raise Exception('Unable to extract time from page')

        reply_at = match.group(1)
        reply_at_parsed = __calculate_reply_time(reply_at)

        reply = Reply(user_id, screen_name, text, reply_at_parsed)
        # log("weibo_reply", reply)
        reply_list.append(reply)

    return reply_list


def get_weibo_reply(http_request, weibo_url, reply_max = 200):
    """
    get_weibo_reply returns a weibo's replies from its url

    @param http_request The http_request is an instance of WeiboHttpRequest
    @param weibo_url The url of the weibo
    @param reply_max Max number of replies 

    returns a list of Reply
    """
    
    main_content = http_request.get(weibo_url)
    mid = __extract_mid(main_content)
    count = 0
    weibo_reply = []
    for page in range(1, 100):
        reply_list = __get_reply_at_page(http_request, mid, page)
        log("weibo_reply", "GET {0} replies from page {1}".format(len(reply_list), page))
        weibo_reply.extend(reply_list)
        count += len(reply_list)
        if len(reply_list) == 0 or count >= reply_max:
            break

    return weibo_reply[: 200]



