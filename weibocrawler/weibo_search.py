#
# weibo_search.py
#
# BurnedRobot 2013-08-01
#
#       Modified by BurnedRobot at 2013-08-03: 
#       search(http_request, input_term, page_limits) ===> search(http_request, input_term, max_num)
#
#

#! /usr/bin/python3
#! -*- encoding:utf-8 -*-

from weibocrawler.weibo_http_request import WeiboHttpRequest
from weibocrawler.weibo_login import WeiboLogin
from weibocrawler.weibo_page_analysis import WeiboPageAnalyzer
from weibocrawler.weibo_info import WeiboInfo
from weibocrawler.log import log
import urllib.parse 

def search(http_request, input_term, max_num):
    """
    search function simulates users` search action of specific topic
    http request must be initialized before search

    Usage:

    login = WeiboLogin('f641679@rmqkr.net', 'f641679')
    http_request = WeiboHttpRequest(login)
    weibo_info_list = search(http_request, '天一', 10)   # will get the first 10 weibo messages

    """
    page = 1
    weibo_info_list = []
    
    num = len(weibo_info_list)

    while num <= max_num:
        request_url = 'http://s.weibo.com/weibo/' + urllib.parse.quote(input_term) + '&pages=' + str(page)
        content = http_request.get(request_url, enable_cookie = False)

        #log('content',content)
        analyzer = WeiboPageAnalyzer(content)
        analyzer.analyze()
        #analyzer.print_weibo_info_list()

        temp_list = analyzer.get_weibo_info_list()
        weibo_info_list = weibo_info_list + temp_list
        num = num + len(temp_list)
        page = page + 1

    fanal_list = weibo_info_list[:max_num]
        
    return fanal_list

