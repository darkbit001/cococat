import weibocrawler

if __name__ == '__main__':

    username = 'f641679@rmqkr.net'
    password = 'f641679'

    login = weibocrawler.WeiboLogin(username, password)
    http_request = weibocrawler.WeiboHttpRequest(login)
    replies = weibocrawler.get_weibo_reply(http_request, 'http://weibo.com/1097414213/A2JkptPA9')
    for reply in replies:
    	weibocrawler.log("weibo_reply_example", str(reply))