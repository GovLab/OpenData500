import os.path
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.escape import json_encode
import logging

#Mongo
from mongoengine import *
from models import *
import bson
from bson import json_util
import csv
import json
import re
import bcrypt
from datetime import datetime
from utils import *
from geoip import geolite2

class BaseHandler(tornado.web.RequestHandler):
    def get_login_url(self):
        return u"/login"

    def get_current_user(self):
        user_json = self.get_secure_cookie("user")
        if user_json:
            return tornado.escape.json_decode(user_json)
        else:
            return None

    def get_current_language(self):
        logging.info('======= test get language =======')
        return self.get_secure_cookie('lan')

    def load_country(self, country):
        logging.info('======= test load country =======')
        if not country:
            self.redirect("/404/")
            return
        if country not in available_countries:
            self.redirect("/404/")
            return
        else:
            return country

    def load_settings(self, country):
        with open("templates/"+country+"/settings.json") as json_file:
            return json.load(json_file)

    def load_language(self, country, lan, settings):
        logging.info('======= test load language =======')
        current_language = self.get_cookie('lan')
        if lan:
            if lan != current_language and lan in settings['available_languages']:
                self.set_cookie("lan", lan)
                self.redirect(self.request.uri)
                return False
            if lan not in settings['available_languages']:
                lan = settings['default_language']
        elif not lan and self.get_cookie('lan') in settings['available_languages']:
            lan = self.get_cookie('lan')
        else:
            lan = settings['default_language']
        return lan

    def prepare(self):
        # Hacky -- check if this is a country URL.  If that country is locked,
        # require a login.
        if (re.match(r"/(?:([A-Za-z]{2})/)", self.request.uri)):
            country_settings = self.load_settings(self.request.uri[1:3])
            if country_settings.get(u"locked"):
                if not self.current_user:
                    self.redirect(self.get_login_url())
