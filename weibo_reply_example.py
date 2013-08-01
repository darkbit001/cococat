import weibo_http_request
import weibo_login
import weibo_reply
import log

if __name__ == '__main__':

    username = 'f641679@rmqkr.net'
    password = 'f641679'

    login = weibo_login.WeiboLogin(username, password)
    http_request = weibo_http_request.WeiboHttpRequest(login)
    replies = weibo_reply.get_weibo_reply(http_request, 'http://weibo.com/1097414213/A2JkptPA9')
    for reply in replies:
    	log.log("weibo_reply_example", str(reply))