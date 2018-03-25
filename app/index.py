import tornado.web
import tornado.ioloop
import tornado.options
import tornado.gen
import tornado.httpserver
import tornado.httpclient

import os
import json
import secrets
from operator import attrgetter
from operator import itemgetter

# story header bar
# add "to the top" button
# auth page

import lois
import porter_db as porter

from tornado.options import define
define("port", default=3304, type=int)

class BaseHandler(tornado.web.RequestHandler):
	stories = porter.DataBase("stories")
	trash = porter.DataBase("trash")
	
	def load_db(self):
		self.stories = porter.DataBase("stories")
		self.trash = porter.DataBase("trash")
	
	def get_current_user(self):
		return self.get_secure_cookie("auth")
	
	def hash(self, p):
		try:
			c, d = p[0], p[1:]
			k = int(d) * ord(c)
			return k
		except:
			return None

class IndexHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self):
		stories = self.stories.fetch_all()
		self.render("index.html", recent=stories[-3:])

class AuthHandler(BaseHandler):
	def get(self):
		next_page = self.get_argument("next", "/")
		self.render("auth.html", message="authentication", next=next_page)
	
	def post(self):
		password = self.get_argument("password", None)
		next_page = self.get_argument("next", "/")
		session = self.get_argument("session", "open")
		
		key = self.hash(password)
		lock = 799920
		
		if session == "close":
			self.clear_cookie("auth")
			return
		
		if key == lock:
			self.set_secure_cookie("auth", "locker", expires_days=1)
			self.redirect(next_page)
		else:
			self.render("auth.html", message="failed")

class SearchHandler(BaseHandler):
	def get(self):
		# used for testing in place of .xget()
		raw = open('notes/searchpage2.txt').read()
		hits = lois.parse_for_urls(raw, extra=True)
		self.render("results.html", error=None, hits=hits)
	
	@tornado.web.authenticated
	def xget(self):
		# should replace .get()
		query = self.get_argument("query")
		
		try:
			hits = lois.get_hits(query)
			r = {"error":None, "hits":hits}
			self.write(json.dumps(r))
		except:
			r = {"error":"an error occured", "hits":[]}
			self.write(json.dumps(r))
	
	@tornado.web.authenticated
	def post(self):
		query = self.get_argument("query")
		scope = self.get_argument("scope")
		
		if scope == "external":
			try:
				hits = lois.get_hits(query)
				self.render("results.html", error=None, hits=hits)
			except:
				self.render("results.html", error="no internet connection", hits=[])
		elif scope == "internal":
			pass # coming up later

class Stories(BaseHandler):
	@tornado.web.authenticated
	def get(self):
		stories = self.stories.fetch_all()
		stories = sorted(stories, key=itemgetter('_id'), reverse=True)
		self.render("stories.html", stories=stories)

class StoryHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self, story_id):
		story = self.stories.fetch(story_id)
		if not story:
			# raise tornado.web.HTTPError(404)
			pass
		self.render("story.html", story=story)
	
	@tornado.web.authenticated
	def delete(self, story_id):
		story = self.stories.fetch(story_id)
		self.trash.insert(story)
		self.stories.delete(story_id)
		self.stories.save()
		self.trash.save()
		self.redirect("/stories")

class Save(BaseHandler):
	@tornado.web.authenticated
	@tornado.gen.coroutine
	def get(self):
		story_url = self.get_argument("story_url")
		
		client = tornado.httpclient.AsyncHTTPClient()
		response = yield client.fetch(story_url)
		story = lois.parse_for_stories(response.body)
		
		self.stories.insert(story)
		self.stories.save()

class LoisHandler(BaseHandler):
	def get(self):
		self.render("lois.html")
	
	def xget(self):
		self.render("lois.html")


handlers = [
	(r"/", IndexHandler),
	(r"/auth", AuthHandler),
	(r"/search", SearchHandler),
	(r"/stories", Stories),
	(r"/stories/([0-9]+)", StoryHandler),
	(r"/save", Save),
	(r"/lois", LoisHandler),
]

settings = dict(
	debug = True,
	cookie_secret = secrets.token_hex(5),
	template_path = os.path.join(os.path.dirname(__file__), "pages"),
	static_path = os.path.join(os.path.dirname(__file__), "assets"),
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
