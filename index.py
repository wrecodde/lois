import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpserver


# pages:
	# index: show recent stories; make new search
	# search: search results and confirmation
	# stories: all stories
	# story: a story; trash function
	# auth: confirm access to lois

class BaseHandler(tornado.web.RequestHandler):
	pass

class IndexHandler(BaseHandler):
	def get(self):
		pass

class AuthHandler(BaseHandler):
	def get(self):
		pass

class SearchHandler(BaseHandler):
	def get(self):
		pass
	
	def post(self):
		pass

class Stories(BaseHandler):
	def get(self):
		pass

class StoryHandler(BaseHandler):
	def get(self):
		pass
	
	def delete(self):
		pass

handlers = [
	(r"/", IndexHandler),
	(r"/auth", AuthHandler),
	(r"/search", SearchHandler),
	(r"/stories", Stories),
	(r"/story", StoryHandler),
]

settings = dict(
	debug = True,
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
