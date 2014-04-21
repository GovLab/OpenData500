#!/usr/bin/env python
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
import models
import bson
from bson import json_util
import csv
import json
import re
import bcrypt
from datetime import datetime
from utils import *
from handlers.handlers import *

# import and define tornado-y things
from tornado.options import define
define("port", default=5000, help="run on the given port", type=int)

#Connect to mongo
connect('db', host=os.environ.get('MONGOLAB_URI'))

# application settings and handle mapping info
class Application(tornado.web.Application):
    def __init__(self):
        self.stats = StatsGenerator()
        self.files = FileGenerator()
        handlers = [
            (r'/(favicon.ico)', tornado.web.StaticFileHandler, {"path": ""}),
            (r"/", MainHandler),
            (r"/sankeyChart/?", SankeyChartHandler),
            (r"/submitCompany/?", SubmitCompanyHandler),
            (r"/validate/?", ValidateHandler),
            (r"/edit/([a-zA-Z0-9]{24})/?", EditCompanyHandler),
            (r"/addData/([a-zA-Z0-9]{24})/?", SubmitDataHandler),
            (r"/media/?", MediaHandler),
            (r"/delete/([a-zA-Z0-9]{24})/?", DeleteCompanyHandler),
            (r"/admin/?", AdminHandler),
            (r"/admin/edit/([a-zA-Z0-9]{24})/?", AdminEditCompanyHandler),
            (r"/about/?", AboutHandler),
            (r"/resources/?", ResourcesHandler),
            (r"/stats/?", FindingsHandler),
            (r"/chart/?", ChartHandler),
            (r"/download/?", DownloadHandler),
            (r'/download/(.*)/?',tornado.web.StaticFileHandler, {'path':os.path.join(os.path.dirname(__file__), 'static')}),
            (r"/candidates/?", CandidateHandler),
            (r"/list/?", ListHandler),
            (r'/thanks/?', ThanksHandler),
            (r'/login/?', LoginHandler),
            (r'/logout/?', LogoutHandler),
            (r'/register/?', RegisterHandler),
            (r"/([^/]+)/?", CompanyHandler)
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            ui_modules={
                "Company": CompanyModule,
                "datetime": datetime},
            debug=True,
            cookie_secret=os.environ.get('COOKIE_SECRET'),
            xsrf_cookies=True,
            login_url="/login"
        )
        tornado.web.Application.__init__(self, handlers, **settings)

class CompanyModule(tornado.web.UIModule):
    def render(self, company):
        return self.render_string(
            "modules/company.html",
            company=company
        )
    def css_files(self):
        return "/static/css/styles.css"
    def javascript_files(self):
        return "/static/js/script.js"

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(tornado.options.options.port)

    # start it up
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()









































