import tornado.web
import tornado.ioloop
import tornado.options
import tornado.gen


class BaseHandler(tornado.web.RequestHandler):
	def get_current_user(self):
		try:
		    session_cookie = self.get_secure_cookie("user_session")
		    # decrypt and extract component user info
		    # feed back to auth handler
		except:
			
			# should an error occur
			return None
	
	def password_hash(self, p):
		try:
			c, d = p[0], p[1:]
			k = int(d) * ord(c)
			return k
		except:
			return None

class IndexHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self):
		self.render("index.html")
	
	@tornado.web.authenticated
	def post(self):
		self.write("data sent")


# authentication
class Auth_SignIn(BaseHandler):
	def get(self):
		next_page = self.get_argument("next", "/")
		user_session = self.get_current_user()
		if user_session is None:
			# no user is logged in
			self.render("auth/signin.html", next=next_page)
		else:
			# re-authenticate user
			self.clear_secure_cookie("user_session")
			self.redirect("/auth/signin", next_page=next_page)
	
	def post(self):
		# get and confirm user creds
		user = self.get_query_argument("user")
		next = self.get_argument("next_page")
		
		print(user, next)
		
		self.set_secure_cookie("user_session", b"encryptediInfo")
		# communication is via ajax

class Auth_SignUp(BaseHandler):
	pass


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

