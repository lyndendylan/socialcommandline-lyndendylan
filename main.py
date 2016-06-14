#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))
sys.path.append(os.path.join(os.path.dirname(__file__), "Controllers"))


import webapp2
import jinja2
import json
import random
import pickle
import string
import re
import logging
import httplib2
import functools
import requests 
import tweepy

from gaesessions 						import get_current_session
from gaesessions 						import delete_expired_sessions
from google.appengine.ext.webapp.util 	import run_wsgi_app
from google.appengine.ext 				import ndb
from google.appengine.api 				import mail
from google.appengine.api 				import users
from google.appengine.api 				import urlfetch
from urllib 							import unquote as urlunquote
from xml.dom 							import minidom

access_token = "739842667916492800-FJg9hohBppMJ8w816cmJVCE6tv58825"
access_token_secret = "wd1EYa0tKzRhYY3gvHFnpZzBja5Ya4NWV56sFsSackgD7"
consumer_key = "MIEorUIGXR3Z4W4aUsv83hled"
consumer_secret = "GyEJT7eTiYTIWmyc2sNGnFXNv790DAhNe9CrxNYwoUm5yMMfN0"
live_callback_url = "https://socialcommandline.appspot.com/live_twitter_callback"
local_callback_url = "localhost:8080/local_twitter_callback"

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class MainHandler(webapp2.RequestHandler):
    def write(self, *args, **kwargs):
        self.response.out.write(*args, **kwargs)
        
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kwargs):
        self.write(self.render_str(template, **kwargs))

class HomePage(MainHandler):
    def get(self):
        self.render("homepage.html")

class WhatIs(MainHandler):
    def get(self):
        self.render("whatis.html")

class Profile(MainHandler):
    def get(self):
        pass

class ShowData(MainHandler):
    def get(self):
        users = User.get_all()
        self.render("data.html", users=users)

class LoadDylansTimeline(MainHandler):
    def get(self):

    	"""
	    	create the ouath object for my application thats registered on apps.twitter.com
	    	set the access token so twitter knows its my app accessing their apis
	    	then create the api object
	    	the app is registered on my twitter account which is under screen name @code_monkey_dyl
	    	calling api.home_timeline() retrieves all the public tweets from my account @code_monkey_dyl

    	"""
    	auth = tweepy.OAuthHandler(consumer_key, consumer_secret, local_callback_url)
    	auth.set_access_token(access_token, access_token_secret)
    	api = tweepy.API(auth)
    	public_tweets = api.home_timeline()
    	self.render("twitter.html", tweets=public_tweets)

class LoadTwitterTimeline(MainHandler):
	def get(self):
		auth = tweepy.OAuthHandler(consumer_key, consumer_secret, live_callback_url)
		auth.set_access_token(access_token, access_token_secret)
    	try:
    		redirect_url = auth.get_authorization_url()
    		logging.error(redirect_url)
    	except tweepy.TweepError as te:
    		logging.error(str(te))

 
class LoadFacebookTimeline(MainHandler):
	def get(self):
		pass

class LiveTwitterCallback(MainHandler):
    def get(self):
    	pass

class LocalTwitterCallback(MainHandler):
    def get(self):
    	pass

def show_info(user):
	logging.info("aanickname: %s, auth_domain: %s, email: %s, federated_identity: %s, federated_provided: %s, user_id: %s " % (user.nickname(), user.auth_domain(), user.email(), user.federated_identity(), user.federated_provider(), user.user_id()))

app = webapp2.WSGIApplication([

    ('/', HomePage),
    ('/whatisscl', WhatIs),
    ('/profile', Profile),
    ('/showdata', ShowData),
    ('/load_dylans_timeline', LoadDylansTimeline),
    ('/load_twitter_timeline', LoadTwitterTimeline),
    ('/load_facebook_timeline', LoadFacebookTimeline),
    (local_callback_url, LocalTwitterCallback),
    (live_callback_url, LiveTwitterCallback)


], debug=True)

run_wsgi_app(app)
