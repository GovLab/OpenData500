#    Sample main.py Tornado file
#    (for Tornado on Heroku)
#
#    Author: Mike Dory | dory.me
#    Created: 11.12.11 | Updated: 06.02.13
#    Contributions by Tedb0t, gregory80
#
# ------------------------------------------

#!/usr/bin/env python
import os.path
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

#Mongo
from mongoengine import *
import models
import bson
from bson import json_util

# import and define tornado-y things
from tornado.options import define
define("port", default=5000, help="run on the given port", type=int)

#Connect to mongo
connect('db', host=os.environ.get('MONGOLAB_URI'))

# application settings and handle mapping info
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/submitCompany", SubmitCompanyHandler),
            (r"/edit/([a-zA-Z0-9]{24})", EditCompanyHandler),
            (r"/addData/([a-zA-Z0-9]{24})", SubmitDataHandler)
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            ui_modules={"Company": CompanyModule},
            debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)


# the main page
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        companies = models.Company.objects()
        self.render(
            "index.html",
            page_title='OpenData500',
            page_heading='Welcome to the OpenData 500',
            companies = companies
        )

class SubmitCompanyHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(
            "submitCompany.html",
            page_title = "Submit a Company",
            page_heading = "Submit a Company"
        )
    def post(self):
        firstName = self.get_argument("firstName", None)
        lastName = self.get_argument("lastName", None)
        url = self.get_argument('url', None)
        companyName = self.get_argument("companyName", None)
        email = self.get_argument("email", None)
        phone = self.get_argument("phone", None)
        ceoFirstName = self.get_argument("ceoFirstName", None)
        ceoLastName = self.get_argument("ceoLastName", None)
        ceoEmail = self.get_argument("ceoEmail", None)
        companyType = self.get_argument("companyType", None)
        if companyType == 'other':
            companyType = self.get_argument('otherCompanyType', None)
        yearFounded = self.get_argument("yearFounded", None)
        fte = self.get_argument("fte", None)
        companyFunction = self.get_argument("companyFunction", None)
        if companyFunction == 'other':
            companyFunction = self.get_argument('otherCompanyFunction', None)
        criticalDataTypes = self.request.arguments['criticalDataTypes']
        criticalDataTypes.append(self.get_argument('otherCriticalDataTypes', None))
        revenueSource = self.request.arguments['revenueSource']
        revenueSource.append(self.get_argument('otherRevenueSource', None))
        sector = self.request.arguments['sector']
        sector.append(self.get_argument('otherSector', None))
        descriptionLong = self.get_argument('descriptionLong', None)
        descriptionShort = self.get_argument('descriptionShort', None)
        socialImpact = self.get_argument('socialImpact', None)
        financialInfo = self.get_argument('financialInfo')
        datasetWishList = self.get_argument('datasetWishList', None)
        companyRec = self.get_argument('companyRec', None)
        conferenceRec = self.get_argument('conferenceRec', None)
        submitter = models.Person(
            firstName = firstName,
            lastName = lastName,
            email = email,
            phone = phone,
            personType = "Submitter",
            datasetWishList = datasetWishList,
            companyRec = companyRec,
            conferenceRec = conferenceRec
        )
        ceo = models.Person(
            firstName = ceoFirstName,
            lastName = ceoLastName,
            email = ceoEmail,
            personType = "CEO"
        )
        company = models.Company(
            companyName = companyName,
            url = url,
            ceo = ceo,
            submitter = submitter,
            yearFounded = yearFounded,
            fte = fte,
            companyType = companyType,
            companyFunction = companyFunction,
            criticalDataTypes = criticalDataTypes,
            revenueSource = revenueSource,
            sector = sector,
            descriptionLong = descriptionLong,
            descriptionShort = descriptionShort,
            socialImpact = socialImpact,
            financialInfo = financialInfo,
            vetted = False
        )
        company.save()
        id = str(company.id)
        self.redirect("/addData/" + id)

class SubmitDataHandler(tornado.web.RequestHandler):
    def get(self, id):
        company = models.Company.objects.get(id=bson.objectid.ObjectId(id))
        page_heading = "Enter Data Sets for " + company.companyName
        self.render("submitData.html",
            page_title = "Submit Data Sets For Company",
            page_heading = page_heading,
            id = id
        )
    def post(self, id):
        datasetName = self.get_argument('datasetName', None)
        datasetURL = self.get_argument('datasetURL', None)
        dataType = self.request.arguments['dataType']
        dataType.append(self.get_argument('dataType', None))
        rating = self.get_argument('rating', None)
        reason = self.get_argument('reason', None)
        dataset = models.Dataset(
            datasetName = datasetName,
            datasetURL = datasetURL,
            dataType = dataType,
            rating = rating, 
            reason = reason,
        )
        id = self.get_argument('id', None)
        company = models.Company.objects.get(id=bson.objectid.ObjectId(id))
        company.datasets.append(dataset)
        company.save()
        self.redirect("/")

class EditCompanyHandler(tornado.web.RequestHandler):
    def get(self, id):
        company = models.Company.objects.get(id=bson.objectid.ObjectId(id))
        page_heading = "Editing " + company.companyName
        page_title = "Editing " + company.companyName
        if company is None:
            self.render("404.html", message=id)
        self.render("editCompany.html",
            page_title = page_title,
            page_heading = page_heading,
            company = company
        )

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


# RAMMING SPEEEEEEED!
def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(tornado.options.options.port)

    # start it up
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()









































