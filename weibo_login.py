#
# weibo_login.py
#
# ling0322 2013-07-31
#

class WeiboLogin:
    """
    WeiboLogin simulates the weibo login behavior with username and password, and finally 
    get the cookies for the later http requests

    Usage:

        login = WeiboLogin(your_username, your_password)
        cookies_str = login.get_cookies()
    """

    def __init__(self, username, password):
        self.__username = username
        self.__password = password

    def get_cookies():
        """
        Not Implemented 
        """

        return "_s_tentry=-; Apache=4143019942566.7524.1375238457760; SINAGLOBAL=4143019942566.7524.1375238457760; ULV=1375238457767:1:1:1:4143019942566.7524.1375238457760:; SUE=es%3D7a48552d3071e5bd379dbc2b027914c4%26ev%3Dv1%26es2%3D4889ae95d6c92e300712f208dc26ca7e%26rs0%3DFtKkhNT3EF9BjL2OGWCwJ4lBDtWU3pXcfArtEdKPBUzZPAyocc%252FZj%252F%252F4LkodAQmCQqzhpL%252FrYA2BUaDpkMvs%252B1aUlnSb2Cc32MKie%252FVMahC1FuROmEr4lgbn6Y3aafl%252BMwV2MwmJO3CYgsr%252BoBXk%252BqHF%252FB1V6f9%252BLhZVDOGaHr4%253D%26rv%3D0; SUP=cv%3D1%26bt%3D1375238478%26et%3D1375324878%26d%3Dc909%26i%3D0660%26us%3D1%26vf%3D0%26vt%3D0%26ac%3D0%26st%3D0%26uid%3D2605372777%26name%3D327716067%2540qq.com%26nick%3DYukiBot%26fmp%3D%26lcp%3D2012-10-16%252011%253A16%253A23; SUS=SID-2605372777-1375238478-XD-hl5t8-c5974593b001f256525011383dc2680a; ALF=1377830477; SSOLoginState=1375238478; wvr=5"