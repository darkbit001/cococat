#
# log.py
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
    datetime_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logstr = "[{0}] {1}: {2}".format(datetime_str, tag, text)
    '''
    f = open('log' + datetime.datetime.now().strftime("%Y%m%d%H"), 'a')
    f.write(logstr)
    f.close()
    '''
    print(logstr)
