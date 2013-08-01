#
# weibo_reply.py
#
# ling0322 2013-08-01
#

class Reply:
	def __init__(self, user_id, reply_time, text):
		self.user_id = user_id
		self.reply_time = reply_time
		self.text = text

def get_weibo_reply(http_request, weibo_url):
	"""
	get_weibo_reply returns a weibo's replies from its url

	@param http_request The http_request is an instance of WeiboHttpRequest
	@param weibo_url The url of the weibo

	returns a list of Reply
	"""

	pass