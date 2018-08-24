# app dependent services
import os
import tinydb

import lois
import search

# database config: tinydb
db_path = os.path.join(os.path.dirname(__file__), ".service")

if not os.path.isdir(db_path):
	os.mkdir(db_path)

db_query = tinydb.Query()

stories = tinydb.TinyDB(db_path + "/stories.db")
trash = tinydb.TinyDB(db_path + "/trash.db")

def get_story(story_id):
	story = stories.get(db_query.story_id == story_id)
	return story

def save_story(web_page):
	# pass web page on to lois.Story for parsing
	# transform Story and write to database
	# saving a story modifies the index too
	
	story = lois.Story(web_page=web_page)
	
	# check for duplicates
	if stories.search(db_query.story_id == story.story_id):
		return {"error":"duplicate story", "msg":"duplicate story exists already"}
	
	stories.insert(story.transform())
	index_story(story)

def trash_story(story_id, permanent=False):
	# move story across databases (to trash)
	# modify index
	
	story = get_story(story_id)
	stories.remove(query.story_id == story_id)
	
	if permanent:
		writer = story_index.writer()
		writer.delete_by_term("story_id", story_id)
		writer.commit()
		return {"error":None, "msg":"permanently trashed story"}
	
	trash_id = trash.insert(story)
	return {"error":None, "msg":"moved story to trash"}

def modify_story(story_id, mod={}):
	# make modifications to a story
	actions = ["fave", "read", "restore"]
	
	if not mod:
		return
	
	for action, value in mod.items():
		pass
	
	if action not in actions:
		return # error
	
	writer = story_index.writer()
	
	if action == "fave":
		stories.update({"fave": value}, db_query.story_id == story_id)
		writer.update_document(story_id=story_id, fave=value)
		return
	elif action == "read":
		stories.update({"read": value}, db_query.story_id == story_id)
		writer.update_document(story_id=story_id, read=value)
		return
	
	if action == "restore":
		if action == "true":
			story = trash.get(query.story_id == story_id)
			trash.remove(query.story_id == story_id)
			stories.insert(story)
	
	# more actions...
	writer.commit()
