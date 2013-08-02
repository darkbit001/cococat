#
# weibo_follow_example.py
#
# RobotFlying 2013-08-02
#

#! /usr/bin/python3
# -*- encoding:utf-8 -*-

import sys
from weibo_login import WeiboLogin
from weibo_http_request import WeiboHttpRequest
from weibo_follow import get_follow_list
from log import log


def main():

    if len(sys.argv) < 2:
        print("Usage: python3 ./weibo_follow_example.py [user_id]")
        sys.exit(0)

    login = WeiboLogin('f641679@rmqkr.net', 'f641679')
    http_request = WeiboHttpRequest(login)
    follow_list = get_follow_list(http_request, sys.argv[1])
    log('length of follow_list', len(follow_list))
    log('follow_list',follow_list)


if '__main__' == __name__:
    main()

