# first is the query
# run a search
# get a list of urls
# fetch the stories from those urls

import requests
from bs4 import BeautifulSoup as Bs
import re

def parse_query(query):
	keywords = query.split()
	parsed_query = "+".join(keywords)
	return parsed_query

def run_search(parsed_query):
	search_url = "https://google.com/search?q="
	results_page = requests.get(search_url+parsed_query)
	return results_page

def get_urls(results_page):
	soup = Bs(results_page.text, "html5lib")
	hits = soup.find_all("div", attrs={"class":"g"})
	straight_link = r"([\w\s',\.-]+) - ([\w\s'/,\.-]+)(https://[\w\./-]+)CachedSimilar([\w\s',\./-]+)"
	
	url_list = []
	for hit in hits:
		parse = re.search(straight_link, hit.text)
		if parse:
			url = parse.group(3)
			url_list.append(url)
	
	return url_list

def fetch_story(url):
	page = requests.get(url)
	header = []
	pages = []
	
	soup = Bs(page.text, "html5lib")
	head = soup.find("div", attrs={"class":"b-story-header"}).text
	body = soup.find("div", attrs={"class":"b-story-body-x"}).text
	
	parse_header = re.search(r"([\w\s',/-]+)\n\s*by([\w\s',/-]+)", head)
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
	
	return (header, pages)

# to do:
	# add rating retrieval