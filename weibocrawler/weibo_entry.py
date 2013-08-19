#
#  weibo_entry.py
#
#  BurnedRobot 2013-08-01
#


#! /usr/bin/python3
# -*- encoding:utf-8 -*-

import re
import datetime
from weibocrawler.log import log
import json

class WeiboEntry:
    """
    Every weibo entry was extract from weibo webpage.
    This class can extract useful information from every weibo.
    """
    def __init__(self,content):
        self.__content = content

    def get_mid(self):
        _pattern = re.compile(r"""<dl class=\\\"feed_list\\\" mid=\\\"(?P<mid>[0-9]\w*)\\\" action-type=\\\"feed_list_item\\\" """)
        _match = _pattern.search(self.__content)
        _mid = _match.group('mid')
        return _mid

    def get_url(self):
        _pattern = re.compile(r'href=\\\"(?P<url>http:\\\/\\\/weibo\.com\\\/(?P<user_id>\d+)\\\/[\d\w]+)\\\" title')
        _match = _pattern.search(self.__content)
        _url = _match.group('url').replace('\/','/')
        _user_id = _match.group('user_id')
        return _url,_user_id

    def get_create_time(self):
        _pattern = re.compile(r'date=\\\"(?P<time>\d+)')
        _match = _pattern.search(self.__content)
        _timestamp = _match.group('time')

        _zh_timezone = datetime.timezone(datetime.timedelta(hours = 8))
        _time = datetime.datetime.fromtimestamp(int(_timestamp)/1000,_zh_timezone)
        return _time

    def get_text(self):
        _index_beg = self.__content.find('<p node-type=\\\"feed_list_content\\\">')
        _index_end = self.__content.find('<\\/p>',_index_beg)
        _text_block = self.__content[_index_beg:_index_end]

        _index_beg = _text_block.find('<em>')
        _index_beg = _index_beg + 4
        _index_end = _text_block.find('<\\/em>',_index_beg)
        _text_block = _text_block[_index_beg:_index_end]
        #log('_text_block',_text_block)
        _text_block = self.__filter_text(_text_block)
        return _text_block

    def get_forward_num(self):
        _index = self.__content.find('\\u8f6c\\u53d1')
        while -1 != _index:
       #     print(_index)
            _index_beg = self.__content.rfind('<',0,_index)
       #     print(_index_beg)
            _index_end = self.__content.find('>',_index)
       #     print(_index_end)
            _forward_content = self.__content[_index_beg:_index_end]
            if(-1 != _forward_content.find('action')):
       #         print("found!")
                break
            _index = self.__content.find('\\u8f6c\\u53d1',_index+1)

        _p_str = r'\\u8f6c\\u53d1' + r'\(?(?P<num>\d*)\)?'
        _pattern = re.compile(_p_str)
        _match = _pattern.search(_forward_content)
        if '' is _match.group('num'):
            return 0
        #print(_match.group('num'))
        #print()
        return _match.group('num')

    def get_reply_num(self):
        _index = self.__content.find('\\u8bc4\\u8bba')
        while -1 != _index:
        #    print(_index)
            _index_beg = self.__content.rfind('<',0,_index)
        #    print(_index_beg)
            _index_end = self.__content.find('>',_index)
        #    print(_index_end)
            _forward_content = self.__content[_index_beg:_index_end]
            if(-1 != _forward_content.find('action')):
        #        print("found!")
                break
            _index = self.__content.find('\\u8bc4\\u8bba',_index+1)

        _p_str = r'\\u8bc4\\u8bba' + r'\(?(?P<num>\d*)\)?'
        _pattern = re.compile(_p_str)
        _match = _pattern.search(_forward_content)
        if '' is _match.group('num'):
            return 0
        #print(_match.group('num'))
        #print()
        return _match.group('num')

    def get_nick_name(self):
        _pattern = re.compile(r'nick-name=\\\"(?P<nick_name>.*?)\\\"')
        _match = _pattern.search(self.__content)
        return _match.group('nick_name')

    def __filter_text(self,content):
        """
        filter html tag <...> from the weibo content text
        """
        _pattern = re.compile(r"""<.*?>""")
        content = _pattern.sub('',content)
        return content
