from weibocrawler import dboperator
import json
import re
dbo = dboperator.Dboperator(collname = 'UserRelationPages')
cursor = dbo.coll.find({'userId': '2920092522'}, {'htmlStr': 1}).limit(1)
pattern = re.compile(r'<script>parent.FM.view\((.+)\)</script>')
print(pattern.findall(cursor[0]['htmlStr'])[0])