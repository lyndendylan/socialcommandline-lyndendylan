# from google.appengine.ext import vendor
# vendor.add('lib')
import sys
import os 
sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))

from gaesessions import SessionMiddleware
def webapp_add_wsgi_middleware(app):
	app = SessionMiddleware(app, cookie_key=str(os.urandom(64)))
	return app