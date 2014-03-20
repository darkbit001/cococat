from bs4 import BeautifulSoup
import json
if __name__ == '__main__':
	f = open('weibo_content_sample_json_raw', 'br')
	raw = f.read()
	f.close()
	raw = raw.decode('utf-8')
	#print(raw)
	weibo_content_sample_json = json.loads(raw)
	data = weibo_content_sample_json['html']
	#print(data)
	fp = open('weibo_content_sample_json', 'bw')
	fp.write(data)
	fp.close()
