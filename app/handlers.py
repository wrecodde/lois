import tornado.web
import tornado.ioloop
import tornado.options
import tornado.gen

import json

import service

class BaseHandler(tornado.web.RequestHandler):
	def get_current_user(self):
		try:
			session_cookie = self.get_secure_cookie("user_session")
			if session_cookie:
				user_info = json.loads(session_cookie)
				return user_info.get("logged_in_user")
			else:
				return None
		except:
			# should an error occur
			return None
	

class IndexHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self):
		self.render("index.html")


# authentication
class Auth_SignIn(BaseHandler):
	def get(self):
		redirect_to = self.get_query_argument("next", "/")
		user_session = self.get_current_user()
		
		if user_session is None:
			# no user is logged in
			self.render("auth/signin.html", next=redirect_to)
		else:
			# re-authenticate user
			self.clear_cookie("user_session")
			self.redirect("/auth/signin", next=redirect_to)
	
	def post(self):
		# get and confirm user creds
		user = json.loads(self.get_body_argument("user"))
		grant_access = service.validate_user(user)

		if grant_access is True:
			self.set_secure_cookie("user_session", json.dumps({
				"logged_in_user": user.get("email")
			}), expires_days=1)

			self.write(json.dumps({
				"status": "success",
				"status_text": "user logged in successfully"
			}))
		else:
			self.write(json.dumps({
				"status": "failed",
				"status_text": "email or password is incorrect."
			}))
		

class Auth_SignUp(BaseHandler):
	def get(self):
		redirect_to = self.get_query_argument("next", "/")
		
		self.render("auth/signup.html", next=redirect_to)
	
	def post(self):
		user = json.loads(self.get_body_argument("user"))

		if service.email_inuse(user.get("email")):
			self.write(json.dumps({
				"status": "failed",
				"status_text": "email address is already in use"
			}))
			return
		
		if service.username_inuse(user.get("username")):
			self.write(json.dumps({
				"status": "failed",
				"status_text": "username is already in use"
			}))
			return
		
		service.database.create_user(user["email"], user["username"], user["password"])
		self.write(json.dumps({
			"status": "success",
			"status_text": "user account created successfully"
		}))
		

	
class Auth_SignOut(BaseHandler):
	def get(self):
		user_logged_in = self.get_current_user()
		if not user_logged_in:
			return
		try:
			self.clear_cookie("user_session")
			self.write(json.dumps({
				"status": "success",
				"status_text": "user logged out successfully"
			}))
			return
		except:
			self.write(json.dumps({
				"status": "failed",
				"status_text": "server error. we're all over it already."
			}))
			raise

class SearchHandler(BaseHandler):
	def get(self):
		pass
	
	def post(self):
		query = self.get_argument("q")
		scope = self.get_argument("s", "all")

class Stories(BaseHandler):
	@tornado.web.authenticated
	def get(self):
		self.render("stories.html")
	
	def post(self):
		scope = self.get_argument("scope")
		# process request based on scope

class StoryHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self, story_id):
		story = service.get_story(story_id)
		self.render("story.html", story=story)
	
	@tornado.web.authenticated
	def put(self, story_id):
		mod = self.get_argument("mod")
		feedback = service.modify_story(story_id, mod)
	
	@tornado.web.authenticated
	def delete(self, story_id):
		feedback = service.trash_story(story_id)
		self.write(feedback)

class Save(BaseHandler):
	@tornado.web.authenticated
	@tornado.gen.coroutine
	def get(self):
		target_url = self.get_argument("story_url")
		 
		client = tornado.httpclient.AsyncHTTPClient()
		# fetch the web page at the url and pass it to
		# service.save_story()
		# use executor to make asynchronous

