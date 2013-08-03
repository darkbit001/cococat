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
                        

class User_Profile(User):
    def __init__(self, user_id, screen_name, gender, follower_num, following_num, weibo_num, member_type, member_level):
        super(User_Detail,self).__init__(user_id, screen_name, gender)
        self.follower_num = follower_num
        self.following_num = following_num
        self.weibo_num = weibo_num
        self.member_type = member_type
        self.member_level = member_level
    def __repr__(self):
        return 'User_Profile(user_id = {0}, screen_name = "{1}", gender = "{2}", follower_num = "{3}", following_num = "{4}", weibo_num = "{5}", member_type = "{6}", member_level = "{7}")'.format(
            self.user_id,
            self.screen_name,
            self.gender,
            self.follower_num,
            self.following_num,
            self.weibo_num,
            self.member_type,
            self.member_level)

class User_Fllow(User):
    def __init__(self, user_id, screen_name, gender, follow_path, follow_path_url):
        super(User_Fllow, self).__init__(user_id, screen_name, gender)
        self.follow_path = follow_path
        self.follow_path_url = follow_path_url
    def __repr__(self):
        return 'User_Fllow(user_id = {0}, screen_name = "{1}", gender = "{2}", follow_path = "{3}", follow_path_url = "{4}"'.format(
            self.user_id,
            self.screen_name,
            self.gender,
            self.follow_path,
            self.follow_path_url)       