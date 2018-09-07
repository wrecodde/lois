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

