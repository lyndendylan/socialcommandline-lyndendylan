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
import webapp2
import jinja2
import os
import json
import random
import pickle
import string
import re
import logging

from google.appengine.ext import db
from google.appengine.api import mail
from google.appengine.api import users
from xml.dom import minidom
from models import User

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
        if not users.get_current_user():
            google_login_url = users.create_login_url("/")
            self.render("homepage.html", gurl = google_login_url)
        else:
            self.redirect("/profile")

class WhatIs(MainHandler):
    def get(self):
        self.render("whatis.html")

class Profile(MainHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            show_info(user)
            check_user_exists(user)
            google_logout_url = users.create_logout_url("/")
            self.render("profile.html", gurl = google_logout_url)
		
class ShowData(MainHandler):
    def get(self):
        users = User.get_all()
        self.render("data.html", users=users)

def check_user_exists(user):
    pass

def show_info(user):
	logging.info("nickname: %s, auth_domain: %s, email: %s, federated_identity: %s, federated_provided: %s, user_id: %s " % (user.nickname(), user.auth_domain(), user.email(), user.federated_identity(), user.federated_provider(), user.user_id()))

app = webapp2.WSGIApplication([

    ('/', HomePage),
    ('/whatisscl', WhatIs),
    ('/profile', Profile),
    ('/showdata', ShowData)

], debug=True)
