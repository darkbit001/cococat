import weibocrawler

if __name__ == '__main__':

    username = 'f641679@rmqkr.net'
    password = 'f641679'

    login = weibocrawler.WeiboLogin(username, password)
    http_request = weibocrawler.WeiboHttpRequest(login)
    messages = weibocrawler.get_weibo_user_timeline(http_request, '1197161814', 100)
    for message in messages:
    	weibocrawler.log("weibo_timeline_example", message)