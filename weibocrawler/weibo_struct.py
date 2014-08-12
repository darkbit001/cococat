#
# struct.py
#
# ling0322 2013-08-02
#



class Message:
    def __init__(self, user_id, screen_name, create_time, url, mid, forward_count, reply_count, text):
        self.user_id = user_id
        self.screen_name = screen_name
        self.create_time = create_time
        self.url = url
        self.mid = mid
        self.forward_count = forward_count
        self.reply_count = reply_count
        self.text = text

    def __repr__(self):
        return """Message(user_id = {0}, screen_name = "{1}", create_time = "{2}", url = "{3}", mid = {4}, forward_count = {5}, reply_count = {6}, text  = "{7}")""".format(
            self.user_id,
            self.screen_name,
            self.create_time,
            self.url,
            self.mid,
            self.forward_count,
            self.reply_count,
            self.text)

    def __str__(self):
        return "@{0}: {2}; at {1}; Foward={3}; Reply={4}; mid={5}".format(
            self.screen_name, 
            self.create_time, 
            self.text,
            self.forward_count,
            self.reply_count,
            self.mid)

class Reply:
    def __init__(self, user_id, screen_name, text, reply_at):
        self.user_id = user_id
        self.screen_name = screen_name
        self.text = text
        self.reply_at = reply_at

    def __repr__(self):
        return 'Reply(user_id = {0}, screen_name = "{1}", text = "{2}", reply_at = "{3}")'.format(
            self.user_id,
            self.screen_name,
            self.text,
            self.reply_at)

class User:
    def __init__(self, user_id, screen_name, gender):
        self.user_id = user_id
        self.screen_name = screen_name
        self.gender = gender

    def __repr__(self):
        return 'User(user_id = {0}, screen_name = "{1}", gender = "{2}")'.format(
            self.user_id,
            self.screen_name,
            self.gender)    
# class UserClawer(User):
class UserProfile(User):
    def __init__(self, user_id, screen_name, gender, follower_num, following_num, weibo_num, member_type, member_level):
        super(User,self).__init__(user_id, screen_name, gender)
        self.follower_num = follower_num
        self.following_num = following_num
        self.weibo_num = weibo_num
        self.member_type = member_type
        self.member_level = member_level
    def __repr__(self):
        return 'UserProfile(user_id = {0}, screen_name = "{1}", gender = "{2}", follower_num = "{3}", following_num = "{4}", weibo_num = "{5}", member_type = "{6}", member_level = "{7}")'.format(
            self.user_id,
            self.screen_name,
            self.gender,
            self.follower_num,
            self.following_num,
            self.weibo_num,
            self.member_type,
            self.member_level)

class Follower(User):
    def __init__(self, user_id, screen_name, gender, follow_path, follow_path_url, following_user_id):
        super(Follower, self).__init__(user_id, screen_name, gender)
        self.follow_path = follow_path
        self.follow_path_url = follow_path_url
        self.following_user_id = following_user_id
    def __repr__(self):
        return 'Follower(user_id = {0}, screen_name = "{1}", gender = "{2}", follow_path = "{3}", follow_path_url = "{4}", following_user_id = "{5}")'.format(                              # modified by BurnedRobot at 2013-08-03
            self.user_id,
            self.screen_name,
            self.gender,
            self.follow_path,
            self.follow_path_url,
            self.following_user_id)

class Following(User):
    def __init__(self, user_id, screen_name, gender, follow_path, follow_path_url, follower_user_id):
        super(Following, self).__init__(user_id, screen_name, gender)
        self.follow_path = follow_path
        self.follow_path_url = follow_path_url
        self.follower_user_id = follower_user_id

    def __repr__(self):
        return 'Following(user_id = {0}, screen_name = "{1}", gender = "{2}", follow_path = "{3}", follow_path_url = "{4}", follower_user_id = "{5}")'.format(                              # modified by BurnedRobot at 2013-08-03
            self.user_id,
            self.screen_name,
            self.gender,
            self.follow_path,
            self.follow_path_url,
            self.follower_user_id)

class SeedUser():
    def __init__(self, searchpageid = '', nickname = '', title = '', href = '', crawlertime = '', querystring = '', pageindex = '', resulttotal = '', timebatch = ''):
        self.nickname = nickname
        self.title = title
        self.href = href
        self.searchpageid = searchpageid
    def superSearchPage(self, sp):
        self.crawlertime = sp.crawlertime
        self.querystring = sp.querystring
        self.pageindex = sp.pageindex
        self.resulttotal = sp.resulttotal
        self.timebatch = sp.timebatch
    def getdict(self):
        seeddict = dict()
        seeddict['nickName'] = self.nickname
        seeddict['href'] = self.href
        seeddict['title'] = self.title
        seeddict['crawlerTime'] = self.crawlertime
        seeddict['querystring'] = self.querystring
        seeddict['pageIndex'] = self.pageindex
        seeddict['resultTotal'] = self.resulttotal
        seeddict['timeBatch'] = self.timebatch
        seeddict['searchPageId'] = self.searchpageid
        return seeddict

# add by doufunao 2014-07-06
# Page Struct
class Page:
    def __init__(self, crawlertime = '', pageurl = '',  htmlstr = ''):
        self.crawlertime = crawlertime
        self.htmlstr = htmlstr
        self.pageurl = pageurl

    def getdict(self):
        pagedic = dict()
        pagedic['crawlerTime'] = self.crawlertime
        pagedic['htmlStr'] = self.htmlstr
        pagedic['pageUrl'] = self.pageurl
        return pagedic

    def setdict(self, pagedic):
        self.crawlertime = pagedic['crawlerTime']
        self.htmlstr = pagedic['htmlStr']
        self.pageurl = pagedic['pageUrl']

class TimelinePage(Page):
    def __init__(self, crawlertime = '', pageurl = '', htmlstr = '', pageid = '', userid = '', page = '', pagebar = '', prepage = '', ):
        super(TimelinePage, self).__init__(crawlertime, pageurl, htmlstr)
        self.pageid = pageid
        self.userid = userid
        self.page = page
        self.pagebar = pagebar
        self.prepage = prepage

    def getdict(self):
        pagedic = super(TimelinePage, self).getdict()
        pagedic['page'] = self.page
        pagedic['pageId'] = self.pageid
        pagedic['userId'] = self.userid
        pagedic['pageBar'] = self.pagebar
        pagedic['prePage'] = self.prepage
        return pagedic

    def setdict(self, pagedic):
        super(TimelinePage, self).setdict(pagedic)
        self.page = pagedic['page']
        self.pageid = pagedic['pageId']
        self.userid = pagedic['userId']
        self.pagebar = pagedic['pageBar']
        self.prepage = paradic['prePage']

class UserHomePage(Page):
    def __init__(self, crawlertime = '', pageurl = '', htmlstr = '', nickname = '', pageid = '', userid = ''):
        super(UserHomePage, self).__init__(crawlertime, pageurl, htmlstr)
        self.nickname = nickname
        self.pageid = pageid
        self.userid = userid

    def getdict(self):
        pagedic = super(UserHomePage, self).getdict()
        pagedic['nickName'] = self.nickname
        pagedic['pageId'] = self.pageid
        pagedic['userId'] = self.userid
        return pagedic

    def setdict(self, pagedic):
        super(UserHomePage, self).setdict(pagedic)
        self.nickname = pagedic['nickName']
        self.pageid = pagedic['pageId']
        self.userid = pagedic['userId']
        
class SearchPage(Page):
    def __init__(self, crawlertime = '', pageurl = '', htmlstr = '', querystring = '', pageindex = '', pagetotal = '', resulttotal = '', timebatch = ''):
        super(SearchPage, self).__init__(crawlertime, pageurl, htmlstr)
        self.querystring = querystring
        self.pageindex = pageindex
        self.pagetotal = pagetotal
        self.resulttotal = resulttotal
        self.timebatch = timebatch

    def __repr__(self):
        return '''
        SearchPage(crawlerTime = {0}, queryString = {1}, pageIndex = {2}, pageTotal = {3}, resultTotal = {4}, timeBatch = {5})
        '''.format(self.crawlertime,
            self.querystring,
            self.pageindex,
            self.pagetotal,
            self.resulttotal,
            self.timebatch)

    def getdict(self):
        pagedic = super(SearchPage, self).getdict()
        pagedic['queryString'] = self.querystring
        pagedic['pageIndex'] = self.pageindex
        pagedic['pageTotal'] = self.pagetotal
        pagedic['resultTotal'] = self.resulttotal
        pagedic['timeBatch'] = self.timebatch
        return pagedic

    def setdict(self, pagedic):
        super(SearchPage, self).setdict(pagedic)
        self.querystring = pagedic['queryString']
        self.pageindex = pagedic['pageIndex']
        self.pagetotal = pagedic['pageTotal']
        self.resulttotal = pagedic['resultTotal']
        self.timebatch = pagedic['timeBatch']        