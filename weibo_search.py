#
# weibo_search.py
#
# RobotFlying 2013-08-01
#

#! /usr/bin/python3
#! -*- encoding:utf-8 -*-

from weibo_http_request import WeiboHttpRequest
from weibo_login import WeiboLogin
from weibo_page_analysis import WeiboPageAnalyzer
from weibo_info import WeiboInfo
from log import log
import urllib.parse 

def search(http_request,input_term,page_limits):
    """
    search function simulates users` search action of specific topic
    http request must be initialized before search

    Usage:

    login = WeiboLogin('f641679@rmqkr.net','f641679')
    http_request = WeiboHttpRequest(login)
    weibo_info_list = search(http_request,'天一',10)

    """
    page = 1
    weibo_info_list = []

    while page <= page_limits:
        request_url = 'http://s.weibo.com/weibo/' + urllib.parse.quote(input_term) + '&pages=' + str(page)
        content = http_request.get(request_url)

        #log('content',content)
        analyzer = WeiboPageAnalyzer(content)
        analyzer.analyze()
        #analyzer.print_weibo_info_list()

        temp_list = analyzer.get_weibo_info_list()
        weibo_info_list = weibo_info_list + temp_list
        log('length of weibo_info_list',len(weibo_info_list))
        page = page + 1
        
    return weibo_info_list

