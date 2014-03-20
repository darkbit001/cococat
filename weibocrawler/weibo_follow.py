#
# weibo_following.py
#
# BurnedRobot 2013-08-02
#

#! /usr/bin/python3
# -*-encoding:utf-8 -*-

import re,sys,time
from weibocrawler.weibo_profile import WeiboProfile
from weibocrawler import log
import time
import random

def get_max_page_num(content):

    _pattern = re.compile(r'page=(?P<page_num>\d+)')
    _page_list = _pattern.findall(content)
    log('page_list',_page_list)
    _page_list = [ int(x) for x in _page_list ]

    if not _page_list:
        return 1

    return max(_page_list)


def get_page_id(http_request, user_id):

    _url = 'http://weibo.com/u/' + str(user_id)
    log('url',_url)
    sleeptime = random.randint(2,5)
    log('get_page_id sleeptime', sleeptime)
    time.sleep(sleeptime)
    _content = http_request.get(_url)

    _pattern = re.compile(r'\\\/p\\\/(?P<page_id>\d*)')
    _match = _pattern.search(_content)
    _page_id = _match.group('page_id')
    log('page_id',_page_id)


    return _page_id 


def get_content_from_pageid(http_request, page_id, page_num, flag = False):

    _url = 'http://weibo.com/p/' + str(page_id)                             \
           +'/follow?pids=Pl_Official_LeftHisRelation__15&'                 \
           + (flag and ['relate=fans&'] or [''])[0] + 'page='               \
           + str(page_num) + '#place'

    log('url',_url)
    sleeptime = random.randint(2,5)
    log('get_page_id sleeptime', sleeptime)
    time.sleep(sleeptime)
    _content = http_request.get(_url)

    return _content 


def get_follow_list(http_request, user_id, flag = False):
    """
    This function will get following or follower users.
    
    Parameter:
        http_request:   a http_request instance
        user_id:        the user id of one whose following or followers that you want get
        flag:           [default: False] in default case, this function will retrive following users.
                        when flag is set to True, it will retrive follower user.

    Return Value:
        a list of following or follower

    Usage:
        login = WeiboLogin('f641679@rmqkr.net', 'f641679')
        http_request = WeiboHttpRequest(login)
        follow_list = get_follow_list(http_request, 3330370692)
        log('follow_list', len(follow_list))

    """
    
    _page_id = get_page_id(http_request, user_id)
    _content = get_content_from_pageid(http_request, _page_id, 1, flag)
    _max_page_num = get_max_page_num(_content)

    _follow_list = []
    
    i = 1 
    while i <= _max_page_num:
        #log('page',i)
        #time.sleep(3)

        _content = get_content_from_pageid(http_request, _page_id, i, flag)
        _profile = WeiboProfile(_content)

        _temp_list = _profile.get_list(flag)
        log('length of temp list',len(_temp_list))
        _follow_list = _follow_list + _temp_list
        i = i + 1

    return _follow_list
