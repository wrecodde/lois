# database functions
import os
import tinydb

import service

# database config: tinydb
db_dir = os.path.join(os.path.dirname(__file__), ".database")

if not os.path.isdir(db_dir):
	os.mkdir(db_dir)

db_query = tinydb.Query()

stories = tinydb.TinyDB(db_dir + "/stories.db")
trash = tinydb.TinyDB(db_dir + "/trash.db")

def get_story(story_id):
	story = stories.get(db_query.story_id == story_id)
	return story

def save_story(story: json):
	# story: story object converted to json
	
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
