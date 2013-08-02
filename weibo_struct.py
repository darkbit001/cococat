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


