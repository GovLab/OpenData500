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
from tornado.escape import json_encode 

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
            (r"/addData/([a-zA-Z0-9]{24})", SubmitDataHandler),
            (r"/editData/([a-zA-Z0-9]{24})", EditDataHandler),
            (r"/view/([a-zA-Z0-9]{24})", ViewHandler),
            (r"/delete/([a-zA-Z0-9]{24})", DeleteCompanyHandler),
            (r"/recommendCompany", RecommendCompanyHandler)
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
        recommendedCompanies = []
        recommenders = models.Person.objects(personType = "Recommender")
        for r in recommenders:
            recommendedCompanies = recommendedCompanies + r.submittedCompany
        submittedCompanies = []
        submitters = models.Person.objects(personType = "Submitter")
        for s in submitters:
            submittedCompanies = submittedCompanies + s.submittedCompany
        self.render(
            "index.html",
            page_title='OpenData500',
            page_heading='Welcome to the OpenData 500',
            submittedCompanies = submittedCompanies,
            recommendedCompanies = recommendedCompanies
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
        org = self.get_argument("org", None)
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
        if not yearFounded:
            yearFounded = 9999
        fte = self.get_argument("fte", None)
        if not fte:
            fte = 0
        companyFunction = self.get_argument("companyFunction", None)
        if companyFunction == 'other':
            companyFunction = self.get_argument('otherCompanyFunction', None)
        try:
            criticalDataTypes = self.request.arguments['criticalDataTypes']
        except:
            criticalDataTypes = []
        if 'Other' in criticalDataTypes:
            del criticalDataTypes[criticalDataTypes.index('Other')]
            criticalDataTypes.append(self.get_argument('otherCriticalDataTypes', None))
        try:
            revenueSource = self.request.arguments['revenueSource']
        except:
            revenueSource = []
        if 'Other' in revenueSource:
            del revenueSource[revenueSource.index('Other')]
            revenueSource.append(self.get_argument('otherRevenueSource', None))
        try:
            sector = self.request.arguments['sector']
        except:
            sector = []
        if 'Other' in sector:
            del sector[sector.index('Other')]
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
            org = org,
            email = email,
            phone = phone,
            personType = "Submitter",
            datasetWishList = datasetWishList,
            companyRec = companyRec,
            conferenceRec = conferenceRec
        )
        if email == ceoEmail:
            ceo = submitter
            ceo.personType = "CEO"
            ceo.save()
            submitter.save()
        else:
            ceo = models.Person(
                firstName = ceoFirstName,
                lastName = ceoLastName,
                email = ceoEmail,
                personType = "CEO"
            )
            submitter.save()
            ceo.save()
        company = models.Company(
            companyName = companyName,
            url = url,
            ceo = ceo,
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
            submitter = submitter,
            vetted = False
        )
        company.save()
        submitter.submittedCompany.append(company)
        submitter.save()
        id = str(company.id)
        self.redirect("/addData/" + id)

class RecommendCompanyHandler(tornado.web.RequestHandler):
    def get(self, id=None):
        try:
            submitterId = models.Person.objects.get(id=bson.objectid.ObjectId(id))
        except:
            submitterId = None
        self.render(
            "recommendCompany.html",
            page_title = "Recommend a Company",
            page_heading = "Recommend a Company",
            submitterId = submitterId
        )

    def post(self):
        firstName = self.get_argument("firstName", None)                                #Person.Submitter
        lastName = self.get_argument("lastName", None)                                  #Person.Submitter
        title = self.get_argument("title", None)                                        #Person.submitter
        org = self.get_argument("org", None)                                            #Person.Submitter
        email = self.get_argument("email", None)                                        #Person.Submitter
        phone = self.get_argument("phone", None)                                        #Person.Submitter
        companyName = self.get_argument("companyName", None)                            #Company
        url = self.get_argument('url', None)                                            #Company
        firstNameContact = self.get_argument("firstNameContact", None)                  #Company.Contact
        lastNameContact = self.get_argument("lastNameContact", None)                    #Company.Contact
        emailContact = self.get_argument("emailContact", None)                          #Company.Contact
        reasonForRecommending = self.get_argument("reasonForRecommending", None)        #Company
        otherInfo = self.get_argument("otherInfo", None)                                #Person.Submitter
        try: 
            submitter = models.Person.objects.get(id=bson.objectid.ObjectId(id))
        except: 
            submitter = models.Person(
                firstName = firstName, 
                lastName = lastName,
                title = title, 
                org = org,
                email = email,
                phone = phone,
                personType = "Recommender",
                otherInfo = otherInfo
            )
            submitter.save()
        contact = models.Person(
            firstName = firstNameContact,
            lastName = lastNameContact,
            email =emailContact,
            personType = "Contact"
        )
        contact.save()
        company = models.Company(
            companyName = companyName,
            url = url,
            contact = contact,
            reasonForRecommending = reasonForRecommending
        )
        company.save()
        submitter.submittedCompany.append(company)
        submitter.save()
        if self.get_argument('submit', None) == 'Recommend Another Company':
            self.render(
                "recommendCompany.html", 
                page_title = "Recommend a Company",
                page_heading = "Recommend a Company",
                submitterId = str(submitter.id)
            )
        else: 
            self.redirect("/")


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
        id = self.get_argument('id', None)
        company = models.Company.objects.get(id=bson.objectid.ObjectId(id))
        datasetName = self.get_argument('datasetName', None)
        datasetURL = self.get_argument('datasetURL', None)
        try:
            dataType = self.request.arguments['dataType']
        except:
            dataType = []
        if 'Other' in dataType:
            del dataType[dataType.index('Other')]
            dataType.append(self.get_argument('otherDataType', None))
        ratingSubmitted = self.get_argument('rating', None)
        if not ratingSubmitted:
            ratingSubmitted = 9999
        reason = self.get_argument('reason', None)
        author = company.submitter
        dataset = models.Dataset(
            datasetName = datasetName,
            datasetURL = datasetURL,
            dataType = dataType,
        )
        rating = models.Rating(
            author = author,
            rating =ratingSubmitted,
            reason = reason
        )
        dataset.ratings.append(rating)
        dataset.usedBy.append(company)
        dataset.save()
        author.submittedDatasets.append(dataset)
        author.save()
        company.datasets.append(dataset)
        company.save()
        if self.get_argument('submit', None) == 'Add Another':
            self.redirect("/addData/" + id)
        else: 
            self.redirect("/")

class EditCompanyHandler(tornado.web.RequestHandler):
    def get(self, id):
        company = models.Company.objects.get(id=bson.objectid.ObjectId(id))
        page_heading = "Editing " + company.companyName
        page_title = "Editing " + company.companyName
        companyType = ['Public', 'Private', 'Nonprofit']
        companyFunction = ['Consumer Research and/or Marketing', 'Consumer Services', 'Data Management and Analysis', 'Financial/Investment Services', 'Information for Consumers']
        criticalDataTypes = ['Federal Open Data', 'State Open Data', 'City/Local Open Data', 'Private/Proprietary Data Sources']
        revenueSource = ['Advertising', 'Data Management and Analytic Services', 'Database Licensing', 'Lead Generation To Other Businesses', 'Philanthropy', 'Software Licensing', 'Subscriptions', 'User Fees for Web or Mobile Access']
        sectors = ['Agriculture', 'Arts, Entertainment and Recreation' 'Crime', 'Education', 'Energy', 'Environmental', 'Finance', 'Geospatial data/mapping', 'Health and Healthcare', 'Housing/Real Estate', 'Manufacturing', 'Nutrition', 'Scientific Research', 'Social Assistance', 'Trade', 'Transportation', 'Telecom', 'Weather']
        if company is None:
            self.render("404.html", message=id)
        self.render("editCompany.html",
            page_title = page_title,
            page_heading = page_heading,
            company = company,
            companyType = companyType,
            companyFunction = companyFunction,
            criticalDataTypes = criticalDataTypes,
            revenueSource = revenueSource,
            sectors = sectors
        )

    def post(self, id):
        company = models.Company.objects.get(id=bson.objectid.ObjectId(id))
        url = self.get_argument('url', None)
        company.companyName = self.get_argument("companyName", None)
        company.ceo.firstName = self.get_argument("ceoFirstName", None)
        company.ceo.lastName = self.get_argument("ceoLastName", None)
        company.ceo.email = self.get_argument("ceoEmail", None)
        company.companyType = self.get_argument("companyType", None)
        if company.companyType == 'other':
            company.companyType = self.get_argument('otherCompanyType', None)
        company.yearFounded = self.get_argument("yearFounded", 9999)
        company.fte = self.get_argument("fte", 0)
        company.companyFunction = self.get_argument("companyFunction", None)
        if company.companyFunction == 'other':
            company.companyFunction = self.get_argument('otherCompanyFunction', None)
        try:
            company.criticalDataTypes = self.request.arguments['criticalDataTypes']
        except:
            company.criticalDataTypes = []
        if 'Other' in company.criticalDataTypes:
            del company.criticalDataTypes[company.criticalDataTypes.index('Other')]
            if self.get_argument('otherCriticalDataTypes', None):
                company.criticalDataTypes.append(self.get_argument('otherCriticalDataTypes', None))
        try:
            company.revenueSource = self.request.arguments['revenueSource']
        except:
            company.revenueSource = []
        if 'Other' in company.revenueSource:
            del company.revenueSource[company.revenueSource.index('Other')]
            if self.get_argument('otherRevenueSource', None):
                company.revenueSource.append(self.get_argument('otherRevenueSource', None))
        company.sector = self.request.arguments['sector']
        company.sector.append(self.get_argument('otherSector', None))
        company.descriptionLong = self.get_argument('descriptionLong', None)
        company.descriptionShort = self.get_argument('descriptionShort', None)
        company.socialImpact = self.get_argument('socialImpact', None)
        company.financialInfo = self.get_argument('financialInfo', None)
        if self.get_argument('vetted') == 'True':
            company.vetted = True
        elif self.get_argument('vetted') == 'False':
            company.vetted = False
        company.save()
        self.redirect('/')

class EditDataHandler(tornado.web.RequestHandler):
    def get(self, id):
        dataset = models.Dataset.objects.get(id=bson.objectid.ObjectId(id))
        datatypes = ['Federal Open Data', 'State Open Data', 'City/Local Open Data']
        self.render("editData.html",
            page_title = "Editing Dataset",
            page_heading = "Edit Datasets",
            datatypes = datatypes,
            dataset = dataset
        )
    def post(self, id):
        dataset = models.Dataset.objects.get(id=bson.objectid.ObjectId(id))
        dataset.datasetName = self.get_argument('datasetName', None)
        dataset.datasetURL = self.get_argument('datasetURL', None)
        try:
            dataset.dataType = self.request.arguments['dataType']
        except:
            dataset.dataType = []
        if 'Other' in dataset.dataType:
            del dataset.dataType[dataset.dataType.index('Other')]
            dataset.dataType.append(self.get_argument('otherDataType', None))
        dataset.save()
        self.redirect("/")

class DeleteCompanyHandler(tornado.web.RequestHandler):
    def get(self, id):
        try:
            company = models.Company.objects.get(id=bson.objectid.ObjectId(id)) 
            #we're deleting a company. Need to delete CEO, delete 
            if company.ceo:
                ceo = company.ceo
                ceo.delete()
            company.delete()
        except:
            dataset = models.Dataset.objects.get(id=bson.objectid.ObjectId(id))
            dataset.delete()
        self.redirect('/')

class ViewHandler(tornado.web.RequestHandler):
    def get(self, id):
        c = models.Company.objects.get(id=bson.objectid.ObjectId(id))
        d = []
        for s in c.datasets:
            ratings = []
            for r in s.ratings:
                ratings.append({
                    "author": str(r.author.id),
                    "rating": r.rating,
                    "reason": r.reason
                })
            companies = []
            for comps in s.usedBy:
                companies.append({
                    "companyID": str(comps.id)
                })
            d.append({
                "ts": str(s.ts),
                "datasetName": s.datasetName,
                "datasetURL": s.datasetURL,
                "ratings": ratings,
                "dataType": s.dataType,
                "usedBy": companies
            })
        obj = {
            "_id": {
                "$oid": str(c.id)
            },
            "ceo": {
                "firstName": c.ceo.firstName,
                "lastName": c.ceo.lastName,
                "personType": c.ceo.personType,
                "email": c.ceo.email,
                "ratings": [],
                "submittedDatasets": []
            },
            "companyFunction": c.companyFunction,
            "companyName": c.companyName,
            "companyType": c.companyType,
            "criticalDataTypes": c.criticalDataTypes,
            "datasets": d,
            "descriptionLong": c.descriptionLong,
            "descriptionShort": c.descriptionShort,
            "financialInfo": c.financialInfo,
            "fte": c.fte,
            "revenueSource": c.revenueSource,
            "sector": c.sector,
            "socialImpact": c.socialImpact,
            "submitter": {
                "firstName": c.submitter.firstName,
                "lastName": c.submitter.lastName,
                "personType": c.submitter.personType,
                "email": c.submitter.email,
                "submittedDatasets": str(c.submitter.submittedDatasets)
            },
            "ts": str(c.ts),
            "url": c.url,
            "vetted": c.vetted,
            "yearFounded": c.yearFounded
        }
        self.write(json_encode(obj))


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









































