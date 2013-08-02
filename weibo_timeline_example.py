import weibo_http_request
import weibo_login
import weibo_timeline
import log

if __name__ == '__main__':

    username = 'f641679@rmqkr.net'
    password = 'f641679'

    login = weibo_login.WeiboLogin(username, password)
    http_request = weibo_http_request.WeiboHttpRequest(login)
    messages = weibo_timeline.get_weibo_user_timeline(http_request, '1197161814', 100)
    for message in messages:
    	log.log("weibo_timeline_example", message)