import weibo_http_request
import weibo_login
import weibo_reply

if __name__ == '__main__':

    username = 'f641679@rmqkr.net'
    password = 'f641679'

    login = weibo_login.WeiboLogin(username, password)
    http_request = weibo_http_request.WeiboHttpRequest(login)
    print(weibo_reply.get_weibo_reply(http_request, 'http://e.weibo.com/1712312484/A2zsZqYnc'))