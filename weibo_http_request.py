#
# weibo_http_request.py
#
# ling0322 2013-07-31
#

import urllib.request
from io import BytesIO
import gzip

class WeiboHttpRequest:
    """
    WeiboHttpRequest simulates the broswer http GET/POST action

    Usage:

        login = WeiboLogin(your_username, your_password)
        http_request = WeiboHttpRequest(login)
        content = http_request.get(weibo_url)
    """

    def __init__(self, weibo_login):
        self.__cookies = weibo_login.get_cookie()

    def __build_header(self):
        header = dict()
        header['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        header['Accept-Encoding'] = 'gzip,deflate,sdch'
        header['Accept-Language'] = 'en-US,en;q=0.8'
        header['Connection'] = 'keep-alive'
        header['DNT'] = '1'
        header['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.71 Safari/537.36'
        header['Cookie'] = '; '.join(map(lambda t: '{0}={1}'.format(t[0], t[1]), self.__cookies.items()))

        return header

    def get(self, url):
        """
        A GET request to the url and returns the content of that url in str type
        """

        request = urllib.request.Request(url = url, headers = self.__build_header())
        fp = urllib.request.urlopen(request)
        http_message = fp.info()
        content = fp.read()
        fp.close()

        if http_message.get('Content-Encoding') == 'gzip':
            buf = BytesIO(content)
            f = gzip.GzipFile(fileobj = buf)
            content = f.read()

        return content.decode('utf-8')

    def post(self, url, data):
        """
        A POST request to the url and returns the content in str type

        Not implemented
        """

        return ""