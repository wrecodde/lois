import re
import hashlib

import requests
import bs4
bsoup = bs4.BeautifulSoup

class Hit:
	# attempt to parse search results
	title = ""
	url = ""
	brief = ""
	valid = False
	
	def __init__(self, raw_hit=None):
		# raw hit must be of type Tag element
		if not isinstance(raw_hit, bs4.element.Tag):
			return
		self.parse_hit(raw_hit)
	
	def parse_hit(self, raw_hit):
		hit_rgx = r"(.*)(https://.*)(CachedSimilar|Cached)(.*)"
		title_rgx = r"(.*) - (.*)*"
		
		raw_text = raw_hit.text.replace("\n", "")
		match = re.search(hit_rgx, raw_text)
		
		if match:
			raw_title = match.group(1)
			match_title = re.search(title_rgx, raw_title)
			
			self.title = match_title.group(1)
			self.url = match.group(2)
			self.brief = match.group(4)
			self.valid = True
		else:
			self.valid = False
			return
	
	def transform(self):
		hit = {"title": self.title, "url": self.url, "brief": self.brief}
		return hit

class Search:
	hits = [] # a list of Hit objects
	
	def __init__(self, query=None, web_page=None):
		if query:
			query = "+".join(query.lower().split())
			g_search = "https://google.com/search?q="
			results_page = requests.get(g_search + query)
			self.parse_page(results_page.text)
		else:
			if web_page:
				self.parse_page(web_page)
			return
	
	def parse_page(self, web_page):
		# parse web page for hits
		page_soup = bsoup(web_page, "html5lib")
		raw_hits = page_soup.find_all("div", attrs={"class":"g"})
		
		for raw_hit in raw_hits:
			hit = Hit(raw_hit)
			if hit.valid:
				self.hits.append(hit)

class Story:
	story_id = "" # hash of story url
	story_url = "" # unique identifier
	title = ""
	author = ""
	author_url = ""
	rating = ""
	pages = []
	
	page = {"page_content":"", "page_url":""}
	
	def __init__(self, url=None, web_page=None):
		if url:
			# this constructor is not responsible for
			# non-generated errors such as internet
			# connectivity
			story_page = requests.get(url)
			self.parse_page(story_page.text)
		else:
			if web_page:
				self.parse_page(web_page)
	
	def parse_page(self, web_page):
		# given a web page, attempt to parse it for a story.
		# should be wrapped in an executor in order to
		# maintain asynchronicity should the story be
		# multipaged
		page_soup = bsoup(web_page, "html5lib")
		
		# url in page is on the twitter button
		twitter_soup = page_soup.find("a", attrs={"class":"twitter-share-button"})
		self.title = twitter_soup["data-text"]
		self.story_url = twitter_soup["data-url"]
		self.story_id = hashlib.md5(self.story_url.encode()).hexdigest()
		
		# author extract
		author_soup = page_soup.find("span", attrs={"class":"b-story-user-y"})
		self.author = author_soup.text
		self.author_url = author_soup.find("a")["href"]
		
		# pages
		# first page
		first_page = page_soup.find("div", attrs={"class":"b-story-body-x"})
		fp_content = first_page.text
		fp_url = self.story_url
		self.pages.append({"page_content":fp_content, "page_url":fp_url})
		
		# multipaged?
		while True:
			next_page = page_soup.find("a", attrs={"class":"b-pager-next"})
			if next_page:
				page_url = next_page["href"]
				new_page = requests.get(page_url).text
				page_soup = bsoup(new_page, "html5lib")
				page_content = page_soup.find("div", attrs={"class":"b-story-body-x"})
				self.pages.append({"page_content": page_content, "page_url": page_url})
				continue
			else:
				break
	
	def transform(self):
		# convert self.atrribs to valid json (dict object)
		story = self.__dict__
		story["pages"] = self.pages
		return story