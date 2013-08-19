#
# weibo_info.py
#
# BurnedRobot 2013-08-01
#

#! /usr/bin/python3
# -*- encoding:utf-8 -*-

from weibocrawler.weibo_entry import WeiboEntry
from weibocrawler.weibo_struct import Message
from weibocrawler.log import log

class WeiboInfo:
    """
    WeiboInfo is a data struct to store data cralwed from webpages
    """

    def __init__(self,weibo_entry):
        self.__mid = weibo_entry.get_mid()
        self.__url,self.__user_id = weibo_entry.get_url()
        self.__time = weibo_entry.get_create_time()
        self.__nick_name = weibo_entry.get_nick_name()
        self.__text = weibo_entry.get_text()
        self.__forward_num = weibo_entry.get_forward_num()
        self.__reply_num = weibo_entry.get_reply_num()

    def print(self):
        log("mid",self.__mid)
        log("url",self.__url)
        log("nick-name",self.__nick_name)
        log("user_id",self.__user_id)
        log("time",self.__time)
        log("forward_num",self.__forward_num)
        log("reply_num",self.__reply_num)
        log("text",self.__text)

    def convert_to_message(self):
        return Message(self.__user_id,
                       self.__nick_name,
                       self.__time,
                       self.__url,
                       self.__mid,
                       self.__forward_num,
                       self.__reply_num,
                       self.__text)

    def get_mid(self):
        return self.__mid

    def get_url(self):
        return self.__url

    def get_nick(self):
        return self.__nick_name

    def get_user_id(self):
        return self.__user_id

    def get_create_time(self):
        return self.__time

    def get_text(self):
        return self.__text

    def get_forward_num(self):
        return self.__forward_num

    def get_reply_num(self):
        return self.__reply_num

