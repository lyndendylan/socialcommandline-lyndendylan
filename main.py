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
import oauthclient
import oauthclient.forms
import oauthclient.models
import functools
import twitter
import TwitterController

from gaesessions import get_current_session
from gaesessions import delete_expired_sessions
from google.appengine.ext import ndb
from google.appengine.api import mail
from google.appengine.api import users
from xml.dom import minidom



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
        twitter_service = TwitterController.get_twitter_service()
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

class TwitterAuthorized(MainHandler):
    def get(self):
        twitter_service = oauthclient.models.OAuthService.get_by_key_name("twitter")
        verifier = self.request.get("oauth_verifier")
        session = get_current_session()
        key = session.get('twitter_request_key')
        secret = session.get('twitter_request_secret')
        if key is None or secret is None:
            self.error(500)
            return

        key, secret = oauthclient.exchange_request_token_for_access_token(twitter_service.consumer_key,
                                                                          twitter_service.consumer_secret,
                                                                          twitter_service.access_token_url,
                                                                          verifier,
                                                                          key,
                                                                          secret)

        twitapi = twitter.Api(twitter_service.consumer_key,
                              twitter_service.consumer_secret,
                              key,
                              secret,
                              cache=None)

        twituser = twitapi.VerifyCredentials()
        profile = Profile.get_by_key_name(twituser.screen_name)
        if profile is None:
            profile = Profile(key_name=twituser.screen_name)

        profile.twitter_access_token_key = key
        profile.twitter_access_token_secret = secret
        profile.save()
        session["twitter_screen_name"] = twituser.screen_name
        self.redirect("/profile")

class Admin(MainHandler):
    def get(self):
        service_formset = oauthclient.forms.create_service_formset()
        self.render("admin.html", service_formset=service_formset)

    def post(self):
        admin_formset = oauthclient.forms.create_service_formset(self.request.POST)
        if oauthclient.forms.save_formset(admin_formset):
            self.redirect("/")
        else:
            self.redirect("/admin")

class SignInWithTwitter(MainHandler):
    def get(self):
        twitter_service = oauthclient.models.OAuthService.get_by_key_name("twitter")

        key, secret = oauthclient.retrieve_service_request_token(twitter_service.request_token_url,
                                                                 twitter_service.consumer_key,
                                                                 twitter_service.consumer_secret)
        session = get_current_session()
        if session.is_active():
            session.terminate()
        session['twitter_request_key'] = key
        session['twitter_request_secret'] = secret

        self.redirect(oauthclient.generate_authorize_url(twitter_service.authenticate_url, key))

class SignOut(MainHandler):
    def get(self):
        session = get_current_session()
        if session.is_active():
            session.terminate()
        self.redirect("/")


def check_user_exists(user):
    pass

def show_info(user):
	logging.info("nickname: %s, auth_domain: %s, email: %s, federated_identity: %s, federated_provided: %s, user_id: %s " % (user.nickname(), user.auth_domain(), user.email(), user.federated_identity(), user.federated_provider(), user.user_id()))

app = webapp2.WSGIApplication([

    ('/', HomePage),
    ('/whatisscl', WhatIs),
    ('/profile', Profile),
    ('/showdata', ShowData),
    ('/registertwitter', RegisterTwitter),
    ('/admin', Admin),
    ('/signin', SignInWithTwitter),
    ('/twitterauthorized', TwitterAuthorized),
    ('/signout', SignOut)



], debug=True)
