# search module

import os
import requests

import service

import whoosh
from whoosh.index import open_dir, create_in
from whoosh.qparser import MultifieldParser, OrGroup
from whoosh.fields import Schema, TEXT, ID


class ParseError(BaseException):
	def __init__(self, message):
		return

file_root = os.path.dirname(__file__) # read, cwd
default_path = os.path.join(file_root, ".service/index")

def open_index(path=default_path, schema="", name="stories"):
	# schema: schema to use
	# name: index name to apply
	if not os.path.isdir(path):
		os.mkdir(path)
	
	# check for already created indexes first
	exists = whoosh.index.exists_in(path, indexname=name)
	if exists:
		index = open_dir(path, indexname=name)
		return index
	else:
		index = create_in(path, schema=schema, indexname=name)
		return index

def index_story(story):
	# index the content of a story
	if not isinstance(story, lois.Story):
		raise ParseError(f"failed to parse {story}.")
	
	prepped_pages = "\n----".join([i["page"] for i in story.pages])
	
	try:
		writer = INDEX.writer()
		writer.add_document(
			title = story.title,
			author = story.author,
			story = prepped_pages,
			uid = story.uid)
	finally:
		writer.commit()

def local_search(query):
	# make a search of app's database
	# results max length is 15
	query = Q_PARSER.parse(query)
	
	searcher = INDEX.searcher()
	hits = searcher.search(query, limit=15)
	return hits
	searcher.close()

def internet_lookup(query):
	# make search queries to multiple sites
	
	query = "+".join(query.lower().split())
	

STORY_SCHEMA = Schema(
	title = TEXT,
	author = TEXT,
	story = TEXT,
	uid = ID(stored=True, unique=True),
)

INDEX = open_index(schema=STORY_SCHEMA)
index = INDEX

Q_PARSER = MultifieldParser(
	["title", "author", "story"], 
	INDEX.schema, 
	group=OrGroup
)


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
