#
# weibo_http_request.py
#
# ling0322 2013-07-31
#

import datetime

def log(tag, text):
    """
    Add a log 

    Usage:

        log("login", "login error")
        log("http_request", "404 page not found")
    """
    datetime_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%m:%S")
    print("[{0}] {1}: {1}".format(datetime_str, tag, text))
    