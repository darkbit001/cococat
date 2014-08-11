#
# weibo_page_analysis.py
#
# BurnedRobot 2013-07-31
#

#! /usr/bin/python3
# -*- encoding:utf-8 -*-

import re,sys
from weibocrawler.weibo_entry import WeiboEntry 
from weibocrawler.weibo_info import WeiboInfo
from weibocrawler.log import log

class WeiboPageAnalyzer:
    """
    WeiboPageAnalyzer make an analysis of weibo webpages in a type of string.

    Usage:
        analyzer = WeiboPageAnalyzer(content)
        analyzer.analyze()
        analyzer.print_weibo_info_list()
        info_list = analyzer.get_weibo_info_list()
    """

    def __init__(self,content):
        self.__content = content
        self.__weibo_info_list = []

    def analyze(self):
        """
        Analyze function will analyze input content and
        store the info extracted from input content into a list
        """
        i = 0
        _weibo_tuple = (0,0,"")
        _weibo_tuple_list = []

        while True:
            #print(_weibo_tuple[1])
            _weibo_dict = {}
            _weibo_tuple = self.__extract_weibo_entry(_weibo_tuple[1]) 
            if(-1 == _weibo_tuple[0]): 
                break
            _entry = WeiboEntry(_weibo_tuple[2])
            _entry.print()
            self.__weibo_info_list.append(WeiboInfo(_entry).convert_to_message())

    def __extract_weibo_entry(self,beg):
        """
        To slit the whole content into every weibo entry
        Return value:
            a tuple includes three elems
            _index_beg: the begin index of weibo entry
            _index_end: the end index of weibo entry
            _weibo_entry: weibo entry content
        """
        _index_beg = self.__content.find('<dl class=\\\"feed_list\\\"',beg)
        #log('index_beg:',_index_beg)
        if(-1 == _index_beg):
            #print("Not found this string!")
            return (-1,-1,"")
        _index_end = self.__content.find('<dl class=\\\"feed_list\\\"',_index_beg+1)
        _index_end = _index_end - 1
        #log('index_end',_index_end)
        _weibo_entry = self.__content[_index_beg:_index_end]
        #log('weibo_entry',_weibo_entry)
        return (_index_beg,_index_end,_weibo_entry)

    def get_weibo_info_list(self):
        return self.__weibo_info_list

    def print_weibo_info_list(self):
        for _elem in self.__weibo_info_list:
            #_elem.print()
            log("weibo_page_analysis",_elem)
            log("","\n")
