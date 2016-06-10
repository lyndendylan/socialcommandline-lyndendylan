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
import twitter
import requests 

from TwitterController import TwitterController
from appengine_oauth import oauth
from gaesessions import get_current_session
from gaesessions import delete_expired_sessions
from google.appengine.ext import ndb
from google.appengine.api import mail
from google.appengine.api import users
from google.appengine.api import urlfetch
from urllib import unquote as urlunquote
from xml.dom import minidom

access_token = "739842667916492800-FJg9hohBppMJ8w816cmJVCE6tv58825"
consumer_key = "MIEorUIGXR3Z4W4aUsv83hled"
consumer_secret = "GyEJT7eTiYTIWmyc2sNGnFXNv790DAhNe9CrxNYwoUm5yMMfN0"
callback_url = "https://socialcommandline.appspot.com/twitter_callback"

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


class TwitterSignin(MainHandler):
    def get(self):
        client = oauth.TwitterClient(consumer_key, consumer_secret, callback_url)
        self.redirect(client.get_authorization_url())

class TwitterCallback(MainHandler):
    def get(self):
        #My App Twitter Client object
        client = oauth.TwitterClient(consumer_key, consumer_secret, callback_url)
        
        #retrieve the auth_token from the client who has logged in
        #retrieve the verifier
        auth_token = self.request.get("oauth_token")
        auth_verifier = self.request.get("oauth_verifier")

        #retrieve twitter user info on our logged in user
        user_info = client.get_user_info(auth_token, auth_verifier=auth_verifier)

        response = client.make_request(
            "https://api.twitter.com/1.1/search/tweets.json",
            token=access_token,
            secret=user_info["secret"],
            method=urlfetch.GET,
            additional_params={"oauth_verifier":auth_verifier}
        )

        content = response.content

        self.render("twitter.html",  
                    client = json.dumps(vars(client)),
                    content = json.dumps(content)
                    )

def check_user_exists(user):
    pass

def show_info(user):
	logging.info("nickname: %s, auth_domain: %s, email: %s, federated_identity: %s, federated_provided: %s, user_id: %s " % (user.nickname(), user.auth_domain(), user.email(), user.federated_identity(), user.federated_provider(), user.user_id()))

app = webapp2.WSGIApplication([

    ('/', HomePage),
    ('/whatisscl', WhatIs),
    ('/profile', Profile),
    ('/showdata', ShowData),
    ('/twitter_signin', TwitterSignin),
    ('/twitter_callback', TwitterCallback)

], debug=True)
