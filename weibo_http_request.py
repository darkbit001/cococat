#
# weibo_http_request.py
#
# ling0322 2013-07-31
#

import urllib.request
from io import BytesIO
import gzip
import json
import os.path
import log

class WeiboHttpRequest:
    """
    WeiboHttpRequest simulates the broswer http GET/POST action

    Usage:

        login = WeiboLogin(your_username, your_password)
        http_request = WeiboHttpRequest(login)
        content = http_request.get(weibo_url)
    """

    COOKIES_FILE = 'cookies.json'

    def __init__(self, weibo_login):
        if self.__load_cookies() == False:
            log.log("http_request", "get cookies from weibo.com")
            self.__cookies = weibo_login.get_cookie()
            if self.__cookies == None:
                raise Exception("Unable to get cookie")
            self.__dump_cookies()

    def __dump_cookies(self):
        with open(self.COOKIES_FILE, 'w') as fp:
            json.dump(self.__cookies, fp)

    def __load_cookies(self):
        """
        Load cookies form local COOKIES_FILE and validate it
        Return True if cookies is valid, vise versa
        """

        if os.path.exists(self.COOKIES_FILE) == True:
            log.log("http_request", "load cookies from local file.")
            try: 
                with open(self.COOKIES_FILE) as fp:
                    self.__cookies = json.load(fp)
            except Exception as e:
                log.log("http_request", str(e))
                return False
            try:
                if self.__check_cookie_validation() == True:
                    log.log("http_request", "cookies loaded.")
                    return True
                else:
                    log.log("http_request", "local cookie is invalid.")
            except:
                log.log("http_request", "local cookie is invalid.")

        return False


    def __check_cookie_validation(self):
        content = self.get('http://www.weibo.com')
        if content.find('nameBox') == -1:
            return False
        else:
            return True

    def __build_header(self, enable_cookie):
        header = dict()
        header['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        header['Accept-Encoding'] = 'gzip,deflate,sdch'
        header['Accept-Language'] = 'en-US,en;q=0.8'
        header['Connection'] = 'keep-alive'
        header['DNT'] = '1'
        header['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.71 Safari/537.36'
        if enable_cookie == True:
            header['Cookie'] = '; '.join(map(lambda t: '{0}={1}'.format(t[0], t[1]), self.__cookies.items()))

        return header

    def get(self, url, enable_cookie = True):
        """
        A GET request to the url and returns the content of that url in str type
        """

        log.log("http_request", "GET {0}".format(url))

        request = urllib.request.Request(url = url, headers = self.__build_header(enable_cookie))
        fp = urllib.request.urlopen(request)
        http_message = fp.info()
        content = fp.read()
        fp.close()
        
        content_len = len(content)
        log.log("http_request", "GET {0} ... OK {1} Bytes".format(url, content_len))

        if http_message.get('Content-Encoding') == 'gzip':
            buf = BytesIO(content)
            f = gzip.GzipFile(fileobj = buf)
            content = f.read()
            log.log("http_request", "unzip {0} -> {1}".format(content_len, len(content)))
        
        return content.decode('utf-8')

    def post(self, url, data):
        """
        A POST request to the url and returns the content in str type

        Not implemented
        """

        return ""