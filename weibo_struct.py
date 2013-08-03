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
                        

class UserProfile(User):
    def __init__(self, user_id, screen_name, gender, follower_num, following_num, weibo_num, member_type, member_level):
        super(User_Detail,self).__init__(user_id, screen_name, gender)
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
        return 'Follower(user_id = {0}, screen_name = "{1}", gender = "{2}", follow_path = "{3}", follow_path_url = "{4}", following_user_id = "{5}")'.format(                              # modified by RobotFlying at 2013-08-03
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
        return 'Following(user_id = {0}, screen_name = "{1}", gender = "{2}", follow_path = "{3}", follow_path_url = "{4}", follower_user_id = "{5}")'.format(                              # modified by RobotFlying at 2013-08-03
            self.user_id,
            self.screen_name,
            self.gender,
            self.follow_path,
            self.follow_path_url,
            self.follower_user_id)


