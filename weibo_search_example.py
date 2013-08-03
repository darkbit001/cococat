#
# weibo_search_example.py
#
# RobotFlying 2013-08-01
#

#! /usr/bin/python3
# -*- encoding:utf-8 -*-

import sys
from weibo_search import search
from weibo_login import WeiboLogin
from weibo_http_request import WeiboHttpRequest
from log import log

def print_weibo_info_list(input_list):
    for elem in input_list:
        log("",elem)
        log("",'\n')

def main():
    """Usage: python3 ./weibo_search_example.py [search_term]"""
    
    if len(sys.argv) < 2:
        print(main.__doc__)
        sys.exit(0)
    login = WeiboLogin('f641679@rmqkr.net','f641679')
    http_request = WeiboHttpRequest(login)

    weibo_info_list = search(http_request,sys.argv[1],10)
    print_weibo_info_list(weibo_info_list)

if "__main__" == __name__:
    main()
