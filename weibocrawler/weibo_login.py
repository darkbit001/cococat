#
# weibo_login.py
#
# ling0322 2013-07-31
#

import urllib.request
from urllib.parse import urlencode
import base64
import rsa
import re
import json
import binascii


class WeiboLogin:
    """
    WeiboLogin simulates the weibo login behavior with username and password, and finally 
    get the cookies for the later http requests

    Usage:

        login = WeiboLogin(your_username, your_password)
        cookies = login.get_cookies()
    """

    LOGIN_URL = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.11)'
    SSOLOGIN_JS_URL = 'http://login.sina.com.cn/sso/prelogin.php?entry=sso&callback=sinaSSOController.preloginCallBack&rsakt=mod&client=ssologin.js(v1.4.11)'
    PUBKEY = 'EB2A38568661887FA180BDDB5CABD5F21C7BFD59C090CB2D245A87AC253062882729293E5506350508E7F9AA3BB77F4333231490F915F6D63C55FE2F08A49B353F444AD3993CACC02DB784ABBB8E42A9B1BBFFFB38BE18D78E87A0E41B9B8F73A928EE0CCEE1F6739884B9777E4FE9E88A1BBE495927AC4A799B3181D6442443'
    RSAKV = '1330428213'
    CALLBACK_URL = 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack'

    def __init__(self, username, password):
        self.__username = username
        self.__password = password

    def __prelogin(self):
        """
        prelogin returns server_time and nonce for login crypto
        """

        fp = urllib.request.urlopen(self.SSOLOGIN_JS_URL)
        content = fp.read()
        fp.close()

        content = content.decode('utf-8')
        json_data = re.search('\((.*)\)', content).group(1)
        data = json.loads(json_data)
        server_time = str(data['servertime'])
        nonce = data['nonce']
        return server_time, nonce

    def __encrypt_username(self, username):
        username_quoted = urllib.parse.quote(username)
        username_encrypted = base64.encodestring(username_quoted.encode('utf-8'))[:-1]
        return username_encrypted.decode('utf-8')

    def __encrypt_password(self, password, server_time, nonce):
        rsa_public_key = int(self.PUBKEY, 16)
        key = rsa.PublicKey(rsa_public_key, 65537)
        message = str(server_time) + '\t' + str(nonce) + '\n' + str(password)
        message_bytes = message.encode('utf-8')
        passwd = rsa.encrypt(message_bytes, key)
        return binascii.b2a_hex(passwd).decode('utf-8')

    def __build_login_form_data(self, encryptd_username, encrypted_password, server_time, nonce):
        return {
            'entry': 'weibo',
            'gateway': '1',
            'from': '',
            'savestate': '7',
            'userticket': '1',
            'ssosimplelogin': '1',
            'vsnf': '1',
            'vsnval': '',
            'su': encryptd_username,
            'service': 'miniblog',
            'servertime': server_time,
            'nonce': nonce,
            'pwencode': 'rsa2',
            'sp': encrypted_password,
            'encoding': 'UTF-8',
            'prelt': '115',
            'rsakv' : self.RSAKV,
            'url': self.CALLBACK_URL,
            'returntype': 'META'
        }

    def __parse_cookie(self, http_message):
        cookies_dict = {}
        for key, value in http_message.items():
            if key == 'Set-Cookie':
                cookie_line = value[: value.find(';')]
                fields = cookie_line.split('=')
                cookies_dict[fields[0]] = fields[1]

        return cookies_dict




    def get_cookie(self):
        try:
            server_time, nonce = self.__prelogin()
            encryptd_username = self.__encrypt_username(self.__username)
            encrypted_password = self.__encrypt_password(self.__password, server_time, nonce)
            form_data = self.__build_login_form_data(encryptd_username, encrypted_password, server_time, nonce)
            
            request  = urllib.request.Request(url = self.LOGIN_URL, data = urlencode(form_data).encode('utf-8'))
            fp = urllib.request.urlopen(request)
            content = fp.read()
            fp.close()

            content = content.decode('gbk')
            match = re.search('location\.replace\(\"(.*?)\"\)', content)
            callback_url = match.group(1)

            fp = urllib.request.urlopen(callback_url)
            content = fp.read()
            cookie_dict = self.__parse_cookie(fp.info())
            fp.close()

            if 'SUE' in cookie_dict and cookie_dict['SUE'] != 'deleted':
                return cookie_dict
        except e:
            print(e)

        return None



