import weibo_http_request
import weibo_login

if __name__ == '__main__':

    username = 'f641679@rmqkr.net'
    password = 'f641679'

    login = weibo_login.WeiboLogin(username, password)
    http_request = weibo_http_request.WeiboHttpRequest(login)
    print(http_request.get('http://weibo.com/p/aj/mblog/mbloglist?page=8&id=1005051403544953'))

