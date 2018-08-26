
import tornado.httpserver
import tornado.httpclient

import os
import secrets

import service
from handlers import *


from tornado.options import define
define("port", default=33041, type=int)


handlers = [
	(r"/", IndexHandler),
	(r"/auth/signup", Auth_SignUp),
	(r"/auth/signin", Auth_SignIn),
	(r"/auth/signout", Auth_SignOut),
	(r"/search", SearchHandler),
	(r"/stories", Stories),
	(r"/stories/([0-9]+)", StoryHandler),
	(r"/save", Save),
]

settings = dict(
	debug = True,
	cookie_secret = secrets.token_hex(16),
	template_path = os.path.join(os.path.dirname(__file__), "templates"),
	static_path = os.path.join(os.path.dirname(__file__), "static"),
	login_url = "/auth/signin",
	autoescape = None,
)

app = tornado.web.Application(handlers, **settings)
def start():
	tornado.options.parse_command_line()
	port = tornado.options.options.port
	server = tornado.httpserver.HTTPServer(app)
	server.listen(port)
	
	print("application server started")
	print(f"server is listening on port {port}")
	tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
	start()
