import get_search_results
import get_user_pages
import get_user_relationship
import get_user_timeline
import proc_search_results
import proc_user_pages
import proc_user_relation_pages
import proc_user_timeline_pages

def main():
	get_search_results.main()
	proc_search_results.main()
	get_user_pages.main()
	proc_user_pages.main()
	get_user_relationship.main()
	proc_user_relation_pages.main()
	get_user_timeline.main()
	proc_user_timeline_pages.main()

main()
