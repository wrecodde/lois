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
	
	def __init__(self, story=None, raw_hit=None):
		if not story:
			# raw hit must be of type Tag element
			if not isinstance(raw_hit, bs4.element.Tag):
				return # or raise error
			self.parse_hit(raw_hit)
		
		# or parse story object from internal search results
		self.parse_story(story)
	
	
	def parse_story(self, story):
		self.title = story.title
		self.url = "/stories/" + story.story_id
		self.brief = story.pages[0]["page_content"][:150]
		self.valid = True
		return
	
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

class Story:
	title = ""
	author = ""
	pages = []
	
	url = "" # unique identifier
	uid = "" # hash of story url
	
	def __init__(self, url=None, web_page=None):
		if url:
			web_page = requests.get(url)
			self.parse_page(web_page.text)
		else:
			if web_page:
				self.parse_page(web_page)
	
	def parse_page(self, web_page):
		page_soup = bsoup(web_page, "html5lib")
		
		# url in page is on the twitter button
		twitter_btn = page_soup.find("a", attrs={"class":"twitter-share-button"})
		self.title = twitter_btn["data-text"]
		self.url = twitter_btn["data-url"]
		self.uid = hashlib.md5(self.url.encode()).hexdigest()
		
		# author extract
		author_soup = page_soup.find("span", attrs={"class":"b-story-user-y"})
		self.author = author_soup.text
		
		# first page
		fp = page_soup.find("div", attrs={"class":"b-story-body-x"})
		self.pages.append({"page":fp.text})
		
		# multipaged?
		while True:
			next_page = page_soup.find("a", attrs={"class":"b-pager-next"})
			if next_page:
				page_url = next_page["href"]
				new_page = requests.get(page_url).text
				page_soup = bsoup(new_page, "html5lib")
				page_content = page_soup.find("div", attrs={"class":"b-story-body-x"})
				self.pages.append({"page": page_content})
				continue
			else:
				break
	
	def transform(self):
		# convert attributes to valid json (dict object)
		return self.__dict__
	
	def make(self, m_story):
		# convert transformed story (dict object) to Story object
		p = m_story
		
		self.title = p.get("title")
		self.author = p.get("author")
		self.pages = p.get("pages")
		
		self.url = p.get("url")
		self.uid = str(p.get("uid"))
		
		return self
