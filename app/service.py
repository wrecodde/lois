import re
import hashlib
import requests

import bs4
bsoup = bs4.BeautifulSoup

import database

class SearchHit:
	"""SearchHit defines the attributes and methods
	of a search result, whether local or over the internet."""
	# title
	# url
	# brief
	# uid
	# scope
	
	pass

class Story:
	"""Story describes attributes and methods needed
	to work with a story, acting as an API between the
	database and app."""
	
	# title
	# url
	# uid
	# author
	# pages
	
	pass


def get_story_from_site():
	"""Contain code to parse web page from a given url.
	Functions (parsers) are specific to each site."""

	pass

def validate_user(asking_user):
	saved_user = database.get_user(asking_user.get("email"))
	if not saved_user:
		return False
	
	if saved_user.get("password") == hash(asking_user.get("password")):
		return True
	
	return False