# database functions
import os
import tinydb

import service

# database config: tinydb
db_dir = os.path.join(os.path.dirname(__file__), ".database")

if not os.path.isdir(db_dir):
	os.mkdir(db_dir)


users = tinydb.TinyDB(db_dir + "/users.db")
stories = tinydb.TinyDB(db_dir + "/stories.db")
trash = tinydb.TinyDB(db_dir + "/trash.db")


def create_user(email, username, password):
	users.insert({
		"uid" : hash(email + username),
		"email": email,
		"username": username,
		"password": hash(password)
	})

	return

def get_user(email):
	user_query = tinydb.Query()
	user = users.search(user_query.email == email)

	if user:
		return user[0]
	else:
		return None

