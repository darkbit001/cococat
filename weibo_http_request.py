#
# weibo_http_request.py
#
# ling0322 2013-07-31
#


class WeiboHttpRequest:
    """
    WeiboHttpRequest simulates the broswer http GET/POST action

    Usage:

        login = WeiboLogin(your_username, your_password)
        http_request = WeiboHttpRequest(login)
        content = http_request.get(weibo_url)
    """

    def __init__(self, login):
        self.__weibo_login = login

    def get(url):
        """
        A GET request to the url and returns the content of that url in str type

        Not implemented !!!
        """

        return ""

    def post(url, data):
        """
        A POST request to the url and returns the content in str type

        Not implemented
        """

        return ""