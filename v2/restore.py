import json
import lois, service

f = open("assets/export.txt")
stories = []

for story in f.readlines():
	stories.append(json.loads(story))

new_stories = []
for story in stories:
	n = {}
	n["title"] = story["title"]
	n["author"] = story["author"]
	n["pages"] = [{"page": text} for text in story["pages"]]
	n["uid"] = story["_id"]
	
	new_stories.append(n)

ns = [lois.Story().make(new) for new in new_stories]
