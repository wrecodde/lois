import tornado.web
import tornado.ioloop
import tornado.options
import tornado.gen
import tornado.httpserver
import tornado.httpclient

import os
import secrets

import service

from tornado.options import define
define("port", default=33041, type=int)


class BaseHandler(tornado.web.RequestHandler):
	def get_current_user(self):
		try:
		    session_cookie = self.get_secure_cookie("user_session")
		    # decrypt and extract component user info
		    # feed back to auth handler
		else:
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

class AuthHandler(BaseHandler):
	def get(self):
		next_page = self.get_argument("next", "/")
		user_session = self.get_current_user()
		if user_session is None:
			# no user is logged in
			self.render("auth.html", next=next_page)
		else:
			# re-authenticate user
			self.redirect(next_page)
	
	def post(self):
		# get and confirm user creds
		
		self.set_secure_cookie("user_session", b"encryptediInfo")
		# communication is via ajax

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

class LoisHandler(BaseHandler):
	def get(self, *args):
		self.render("lois.html")
	
	def post(self):
		action = self.get_argument("action")
		if action == "0":
			import random
			self.lois.insert({"number": random.choice(range(33))})
		elif action == "1":
			print(self.lois.fetch_all())

class Leila(LoisHandler):
	def get(self, *args):
		self.render("leila.html")
	
	def post(self):
		action = self.get_argument("action")
		
		if action == "0":
			import random
			self.lois.insert({"number": random.choice(range(33))})
		elif action == "1":
			print(self.lois.fetch(0))


handlers = [
	(r"/", IndexHandler),
	(r"/auth/signup", AuthSignUpHandler),
	(r"/auth/signin", AuthSignInHandler),
	(r"/search", SearchHandler),
	(r"/stories", Stories),
	(r"/stories/([0-9]+)", StoryHandler),
	(r"/save", Save),
	(r"/lois", LoisHandler),
	(r"/leila", Leila),
]

settings = dict(
	debug = True,
	cookie_secret = secrets.token_hex(5),
	template_path = os.path.join(os.path.dirname(__file__), "templates"),
	static_path = os.path.join(os.path.dirname(__file__), "static"),
	login_url = "/auth",
	autoescape = None,
)

app = tornado.web.Application(handlers, **settings)
def start():
	tornado.options.parse_command_line()
	port = tornado.options.options.port
	server = tornado.httpserver.HTTPServer(app)
	server.listen(port)
	
	tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
	start()
