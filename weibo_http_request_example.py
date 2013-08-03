import weibocrawler

if __name__ == '__main__':

    username = 'f641679@rmqkr.net'
    password = 'f641679'

    login = weibocrawler.WeiboLogin(username, password)
    http_request = weibocrawler.WeiboHttpRequest(login)
    print(http_request.get('http://weibo.com/p/aj/mblog/mbloglist?page=8&id=1005051403544953'))

