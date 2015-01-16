import create_nicks
import get_search_results
import get_user_pages
import get_user_relationship
import get_user_timeline
import proc_search_results
import proc_user_pages
import proc_user_relation_pages
import proc_user_timeline_pages
from convert_cookies import convert_cookies
from weibocrawler import WeiboHttpRequest
from weibocrawler import WeiboLogin

def get_request(check_cookie_file = True):
	username = 'e1441430@drdrb.com'
	password = 'e1441430'
	if check_cookie_file == True:
		convert_cookies()
	login = WeiboLogin(username, password)
	http_request = WeiboHttpRequest(login)
	return http_request

def main():
	# get_search_results.main()
	# proc_search_results.main()
	request = get_request()
	create_nicks.main()
	get_user_pages.main(request)
	proc_user_pages.main()
	get_user_timeline.main(request)
	proc_user_timeline_pages.main()
	get_user_relationship.main(request)
	proc_user_relation_pages.main()
main()
