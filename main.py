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
            # (r"/2/?", SankeeyChartHandler),
            (r"/3/?", ChordDiagramHandler),
            (r"/submitCompany/?", SubmitCompanyHandler),
            (r"/validate/?", ValidateHandler),
            (r"/edit/([a-zA-Z0-9]{24})/?", EditCompanyHandler),
            (r"/addData/([a-zA-Z0-9]{24})/?", SubmitDataHandler),
            (r"/media/?", MediaHandler),
            (r"/delete/([a-zA-Z0-9]{24})/?", DeleteCompanyHandler),
            (r"/deleteData/([a-zA-Z0-9]{24})/?", DeleteDatasetHandler),
            (r"/admin/?", AdminHandler),
            (r"/admin/edit/([a-zA-Z0-9]{24})/?", AdminEditCompanyHandler),
            (r"/about/?", AboutHandler),
            (r"/resources/?", ResourcesHandler),
            (r"/findings/?", FindingsHandler),
            #(r"/files/?", FilesHandler),
            (r"/download/?", DownloadHandler),
            (r'/download/(.*)/?',tornado.web.StaticFileHandler, {'path':os.path.join(os.path.dirname(__file__), 'static')}),
            (r"/candidates/?", CandidateHandler),
            (r"/preview/?", PreviewHandler),
            (r'/thanks/?', ThanksHandler),
            (r'/login/?', LoginHandler),
            (r'/logout/?', LogoutHandler),
            (r'/register/?', RegisterHandler),
            (r"/media/?", MediaHandler),
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

class BaseHandler(tornado.web.RequestHandler): 
    def get_login_url(self):
        return u"/login"
    def get_current_user(self):
        user_json = self.get_secure_cookie("user")
        if user_json:
            return tornado.escape.json_decode(user_json)
        else:
            return None

# the main page
class MainHandler(BaseHandler):
    @tornado.web.addslash
    #@tornado.web.authenticated
    def get(self):
        self.render(
            "index.html",
            user=self.current_user,
            page_title='Open Data500',
            page_heading='Welcome to the Open Data 500 Pre-Launch',
        )


class ChordDiagramHandler(BaseHandler):
    @tornado.web.addslash
    @tornado.web.authenticated
    def get(self):
        self.render(
            "index3.html",
            user=self.current_user,
            page_title='Open Data500',
            page_heading='Welcome to the Open Data 500 Pre-Launch',
        )

class LoginHandler(BaseHandler): 
    @tornado.web.addslash
    def get(self):
        self.render(
            "login.html", 
            next=self.get_argument("next","/"), 
            message=self.get_argument("error",""),
            page_title="Please Login",
            page_heading="Login to OD500" 
            )

    def post(self):
        email = self.get_argument("email", "")
        password = self.get_argument("password", "").encode('utf-8')
        user = models.Users.objects.get(email=email)
        if user and user.password and bcrypt.hashpw(password, user.password.encode('utf-8')) == user.password:
            logging.info('successful login for '+email)
            self.set_current_user(email)
            self.redirect("/")
        else: 
            logging.info('unsuccessful login')
            error_msg = u"?error=" + tornado.escape.url_escape("Login incorrect.")
            self.redirect(u"/login" + error_msg)

    def set_current_user(self, user):
        logging.info('setting ' + user)
        if user:
            self.set_secure_cookie("user", tornado.escape.json_encode(user))
        else: 
            self.clear_cookie("user")

class MediaHandler(BaseHandler):
    @tornado.web.addslash
    def get(self):
        self.render(
            "media.html",
            user=self.current_user,
            page_title="Media"
            )

class FindingsHandler(BaseHandler):
    @tornado.web.addslash
    def get(self):
        self.render(
            "findings.html",
            user=self.current_user,
            page_title="Findings"
            )

class ThanksHandler(BaseHandler): 
    @tornado.web.addslash
    def get(self):
        self.render(
            "thankyou.html", 
            user=self.current_user,
            page_title="OD500 - Thanks!",
            page_heading="Thank you for participating in the Open Data 500!" 
            )

class RegisterHandler(LoginHandler):
    @tornado.web.addslash
    @tornado.web.authenticated
    def get(self):
        self.render(
            "register.html", 
            next=self.get_argument("next","/"),
            page_title="Register",
            page_heading="Register for OD500"
            )

    @tornado.web.authenticated
    def post(self):
        email = self.get_argument("email", "")
        try:
            user = models.Users.objects.get(email=email)
        except:
            user = ''
        if user:
            error_msg = u"?error=" + tornado.escape.url_escape("Login name already taken")
            self.redirect(u"/register" + error_msg)
        else: 
            password = self.get_argument("password", "")
            hashedPassword = bcrypt.hashpw(password, bcrypt.gensalt(8))
            newUser = models.Users(
                email=email,
                password = hashedPassword
                )
            newUser.save()
            self.set_current_user(email)
            self.redirect("/")

class LogoutHandler(BaseHandler): 
    def get(self):
        self.clear_cookie("user")
        self.redirect(u"/login")


class CompanyHandler(BaseHandler):
    @tornado.web.addslash
    #@tornado.web.authenticated
    def get(self, companyName):
        try:
            try:
                company = models.Company2.objects.get(prettyName=companyName)
            except Exception, e:
                logging.info("Company: " + companyName + ": " + str(e))
                company = models.Company2.objects(prettyName=companyName)[0]
            self.render(
            "company.html",
            page_title='Open Data500',
            user=self.current_user,
            page_heading=company.companyName,
            company = company,
        )
        except Exception, e:
            logging.info("Company: " + companyName + ": " + str(e)) 
            self.render(
                "404.html",
                page_title='404 - Open Data500',
                user=self.current_user,
                page_heading='Hmm...',
                error = '404 - Not Found'
            )
        

      
class PreviewHandler(BaseHandler):
    @tornado.web.addslash
    #@tornado.web.authenticated
    def get(self):
        companies = models.Company.objects(preview50=True).order_by('prettyName')
        self.render(
            "preview.html",
            page_title='Open Data500',
            page_heading='Preview of the Open Data 500',
            companies = companies,
            user=self.current_user
        )

class CandidateHandler(BaseHandler):
    @tornado.web.addslash
    #@tornado.web.authenticated
    def get(self):
        companies = models.Company2.objects(display=True).order_by('prettyName')
        agencies = models.Agency.objects(Q(usedBy__not__size=0) & Q(source="dataGov") & Q(dataType="Federal")).order_by("-usedBy_count").only("name", "abbrev")[0:16]
        stats = models.Stats.objects().first()
        self.render(
            "candidates.html",
            page_title='Open Data 500',
            page_heading='OD500 Companies',
            companies = companies,
            stats = stats,
            #recentlySubmitted=recentlySubmitted,
            states=states,
            agencies = agencies,
            categories = categories,
            user=self.current_user,
            #stateInfo=stateInfo
        )

class AboutHandler(BaseHandler):
    @tornado.web.addslash
    #@tornado.web.authenticated
    def get(self):
        self.render(
            "about.html",
            page_title='About the OpenData500',
            page_heading='About the OpenData 500',
            user=self.current_user
        )

class ResourcesHandler(BaseHandler):
    @tornado.web.addslash
    #@tornado.web.authenticated
    def get(self):
        self.render(
            "resources.html",
            page_title='Open Data Resources',
            user=self.current_user,
            page_heading='Open Data Resources'
        )

class AdminHandler(BaseHandler):
    @tornado.web.addslash
    @tornado.web.authenticated
    def get(self):
        surveySubmitted = models.Company2.objects(Q(submittedSurvey=True) & Q(vetted=True)).order_by('prettyName')
        sendSurveys = models.Company2.objects(Q(submittedSurvey=False))
        needVetting = models.Company2.objects(Q(submittedSurvey=True) & Q(vetted=False)).order_by('-lastUpdated', 'prettyName')
        stats = models.Stats.objects().first()
        if self.current_user == 'alex' or self.current_user == 'Elizabeth':
            self.render('404.html',
                page_heading="I'm afraid I can't let you do that.",
                page_title="Forbidden",
                error="Not Enough Priviliges")
        else:
            self.render(
                "admin.html",
                page_title='OpenData500',
                page_heading='Welcome to the OpenData 500',
                surveySubmitted = surveySubmitted,
                needVetting = needVetting,
                user=self.current_user,
                sendSurveys = sendSurveys,
                stats = stats
            )
    def post(self):
        action = self.get_argument("action", None)
        if action == "refresh":
            self.application.stats.refresh_stats()
            stats = models.Stats.objects().first()
            self.write({"totalCompanies": stats.totalCompanies, "totalCompaniesWeb":stats.totalCompaniesWeb, "totalCompaniesSurvey":stats.totalCompaniesSurvey})
        elif action == "files":
            #self.application.files.generate_company_json()
            #self.application.files.generate_agency_json()
            self.application.files.generate_company_csv()
            self.application.files.generate_company_all_csv()
            #self.application.files.generate_agency_csv()
            self.write("success")
        elif action == "sankey":
            #self.application.files.generate_sankey_json()
            self.application.files.generate_chord_chart_files()
            self.write("success")
        elif action == 'display':
            try:
                id = self.get_argument("id", None)
                c = models.Company2.objects.get(id=bson.objectid.ObjectId(id))
            except Exception, e:
                logging.info("Error: " + str(e))
                self.write(str(e))
            c.display = not c.display
            c.save()
            self.application.stats.update_all_state_counts()
            self.write("success")
        elif action == 'agency_csv':
            self.application.files.generate_agency_csv()
            self.write("success")


class ValidateHandler(BaseHandler):
    def post(self):
        #check if companyName exists:
        companyName = self.get_argument("companyName", None)
        prettyName = re.sub(r'([^\s\w])+', '', companyName).replace(" ", "-").title()
        logging.info(prettyName)
        try: 
            c = models.Company2.objects.get(prettyName=prettyName)
            logging.info('company exists.')
            self.write('{ "error": "This company has already been submitted. Email opendata500@thegovlab.org for questions." }')
        except:
            logging.info('company does not exist. Carry on.')
            self.write('true')


class SubmitCompanyHandler(BaseHandler):
    @tornado.web.addslash
    #@tornado.web.authenticated
    def get(self):
        self.render(
            "submitCompany.html",
            page_title = "Submit Your Company",
            page_heading = "Submit Your Company",
            companyType = companyType,
            companyFunction = companyFunction,
            criticalDataTypes = criticalDataTypes,
            revenueSource = revenueSource,
            categories=categories,
            datatypes = datatypes,
            stateList = stateList,
            user=self.current_user,
            stateListAbbrev=stateListAbbrev
        )

    #@tornado.web.authenticated
    def post(self):
        #print all arguments to log:
        logging.info("Submitting New Company")
        logging.info(self.request.arguments)
        #-------------------CONTACT INFO---------------
        firstName = self.get_argument("firstName", None)
        lastName = self.get_argument("lastName", None)
        title = self.get_argument("title", None)
        email = self.get_argument("email", None)
        phone = self.get_argument("phone", None)
        try:
            if self.request.arguments['contacted']:
                contacted = True
        except:
            contacted = False
        contact = models.Person2(
            firstName = firstName,
            lastName = lastName,
            title = title,
            email = email,
            phone = phone,
            contacted = contacted,
        )
        #-------------------CEO INFO---------------
        ceoFirstName = self.get_argument("ceoFirstName", None)
        ceoLastName = self.get_argument("ceoLastName", None)
        ceo = models.Person2(
                firstName = ceoFirstName,
                lastName = ceoLastName,
                title = "CEO"
            )
        #-------------------COMPANY INFO---------------
        url = self.get_argument('url', None)
        companyName = self.get_argument("companyName", None)
        prettyName = re.sub(r'([^\s\w])+', '', companyName).replace(" ", "-").title()
        city = self.get_argument("city", None)
        zipCode = self.get_argument("zipCode", None)
        state = self.get_argument('state', None)
        companyType = self.get_argument("companyType", None)
        if companyType == 'other':
            companyType = self.get_argument('otherCompanyType', None)
        yearFounded = self.get_argument("yearFounded", None)
        if not yearFounded:
            yearFounded = 0
        fte = self.get_argument("fte", None).replace(",","")
        if not fte:
            fte = 0
        try:
            revenueSource = self.request.arguments['revenueSource']
        except:
            revenueSource = []
        if 'Other' in revenueSource:
            del revenueSource[revenueSource.index('Other')]
            revenueSource.append(self.get_argument('otherRevenueSource', None))
        companyCategory = self.get_argument("category", None)
        if companyCategory == 'Other':
            companyCategory = self.get_argument('otherCategory', None)
        description = self.get_argument('description', None)
        descriptionShort = self.get_argument('descriptionShort', None)
        financialInfo = self.get_argument('financialInfo')
        datasetWishList = self.get_argument('datasetWishList', None)
        sourceCount = self.get_argument("sourceCount", None)
        #--SAVE COMPANY--
        company = models.Company2(
            companyName = companyName,
            prettyName = prettyName,
            url = url,
            ceo = ceo,
            city = city,
            zipCode = zipCode,
            state=state,
            yearFounded = yearFounded,
            fte = fte,
            companyType = companyType,
            revenueSource = revenueSource,
            companyCategory = companyCategory,
            description= description,
            descriptionShort = descriptionShort,
            financialInfo = financialInfo,
            datasetWishList = datasetWishList,
            sourceCount = sourceCount,
            contact = contact,
            lastUpdated = datetime.now(),
            display = False, 
            submittedSurvey = True,
            vetted = False, 
            vettedByCompany = True,
            submittedThroughWebsite = True,
            locked=False
        )
        company.save()
        self.application.stats.update_all_state_counts()
        id = str(company.id)
        self.write({"id": id})


class SubmitDataHandler(BaseHandler):
    @tornado.web.addslash
    #@tornado.web.authenticated
    def get(self, id):
        #Make not whether we are submitting a Co. and adding a dataset or editing a Co. and adding a dataset
        #get company
        company = models.Company2.objects.get(id=bson.objectid.ObjectId(id))
        page_heading = "Agency and Data Information for " + company.companyName
        self.render("submitData.html",
            page_title = "Submit Data Sets For Company",
            page_heading = page_heading,
            company = company,
            user=self.current_user
        )

    #@tornado.web.authenticated
    def post(self, id):
        logging.info("Submitting Data: "+ self.get_argument("action", None))
        logging.info(self.request.arguments)
        try:
            company = models.Company2.objects.get(id=bson.objectid.ObjectId(id))
        except Exception, e:
            logging.info("Could not get company: " + str(e))
            self.set_status(400)
        agencyName = self.get_argument("agency", None)
        a_id = self.get_argument("a_id", None)
        subagencyName = self.get_argument("subagency", None)
        action = self.get_argument("action", None)
        #------------------------------------JUST SAVE DATA COMMENT QUESTION------------------------
        if action == "dataComments":
            logging.info("saving " + self.get_argument('dataComments', None))
            company.dataComments = self.get_argument('dataComments', None)
            company.lastUpdated = datetime.now()
            company.save()
            self.write("success")
        #------------------------------------ADDING AGENCY/SUBAGENCY------------------------
        if action == "add agency":
            #Existing AGENCY
            logging.info("Trying to get: " + agencyName)
            try:
                agency = models.Agency.objects.get(name=agencyName)
            except Exception, e:
                logging.info("Error: " + str(e))
                self.set_status(400)
            for s in agency.subagencies:
                if s.name == subagencyName:
                    if company not in s.usedBy: #only add if it's not already there.
                        s.usedBy.append(company)
            agency.save()
            if company not in agency.usedBy: #only add if it's not already there.
                agency.usedBy.append(company)
                agency.usedBy_count = len(agency.usedBy)
                agency.save()
            if agency not in company.agencies: #only add if it's not already there.
                company.agencies.append(agency)
                company.save()
            company.lastUpdated = datetime.now() #Update Company's Time of Last Edit
            company.save()
            self.write("success")
        #------------------------------------DELETING AGENCY/SUBAGENCY------------------------
        if action == "delete agency":
            try: 
                agency = models.Agency.objects.get(id=bson.objectid.ObjectId(a_id))
            except Exception, e:
                logging.info("Can't Delete Agency(search by ID): " + str(e))
                try:
                    agency = models.Agency.objects.get(name=agencyName)
                except Exception, e:
                    logging.info("Can't Delete Agency(Search by name): "+str(e))
                    self.set_status(400)
            if subagencyName == '': #delete from agency and subagency
                #remove datasets from agency:
                temp = []
                for d in agency.datasets:
                    if company != d.usedBy:
                        temp.append(d)
                    agency.datasets = temp
                #remove agency from company
                if agency in company.agencies:
                    company.agencies.remove(agency)
                #remove company from agency
                if company in agency.usedBy:
                    agency.usedBy.remove(company)
                #remove datasets from subagencies
                for s in agency.subagencies:
                    if company in s.usedBy: #does the company even use this subagency?
                        temp = []
                        for d in s.datasets: #loop through all datasets for each subagency
                            if company != d.usedBy: #to make an array of the datasets not used by company
                                temp.append(d)
                        s.datasets = temp #and then set the datasets array equal to the remaining.
                        s.usedBy.remove(company)
                #remove from all subagencies
                for s in agency.subagencies:
                    if company in s.usedBy and s.name == subagencyName:
                        s.usedBy.remove(company)
            if subagencyName: #removing just subagency
                #remove datasets from subagency:
                temp = []
                for s in agency.subagencies:
                    if s.name == subagencyName:
                        for d in s.datasets:
                            if company != d.usedBy:
                                temp.append(d)
                        s.datasets = temp
                        #s.usedBy.remove(company)
                #remove company from specific subagency
                for s in agency.subagencies:
                    if company in s.usedBy and s.name == subagencyName:
                        s.usedBy.remove(company)
            agency.usedBy_count = len(agency.usedBy)
            agency.save()
            company.lastUpdated = datetime.now() #Update Company's Time of Last Edit
            company.save()
            self.write("deleted")
        #------------------------------------ADDING DATASET------------------------
        if action == "add dataset":
            try:
                agency = models.Agency.objects.get(name = agencyName)
                logging.info(agency.name)
            except Exception, e:
                logging.info(str(e))
                logging.info("Agency Id: " + agencyName)
                self.set_status(500)
            datasetName = self.get_argument("datasetName", None)
            datasetURL = self.get_argument("datasetURL", None)
            try: 
                rating = int(self.get_argument("rating", None))
            except:
                rating = 0
            dataset = models.Dataset2(
                datasetName = datasetName,
                datasetURL = datasetURL,
                rating = rating,
                usedBy = company)
            #Adding to agency or subagency?
            if subagencyName == '':
                #Add to Agency
                agency.datasets.append(dataset)
            else:
                #add to subagency
                for s in agency.subagencies:
                    if subagencyName == s.name:
                        s.datasets.append(dataset)
            agency.save()
            company.lastUpdated = datetime.now() #Update Company's Time of Last Edit
            company.save()
            self.write("success")
        #------------------------------------EDITING DATASET------------------------
        if action == "edit dataset":
            try:
                agency = models.Agency.objects.get(name=agencyName)
            except:
                self.set_status(400)
            datasetName = self.get_argument("datasetName", None)
            previousDatasetName = self.get_argument("previousDatasetName", None)
            datasetURL = self.get_argument("datasetURL", None)
            try: 
                rating = int(self.get_argument("rating", None))
            except:
                rating = 0
            #-- At Agency Level?--
            if subagencyName == '':
                #find dataset:
                for d in agency.datasets:
                    if d.datasetName == previousDatasetName:
                        d.datasetName = datasetName
                        d.datasetURL = datasetURL
                        d.rating = rating
            else: #look for dataset in subagencies
                for s in agency.subagencies:
                    if s.name == subagencyName:
                        for d in s.datasets:
                            if d.datasetName == previousDatasetName:
                                d.datasetName = datasetName
                                d.datasetURL = datasetURL
                                d.rating = rating
            agency.save()
            company.lastUpdated = datetime.now() #Update Company's Time of Last Edit
            company.save()
            self.write("success")
        #------------------------------------DELETING DATASET------------------------
        if action == "delete dataset":
            try:
                agency = models.Agency.objects.get(name=agencyName)
            except:
                self.set_status(400)
            datasetName = self.get_argument("datasetName", None)
            #Find dataset
            #--At Agency level?--
            if subagencyName == '':
                for d in agency.datasets:
                    if d.datasetName == datasetName:
                        agency.datasets.remove(d)
            else: #--SUBAGENCY LEVEL--
                for s in agency.subagencies:
                    if s.name == subagencyName:
                        for d in s.datasets:
                            if d.datasetName == datasetName:
                                s.datasets.remove(d)
            agency.save()
            company.lastUpdated = datetime.now() #Update Company's Time of Last Edit
            company.save()
            self.write("success")

class EditCompanyHandler(BaseHandler):
    @tornado.web.addslash
    def get(self, id):
        try: 
            company = models.Company2.objects.get(id=bson.objectid.ObjectId(id))
            #Datasets by agency, with no subagency
            page_heading = "Editing " + company.companyName
            page_title = "Editing " + company.companyName
        except:
            self.render("404.html", 
                page_title = "That ain't even a thing.",
                page_heading = "Check yo'self",
                error = "404 - Not Found",
                user=self.current_user,
                message=id)
        if company.locked:
            self.render("404.html",
                page_title = "Can't Edit This Company",
                page_heading = "This company is locked from editing",
                error = "locked")
        else:
            self.render("editCompany.html",
                page_title = page_title,
                page_heading = page_heading,
                company = company,
                companyType = companyType,
                companyFunction = companyFunction,
                criticalDataTypes = criticalDataTypes,
                revenueSource = revenueSource,
                categories=categories,
                datatypes = datatypes,
                stateList = stateList,
                stateListAbbrev=stateListAbbrev,
                user=self.current_user,
                id = str(company.id)
            )

    def post(self, id):
        #save all data to log:
        logging.info("Editing company:")
        logging.info(self.request.arguments)
        #get the company you will be editing
        company = models.Company2.objects.get(id=bson.objectid.ObjectId(id))
        #------------------CONTACT INFO-------------------
        company.contact.firstName = self.get_argument("firstName", None)
        company.contact.lastName = self.get_argument("lastName", None)
        company.contact.title = self.get_argument("title", None)
        company.contact.org = self.get_argument("org", None)
        company.contact.email = self.get_argument("email", None)
        company.contact.phone = self.get_argument("phone", None)
        try: 
            if self.request.arguments['contacted']:
                company.contact.contacted = True
        except:
            company.contact.contacted = False
        #------------------CEO INFO-------------------
        company.ceo.firstName = self.get_argument("ceoFirstName", None)
        company.ceo.lastName = self.get_argument("ceoLastName", None)
        #------------------COMPANY INFO-------------------
        #company.companyName = self.get_argument("companyName", None)
        #company.prettyName = re.sub(r'([^\s\w])+', '', company.companyName).replace(" ", "-").title()
        company.url = self.get_argument('url', None)
        company.city = self.get_argument('city', None)
        company.state = self.get_argument('state', None)
        company.zipCode = self.get_argument('zipCode', None)
        company.companyType = self.get_argument("companyType", None)
        if company.companyType == 'other': #if user entered custom option for Type
            company.companyType = self.get_argument('otherCompanyType', None)
        company.yearFounded = self.get_argument("yearFounded", 0)
        if  not company.yearFounded:
            company.yearFounded = 0
        company.fte = self.get_argument("fte", 0)
        if not company.fte:
            company.fte = 0
        company.companyCategory = self.get_argument("category", None)
        if company.companyCategory == "Other":
            company.companyCategory = self.get_argument("otherCategory", None)
        try: #try and get all checked items. 
            company.revenueSource = self.request.arguments['revenueSource']
        except: #if no checked items, then make it into an empty array (form validation should prevent this always)
            company.revenueSource = []
        if 'Other' in company.revenueSource: #if user entered a custom option for Revenue Source
            del company.revenueSource[company.revenueSource.index('Other')] #delete 'Other' from list
            if self.get_argument('otherRevenueSource', None):
                company.revenueSource.append(self.get_argument('otherRevenueSource', None)) #add custom option to list.
        company.description = self.get_argument('description', None)
        company.descriptionShort = self.get_argument('descriptionShort', None)
        company.financialInfo = self.get_argument('financialInfo', None)
        company.datasetWishList = self.get_argument('datasetWishList', None)
        company.sourceCount = self.get_argument('sourceCount', None) 
        company.dataComments = self.get_argument("dataComments", None)
        company.datasetComments = self.get_argument('datasetComments', None)
        company.submittedSurvey = True
        company.vettedByCompany = True
        company.lastUpdated = datetime.now()
        if company.display: #only if company is displayed
            self.application.stats.update_all_state_counts()
        company.save()
        #self.application.stats.update_all_state_counts()
        self.write('success')

#Editing section for Admins
class AdminEditCompanyHandler(BaseHandler):
    @tornado.web.addslash
    @tornado.web.authenticated
    def get(self, id):
        try: 
            company = models.Company2.objects.get(id=bson.objectid.ObjectId(id))
            page_heading = "Editing " + company.companyName + ' (Admin)'
            page_title = "Editing " + company.companyName + ' (Admin)'
        except Exception, e:
            logging.info('Error: ' + str(e))
            self.render("404.html",
                page_heading = '404 - Company Not Found',
                page_title = '404 - Not Found',
                error = "404 - Not Found",
                user=self.current_user,
                message=id)
        self.render("adminEditCompany.html",
            page_title = page_title,
            page_heading = page_heading,
            company = company,
            companyType = companyType,
            companyFunction = companyFunction,
            criticalDataTypes = criticalDataTypes,
            revenueSource = revenueSource,
            categories=categories,
            datatypes = datatypes,
            stateList = stateList,
            stateListAbbrev=stateListAbbrev,
            user=self.current_user,
            id = str(company.id)
        )

    @tornado.web.authenticated
    def post(self, id):
        #print all arguments to log:
        logging.info("Admin Editing Company")
        logging.info(self.request.arguments)
        #get the company you will be editing
        company = models.Company2.objects.get(id=bson.objectid.ObjectId(id))
        #------------------CONTACT INFO-------------------
        company.contact.firstName = self.get_argument("firstName", None)
        company.contact.lastName = self.get_argument("lastName", None)
        company.contact.title = self.get_argument("title", None)
        company.contact.org = self.get_argument("org", None)
        company.contact.email = self.get_argument("email", None)
        company.contact.phone = self.get_argument("phone", None)
        try: 
            if self.request.arguments['contacted']:
                company.contact.contacted = True
        except:
            company.contact.contacted = False
        #------------------CEO INFO-------------------
        company.ceo.firstName = self.get_argument("ceoFirstName", None)
        company.ceo.lastName = self.get_argument("ceoLastName", None)
        #------------------COMPANY INFO-------------------
        company.companyName = self.get_argument("companyName", None)
        company.prettyName = re.sub(r'([^\s\w])+', '', company.companyName).replace(" ", "-").title()
        company.url = self.get_argument('url', None)
        company.city = self.get_argument('city', None)
        company.state = self.get_argument('state', None)
        company.zipCode = self.get_argument('zipCode', None)
        company.companyType = self.get_argument("companyType", None)
        if company.companyType == 'other': #if user entered custom option for Type
            company.companyType = self.get_argument('otherCompanyType', None)
        company.yearFounded = self.get_argument("yearFounded", 0)
        if  not company.yearFounded:
            company.yearFounded = 0
        company.fte = self.get_argument("fte", 0)
        if not company.fte:
            company.fte = 0
        company.companyCategory = self.get_argument("category", None)
        if company.companyCategory == "Other":
            company.companyCategory = self.get_argument("otherCategory", None)
        try: #try and get all checked items. 
            company.revenueSource = self.request.arguments['revenueSource']
        except: #if no checked items, then make it into an empty array (form validation should prevent this always)
            company.revenueSource = []
        if 'Other' in company.revenueSource: #if user entered a custom option for Revenue Source
            del company.revenueSource[company.revenueSource.index('Other')] #delete 'Other' from list
            if self.get_argument('otherRevenueSource', None):
                company.revenueSource.append(self.get_argument('otherRevenueSource', None)) #add custom option to list.
        company.description = self.get_argument('description', None)
        company.descriptionShort = self.get_argument('descriptionShort', None)
        company.financialInfo = self.get_argument('financialInfo', None)
        company.datasetWishList = self.get_argument('datasetWishList', None)
        company.sourceCount = self.get_argument('sourceCount', None) 
        company.datasetComments = self.get_argument('datasetComments', None)
        if self.get_argument("submittedSurvey", None) == "submittedSurvey":
            company.submittedSurvey = True
        else:
            company.submittedSurvey = False
        if self.get_argument("vettedByCompany", None) == "vettedByCompany":
            company.vettedByCompany = False
        else:
            company.vettedByCompany = True
        if self.get_argument("vetted", None) == "vetted":
            company.vetted = True
        else: 
            company.vetted = False
        if self.get_argument("display", None) == "display":
            company.display = True
        else: 
            company.display = False
        if self.get_argument("locked", None) == "locked":
            company.locked = True
        else: 
            company.locked = False
        #company.lastUpdated = datetime.now()
        company.notes = self.get_argument("notes", None)
        company.save()
        self.application.stats.update_all_state_counts()
        self.write('success')
        #self.redirect('/thanks/')
        # if self.get_argument('submit', None) == 'Save and Submit':
        #     self.redirect('/')
        # if self.get_argument('submit', None) == 'Save And Continue Editing':
        #     self.redirect('/edit/'+id)

# class EditDataHandler(BaseHandler):
#     @tornado.web.addslash
#     @tornado.web.authenticated
#     def get(self, id):
#         #Are we adding a new dataset? or are we editing an existing dataset?
#         dataset = models.Dataset.objects.get(id=bson.objectid.ObjectId(id))
#         self.render("editData.html",
#             page_title = "Editing Dataset",
#             page_heading = "Edit Datasets",
#             datatypes = datatypes,
#             dataset = dataset,
#             user=self.current_user
#         )

#     @tornado.web.authenticated
#     def post(self, id):
#         #get company
#         #company = models.Company.objects.get(id=bson.objectid.ObjectId(id))
#         #get dataset
#         datasetID = self.get_argument('datasetID')
#         dataset = models.Dataset.objects.get(id=bson.objectid.ObjectId(id))
#         #get values
#         datasetName = self.get_argument('datasetName', None)
#         datasetURL = self.get_argument('datasetURL', None)
#         agency = self.get_argument('agency', None)
#         dataType = self.request.arguments['typeOfDataset']
#         #logging.info(dataType)
#         if 'Other' in dataType:
#             del dataType[dataType.index('Other')]
#             dataType.append(self.get_argument('otherTypeOfDataset', None))
#         rating = self.get_argument('rating', None)
#         reason = self.get_argument('reason', None)
#         #try: #to find existing dataset
#         #dataset = models.Dataset.objects.get(id=bson.objectid.ObjectId(id))
#         dataset.datasetName = datasetName
#         dataset.datasetURL = datasetURL
#         dataset.dataType = dataType
#         dataset.agency = agency
#         dataset.ratings[0].rating = rating
#         dataset.ratings[0].reason = reason
#         dataset.save()
#         self.write("success")

class DeleteDatasetHandler(BaseHandler):
    def post(self, id):
        dataset = models.Dataset.objects.get(id=bson.objectid.ObjectId(id))
        dataset.delete()
        self.write('success');



class DeleteCompanyHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, id):
        try:
            company = models.Company2.objects.get(id=bson.objectid.ObjectId(id)) 
        except:
            self.render(
                "404.html",
                page_title='404 - Open Data500',
                page_heading='Oh no...',
                error = "404 - Not Found"
            )
        # #-----REMOVE FROM ALL AGENCIES-----
        agencies = models.Agency.objects(usedBy__in=[str(company.id)])
        for a in agencies:
            #-----REMOVE DATASETS (AGENCY)-----
            temp = []
            temp_print = []
            for d in a.datasets:
                if d.usedBy != company:
                    temp.append(d)
                    temp_print.append(d.usedBy.companyName)
            a.datasets = temp
            logging.info(temp_print)
            #---REMOVE DATASETS (SUBAGENCY)---
            for s in a.subagencies:
                temp = []
                temp_print = []
                for d in s.datasets:
                    if company != d.usedBy:
                        temp.append(d)
                        temp_print.append(d.usedBy.companyName)
                s.datasets = temp
                logging.info(temp_print)
                #--REMOVE FROM SUBAGENCIES--
                if company in s.usedBy:
                    s.usedBy.remove(company)
            #-----REMOVE FROM AGENCY----
            a.usedBy.remove(company)
            a.usedBy_count = len(agency.usedBy)
            a.save()
        ##----------DELETE COMPANY--------
        company.delete()
        self.redirect('/admin/')

class DownloadHandler(BaseHandler):
    @tornado.web.addslash
    #@tornado.web.authenticated
    def get(self):
        self.render(
            "download.html",
            page_title='Download the Open Data 500',
            user=self.current_user,
            page_heading='Download the Open Data 500'
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

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(tornado.options.options.port)

    # start it up
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()









































