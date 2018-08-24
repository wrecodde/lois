
import requests
from bs4 import BeautifulSoup as Bs
import re

try:
	import html5lib
	parser = 'html5lib'
except:
	parser = 'html.parser'


def connected():
	try:
		requests.get("https://google.com")
		return True
	except:
		return False

def fetch_search(parsed_query):
	search_url = "https://google.com/search?q="
	if connected():
		results_page = requests.get(search_url+parsed_query)
		return results_page
	else:
		return None

def fetch_story(url):
	if connected():
		page = requests.get(url)
		return parse_page(page.text)
	else:
		return None

def parse_query(query):
	keywords = query.lower().split()
	parsed_query = "+".join(keywords)
	return parsed_query

def parse_for_urls(results_page, extra=False):
	# parses a google results page to extract possible hits.
	# works completely offline
	
	soup = Bs(results_page, parser)
	hits = soup.find_all("div", attrs={"class":"g"})
	straight_link = r"([\w\s',\.-]+) - ([\w\s'/,\.-]+)(https://[\w\./-]+)CachedSimilar([\w\s',\./-]+)"
	
	url_list = []
	extras = []
	
	for hit in hits:
		parse = re.search(straight_link, hit.text)
		if parse:
			title = parse.group(1)
			url = parse.group(3)
			brief = parse.group(4)
			hit_object = {"title":title, "tease":brief, "url":url}
			extras.append(hit_object)
			url_list.append(url)
	if extra:
		return extras
	
	return url_list

def parse_for_stories(html_page):
	# parses an html page (of a story).
	# should work offline. excpet if there are multiple pages
	# then it would attepmt to fetch those.
	
	header = []
	pages = []
	
	soup = Bs(html_page, parser)
	head = soup.find("div", attrs={"class":"b-story-header"}).text
	body = soup.find("div", attrs={"class":"b-story-body-x"}).text
	
	parse_header = re.search(r"([\w\s'.,/-]+)\n\s*by([\w\s',/-]+)", head)
	if parse_header:
		header.append(parse_header.group(1))
		header.append(parse_header.group(2))
	
	header.append(head)
	pages.append(body)
	
	while True:
		next_page = soup.find("a", attrs={"class":"b-pager-next"})
		if next_page:
			new_page = requests.get(next_page["href"])
			soup = Bs(new_page.text, "html5lib")
			body = soup.find("div", attrs={"class":"b-story-body-x"}).text
			pages.append(body)

		else:
			break
	
	story_object = {"title":header[0], "author":header[1], "pages":pages}
	return story_object

def get_stories(query):
	parsed_query = parse_query(query)
	if connected():
		results = fetch_search(parsed_query)
		urls = parse_for_urls(results)
		
		# terribly synchronous
		stories = []
		
		for url in urls:
			story = fetch_story(url)
			stories.append(story)
		
		return stories
	
	else:
		# we assume no internet connection
		return None

def get_hits(query):
	parsed_query = parse_query(query)
	results_page = fetch_search(parsed_query)
	hits = parse_for_urls(results_page.text, extra=True)
	
	return hits

# to do:
	# add rating retrieval