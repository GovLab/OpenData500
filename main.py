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

# import and define tornado-y things
from tornado.options import define
define("port", default=5000, help="run on the given port", type=int)

#Connect to mongo
connect('db', host=os.environ.get('MONGOLAB_URI'))

#Just some global varbs. 
favicon_path = '/static/img/favicon.ico'
companyType = ['Public', 'Private', 'Nonprofit']
companyFunction = ['Consumer Research and/or Marketing', 'Consumer Services', 'Data Management and Analysis', 'Financial/Investment Services', 'Information for Consumers']
criticalDataTypes = ['Federal Open Data', 'State Open Data', 'City/Local Open Data', 'Private/Proprietary Data Sources']
revenueSource = ['Advertising', 'Data Management and Analytic Services', 'Database Licensing', 'Lead Generation To Other Businesses', 'Philanthropy', 'Software Licensing', 'Subscriptions', 'User Fees for Web or Mobile Access']
sectors = ['Agriculture', 'Arts, Entertainment and Recreation' 'Crime', 'Education', 'Energy', 'Environmental', 'Finance', 'Geospatial data/mapping', 'Health and Healthcare', 'Housing/Real Estate', 'Manufacturing', 'Nutrition', 'Scientific Research', 'Social Assistance', 'Trade', 'Transportation', 'Telecom', 'Weather']
datatypes = ['Federal Open Data', 'State Open Data', 'City/Local Open Data']
categories = ['Business & Legal Services', 'Data/Technology', 'Education', 'Energy', 'Environment & Weather', 'Finance & Investment', 'Food & Agriculture', 'Geospatial/Mapping', 'Governance', 'Healthcare', 'Housing/Real Estate', 'Insurance', 'Lifestyle & Consumer', 'Research & Consulting', 'Scientific Research', 'Transportation']
states ={ "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas", "CA": "California", "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware", "DC": "District of Columbia", "FL": "Florida", "GA": "Georgia", "HI": "Hawaii", "ID": "Idaho", "IL": "Illinois", "IN": "Indiana", "IA": "Iowa", "KA": "Kansas", "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland", "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi", "MO": "Missouri", "MT": "Montana", "NE": "Nebraska", "NV": "Nevada", "NH": "New Hampshire", "NJ": "New Jersey", "NM": "New Mexico", "NY": "New York", "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio", "OK": "Oklahoma", "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina", "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah", "VT": "Vermont", "VA": "Virginia", "WA": "Washington", "WV": "West Virginia", "WI": "Wisconsin", "WY": "Wyoming", "PR": "Puerto Rico"}
stateListAbbrev = [ "", "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "DC", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KA", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY", "PR"]
stateList = ["(Select State)", "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "District of Columbia", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming", "Puerto Rico"]


# application settings and handle mapping info
class Application(tornado.web.Application):
    def __init__(self):
        self.stats = StatsGenerator()
        handlers = [
            (r'/(favicon.ico)', tornado.web.StaticFileHandler, {"path": ""}),
            (r"/", MainHandler),
            (r"/submitCompany/?", SubmitCompanyHandler),
            (r"/validate/?", ValidateHandler),
            (r"/edit/([a-zA-Z0-9]{24})/?", EditCompanyHandler),
            (r"/addData/([a-zA-Z0-9]{24})/?", SubmitDataHandler),
            #(r"/editData/([a-zA-Z0-9]{24})/?", EditDataHandler),
            (r"/view/([a-zA-Z0-9]{24})/?", ViewHandler),
            (r"/media/?", MediaHandler),
            (r"/delete/([a-zA-Z0-9]{24})/?", DeleteCompanyHandler),
            (r"/deleteData/([a-zA-Z0-9]{24})/?", DeleteDatasetHandler),
            #(r"/recommendCompany/?", RecommendCompanyHandler),
            (r"/admin/?", AdminHandler),
            (r"/admin/edit/([a-zA-Z0-9]{24})/?", AdminEditCompanyHandler),
            (r"/about/?", AboutHandler),
            (r"/resources/?", ResourcesHandler),
            #(r"/generateFiles/?", GenerateFilesHandler),
            (r"/download/?", DownloadHandler),
            (r'/download/(.*)/?',tornado.web.StaticFileHandler, {'path':os.path.join(os.path.dirname(__file__), 'static')}),
            #(r"/upload50/?", Upload50Handler),
            #(r"/upload500/?", Upload500Handler),
            #(r"/uploadAll/?", LoadEverythingNewHandler),
            #(r"/uploadAgencies/?", UploadAgencies),
            (r"/candidates/?", CandidateHandler),
            (r"/preview/?", PreviewHandler),
            (r'/thanks/?', ThanksHandler),
            (r'/login/?', LoginHandler),
            (r'/logout/?', LogoutHandler),
            (r'/register/?', RegisterHandler),
            #(r'/dump/?', EverythingHandler),
            (r"/([^/]+)/?", CompanyHandler)
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            ui_modules={"Company": CompanyModule},
            debug=True,
            cookie_secret=os.environ.get('COOKIE_SECRET'),
            xsrf_cookies=True,
            login_url="/login"
        )
        tornado.web.Application.__init__(self, handlers, **settings)

class StatsGenerator(object):
    def get_total_companies(self):
        return models.Stats.objects().first().totalCompanies
    
    def get_total_companies_web(self):
        return models.Stats.objects().first().totalCompaniesWeb
    
    def get_total_companies_surveys(self):
        return models.Stats.objects().first().totalCompaniesSurvey

    def update_totals_companies(self):
        s = models.Stats.objects().first()
        s.totalCompanies = models.Company2.objects().count()
        s.totalCompaniesWeb = models.Company2.objects(submittedThroughWebsite = True).count()
        s.totalCompaniesSurvey = models.Company2.objects(submittedSurvey = True).count()
    
    def increase_individual_state_count(self, state):
        stats = models.Stats.object().first()
        for s in stats.states:
            if s.name == state:
                s.count = s.count + 1
        stats.save()

    def update_all_state_counts(self):
        stats = models.Stats.objects().first()
        companies  = models.Company2.objects(display=True)
        stateCount = []
        for c in companies:
            stateCount.append(c.state)
        stats.states = []
        for i in range(1, 53):
            s = models.States(
                name = stateList[i],
                abbrev = stateListAbbrev[i],
                count = stateCount.count(stateListAbbrev[i]))
            stats.states.append(s)
        stats.save()

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
        self.render("media.html")

class ThanksHandler(BaseHandler): 
    @tornado.web.addslash
    def get(self):
        self.render(
            "thankyou.html", 
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
            page_heading=company.companyName,
            company = company,
        )
        except Exception, e:
            logging.info("Company: " + companyName + ": " + str(e)) 
            self.render(
                "404.html",
                page_title='404 - Open Data500',
                page_heading='Hmm...',
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
        )

class CandidateHandler(BaseHandler):
    @tornado.web.addslash
    #@tornado.web.authenticated
    def get(self):
        companies = models.Company2.objects(display=True).order_by('prettyName')
        stats = models.Stats.objects().first()
        self.render(
            "candidates.html",
            page_title='Open Data 500',
            page_heading='Candidates for the OD500',
            companies = companies,
            stats = stats,
            #recentlySubmitted=recentlySubmitted,
            states=states,
            categories = categories
            #stateInfo=stateInfo
        )

class AboutHandler(BaseHandler):
    @tornado.web.addslash
    #@tornado.web.authenticated
    def get(self):
        self.render(
            "about.html",
            page_title='About the OpenData500',
            page_heading='About the OpenData 500'
        )

class ResourcesHandler(BaseHandler):
    @tornado.web.addslash
    #@tornado.web.authenticated
    def get(self):
        self.render(
            "resources.html",
            page_title='Open Data Resources',
            page_heading='Open Data Resources'
        )

class AdminHandler(BaseHandler):
    @tornado.web.addslash
    @tornado.web.authenticated
    def get(self):
        # surveyNotIn50 = models.Company.objects(Q(preview50=False) & Q(candidate500=True) & Q(submittedSurvey=True)).order_by('prettyName') #Not make distinction between preview 50 and submitted
        # preview50 = models.Company.objects(Q(preview50=True) & Q(candidate500=True) & Q(submittedSurvey=True)).order_by('prettyName')
        surveySubmitted = models.Company2.objects(Q(submittedSurvey=True) & Q(display=True) & Q(vetted=True) & Q(vettedByCompany=True) & Q(submittedThroughWebsite=False)).order_by('prettyName')
        sendSurveys = models.Company2.objects(Q(vetted=False) & Q(vettedByCompany=False)).order_by('prettyName')
        needVetting = models.Company2.objects(Q(submittedSurvey=True) & Q(vetted=False) & Q(vettedByCompany=True)).order_by('ts')
        # candidate500 = models.Company.objects(Q(preview50=False) & Q(candidate500=True) & Q(submittedSurvey=False)).order_by('prettyName')
        # recentlySubmitted = models.Company.objects(Q(preview50=False) & Q(candidate500=False) & Q(submittedSurvey=True)).order_by('ts')
        #recentlySubmitted = models.Company2.objects(Q(submittedThroughWebsite=True) & Q(vettedByCompany=True) & Q(display=False) & Q(vetted=False) & Q(submittedSurvey=True)).order_by('ts')
        self.render(
            "admin.html",
            page_title='OpenData500',
            page_heading='Welcome to the OpenData 500',
            surveySubmitted = surveySubmitted,
            #recentlySubmitted=recentlySubmitted,
            needVetting = needVetting,
            sendSurveys = sendSurveys
        )

class ValidateHandler(BaseHandler):
    def post(self):
        #check if companyName exists:
        companyName = self.get_argument("companyName", None)
        try: 
            c = models.Company2.objects.get(companyName=companyName)
            self.write('{ "error": "This company has already been submitted. Email opendata500@thegovlab.org for questions." }')
        except:
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
            stateListAbbrev=stateListAbbrev
        )

    #@tornado.web.authenticated
    def post(self):
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
        if not zipCode:
            zipCode = 0
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
            display = False, 
            submittedSurvey = True,
            vetted = False, 
            vettedByCompany = True,
            submittedThroughWebsite = True
        )
        company.save()
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
            company = company
        )

    #@tornado.web.authenticated
    def post(self, id):
        try:
            company = models.Company2.objects.get(id=bson.objectid.ObjectId(id))
        except:
            self.set_status(400)
        agencyName = self.get_argument("agency", None)
        subagencyName = self.get_argument("subagency", None)
        action = self.get_argument("action", None)
        #------------------------------------ADDING AGENCY/SUBAGENCY------------------------
        if action == "add agency":
            #Existing AGENCY
            try:
                agency = models.Agency.objects.get(name=agencyName)
            except:
                self.set_status(400)
            for s in agency.subagencies:
                if s.name == subagencyName:
                    if company not in s.usedBy: #only add if it's not already there.
                        s.usedBy.append(company)
            agency.save()
            if company not in agency.usedBy: #only add if it's not already there.
                logging.info(agencyName + " is used by" + company.companyName)
                agency.usedBy.append(company)
                agency.save()
            if agency not in company.agencies: #only add if it's not already there.
                logging.info(company.companyName + " is used by" + agencyName)
                company.agencies.append(agency)
                company.save()
            self.write("success")
        #------------------------------------DELETING AGENCY/SUBAGENCY------------------------
        if action == "delete agency":
            try: 
                agency = models.Agency.objects.get(name=agencyName)
            except:
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
                        logging.info(temp)
                #remove company from specific subagency
                for s in agency.subagencies:
                    if company in s.usedBy and s.name == subagencyName:
                        s.usedBy.remove(company)
            agency.save()
            company.save()
            self.write("deleted")
        #------------------------------------ADDING DATASET------------------------
        if action == "add dataset":
            try:
                agency = models.Agency.objects.get(name=agencyName)
            except:
                self.set_status(400)
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
                message=id)
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
            id = str(company.id)
        )

    def post(self, id):
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
        try: 
            company.zipCode = int(self.get_argument('zipCode', None))
        except:
            company.zipCode = 0
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
        company.submittedSurvey = True
        company.vettedByCompany = True
        company.save()
        self.write('success')
        #self.redirect('/thanks/')
        # if self.get_argument('submit', None) == 'Save and Submit':
        #     self.redirect('/')
        # if self.get_argument('submit', None) == 'Save And Continue Editing':
        #     self.redirect('/edit/'+id)

#Editing section for Admins
class AdminEditCompanyHandler(BaseHandler):
    @tornado.web.addslash
    @tornado.web.authenticated
    def get(self, id):
        company = models.Company2.objects.get(id=bson.objectid.ObjectId(id))
        page_heading = "Editing " + company.companyName + ' (Admin)'
        page_title = "Editing " + company.companyName + ' (Admin)'
        if company is None:
            self.render("404.html", message=id)
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
            id = str(company.id)
        )

    @tornado.web.authenticated
    def post(self, id):
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
        try: 
            company.zipCode = int(self.get_argument('zipCode', None))
        except:
            company.zipCode = 0
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

        company.save()
        self.write('success')
        #self.redirect('/thanks/')
        # if self.get_argument('submit', None) == 'Save and Submit':
        #     self.redirect('/')
        # if self.get_argument('submit', None) == 'Save And Continue Editing':
        #     self.redirect('/edit/'+id)

class EditDataHandler(BaseHandler):
    @tornado.web.addslash
    @tornado.web.authenticated
    def get(self, id):
        #Are we adding a new dataset? or are we editing an existing dataset?
        dataset = models.Dataset.objects.get(id=bson.objectid.ObjectId(id))
        self.render("editData.html",
            page_title = "Editing Dataset",
            page_heading = "Edit Datasets",
            datatypes = datatypes,
            dataset = dataset
        )

    @tornado.web.authenticated
    def post(self, id):
        #get company
        #company = models.Company.objects.get(id=bson.objectid.ObjectId(id))
        #get dataset
        datasetID = self.get_argument('datasetID')
        dataset = models.Dataset.objects.get(id=bson.objectid.ObjectId(id))
        #get values
        datasetName = self.get_argument('datasetName', None)
        datasetURL = self.get_argument('datasetURL', None)
        agency = self.get_argument('agency', None)
        dataType = self.request.arguments['typeOfDataset']
        #logging.info(dataType)
        if 'Other' in dataType:
            del dataType[dataType.index('Other')]
            dataType.append(self.get_argument('otherTypeOfDataset', None))
        rating = self.get_argument('rating', None)
        reason = self.get_argument('reason', None)
        #try: #to find existing dataset
        #dataset = models.Dataset.objects.get(id=bson.objectid.ObjectId(id))
        dataset.datasetName = datasetName
        dataset.datasetURL = datasetURL
        dataset.dataType = dataType
        dataset.agency = agency
        dataset.ratings[0].rating = rating
        dataset.ratings[0].reason = reason
        dataset.save()
        self.write("success")

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
            )
        #-----REMOVE FROM ALL AGENCIES-----
        agencies = models.Agency.objects(usedBy__in=[str(company.id)])
        for a in agencies:
            #-----REMOVE DATASETS (AGENCY)-----
            temp = []
            for d in a.datasets:
                if d.usedBy != company:
                    temp.append(d)
            a.datasets = temp
            #---REMOVE DATASETS (SUBAGENCY)---
            for s in a.subagencies:
                temp = []
                for d in s.datasets:
                    if company != d.usedBy:
                        temp.append(d)
                s.datasets = temp
                #--REMOVE FROM SUBAGENCIES--
                if company in s.usedBy:
                    s.usedBy.remove(company)
            #-----REMOVE FROM AGENCY----
            a.usedBy.remove(company)
            a.save()
        ##----------DELETE COMPANY--------
        company.delete()
        self.redirect('/admin/')


class ViewHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, id):
        c = models.Company.objects.get(id=bson.objectid.ObjectId(id))
        obj = {
            "_id": {
                "$oid": str(c.id)
            },
            "companyName": c.companyName,
            "url": c.url,
            "submitter": {
                "firstName": c.submitter.firstName,
                "lastName": c.submitter.lastName,
                "personType": c.submitter.personType,
                "email": c.submitter.email,
                "title": c.submitter.title,
                "phone": c.submitter.phone,
                "org": c.submitter.org,
                "otherInfo": c.submitter.otherInfo,
                "contacted": c.submitter.contacted,
                "conferenceRec": c.submitter.conferenceRec
            },
            "contact": {
                "firstName": c.contact.firstName,
                "lastName": c.contact.lastName,
                "email": c.contact.email,
                "type": c.contact.personType
            },
            "reasonForRecommending": c.reasonForRecommending,
            "vetted": c.vetted,
            "ts": str(c.ts),
        }
        self.write(json_encode(obj))

class DownloadHandler(BaseHandler):
    @tornado.web.addslash
    #@tornado.web.authenticated
    def get(self):
        self.render(
            "download.html",
            page_title='Download Data',
            page_heading='Download Data',
        )

class LoadEverythingNewHandler(BaseHandler):
    def get(self):
        file = open("AllCompanies.json", "r")
        companies = []
        for line in file:
            companies.append(json.loads(line))
        companies = companies[0]
        for c in companies:
            contact = models.Person2(
                firstName = c['contact']['firstName'],
                lastName = c['contact']['lastName'],
                title = c['contact']['title'],
                email = c['contact']['email'],
                phone = c['contact']['phone'],
                org = c['contact']['org'],
                contacted = c['contact']['contacted'],
            )
            ceo = models.Person2(
                firstName = c['ceo']['firstName'],
                lastName = c['ceo']['lastName']
            )
            company = models.Company2(
                    companyName = c['companyName'],
                    prettyName = c['prettyName'],
                    url = c['url'],
                    contact = contact,
                    ceo = ceo,
                    yearFounded = c['yearFounded'],
                    previousName = c['previousName'],
                    city = c['city'],
                    state = c['state'],
                    zipCode = c['zipCode'],
                    fte = c['fte'],
                    companyType = c['companyType'],
                    companyCategory = c['companyCategory'],
                    revenueSource = c['revenueSource'].split(','),
                    description = c['descriptionLong'],
                    descriptionShort = c['descriptionShort'],
                    financialInfo = c['financialInfo'],
                    datasetWishList = c['contact']['datasetWishList'],
                    confidentiality =c['confidentiality'],
                    ts = json.loads(c['ts'], object_hook=json_util.object_hook),
                    display = c['display'],
                    submittedSurvey = c['submittedSurvey'],
                    vetted = c['vetted'],
                    vettedByCompany = c['vettedByCompany'],
                    submittedThroughWebsite = c['submittedThroughWebsite'],
                    agencies = []
                )
            company.save()
            try:
                for d in c['datasets']:
                    dataset = models.Dataset2(
                            datasetName = d['datasetName'],
                            datasetURL = d['datasetURL'],
                            rating = d['ratings']['rating'],
                            reason = d['ratings']['reason'],
                            usedBy = str(company.id)
                        )
                    agency = models.Agency(
                            name = d['agency'],
                            dataType = ','.join(d['dataType']),
                            ts = json.loads(d['ts'], object_hook=json_util.object_hook),
                            datasets = []
                        )
                    agency.datasets.append(dataset)
                    agency.save()
                    company.agencies.append(agency)
                    company.save()
            except:
                continue


class EverythingHandler(BaseHandler):
    @tornado.web.addslash
    @tornado.web.authenticated
    def get(self):
        companies = models.Company.objects()
        companyList = []
        for c in companies:
            company = {
                "companyName": c.companyName,
                "prettyName": c.prettyName,
                "url": c.url,
                "yearFounded": c.yearFounded,
                "previousName": c.previousName,
                "city": c.city,
                "state": c.state,
                "zipCode": c.zipCode,
                "fte": c.fte,
                "companyType": c.companyType,
                "companyCategory": c.companyCategory,
                "companyFunction": c.companyFunction,
                "criticalDataTypes": ','.join(c.criticalDataTypes),
                "revenueSource": ','.join(c.revenueSource),
                "sector": ','.join(c.sector),
                "descriptionLong": c.descriptionLong,
                "descriptionShort": c.descriptionShort,
                "socialImpact": c.socialImpact,
                "financialInfo": c.financialInfo,
                "confidentiality": c.confidentiality,
                #"contact": c.contact,
                #"recommendedBy": c.recommendedBy,
                "recommended": c.recommended,
                "reasonForRecommending": c.reasonForRecommending,
                #"datasets": c.datasets,
                "ts": json.dumps(c.ts, default=json_util.default),
                "preview50": c.preview50,
                "display": c.display,
                "submittedSurvey": c.submittedSurvey,
                "vetted": c.vetted,
                "vettedByCompany": c.vettedByCompany,
                "submittedThroughWebsite": c.submittedThroughWebsite
            }
            if c.contact:
                company['contact'] = {
                    "firstName": c.contact.firstName,
                    "lastName": c.contact.lastName,
                    "title": c.contact.title,
                    "personType": c.contact.personType,
                    "email": c.contact.email,
                    "phone": c.contact.phone,
                    "org": c.contact.org,
                    "contacted": c.contact.contacted,
                    "otherInfo": ','.join(c.contact.otherInfo),
                    "datasetWishList": c.contact.datasetWishList,
                    "companyRec": c.contact.companyRec,
                    "conferenceRec": c.contact.conferenceRec,
                    #"submittedCompany": c.contact.submittedCompany.id,
                    #"submittedDatasets": c.contact.submittedDatasets
                }
                if c.contact.submittedCompany:
                    company['contact']['submittedCompany'] = str(c.contact.submittedCompany.id)
                if c.contact.submittedDatasets:
                    company['contact']['submittedDatasets'] = []
                    for d in c.contact.submittedDatasets:
                        company['contact']['submittedDatasets'].append(str(d.id))
            if c.ceo:
                company['ceo'] = {
                    "firstName": c.ceo.firstName,
                    "lastName": c.ceo.lastName,
                    "email": c.ceo.email
                }
            if c.datasets:
                company['datasets'] = []
                for d in c.datasets:
                    dataset = {
                        "ts": json.dumps(d.ts, default=json_util.default),
                        "datasetName": d.datasetName,
                        "datasetURL": d.datasetURL,
                        "agency": d.agency,
                        "ratings": {
                            "rating": d.ratings[0].rating,
                            "reason": d.ratings[0].reason
                        },
                        "dataType": d.dataType,
                        "usedBy": str(d.usedBy[0].id)
                    }
                    company['datasets'].append(dataset)
            companyList.append(company)
        with open(os.path.join(os.path.dirname(__file__), 'static') + '/AllCompanies.json', 'w') as outfile:
            json.dump(companyList, outfile)

# class UploadAgencies(BaseHandler):
#     @tornado.web.addslash
#     @tornado.web.authenticated
#     def get(self):
#         with open('agenciesFormatted.csv', 'rb') as csvfile:
#             csvreader = csv.reader(csvfile, delimiter=',')
#             previousAgency = ''
#             a = models.Agency()
#             for row in csvreader:
#                 if row[0] != 'agency':
#                     try: #check if Agency exists
#                         a = models.Agency.objects.get(name=row[0])
#                     except: #make a new one.
#                         a = models.Agency(
#                             name = row[0],
#                             abbrev = row[1],
#                             prettyName = row[6],
#                             url = row[8],
#                             dataType = row[9],
#                             source = "dataGov",
#                             subagencies = [],
#                             usedBy = [],
#                             datasets = []
#                         )
#                         a.save()
#                     if row[3]: #if there is a subagency
#                         s = models.Subagency(
#                             name = row[3],
#                             abbrev = row[4],
#                             url = row[8],
#                             usedBy = [],
#                             datasets = []
#                         )
#                         a.subagencies.append(s)
#                         a.save()

        

class GenerateFilesHandler(BaseHandler):
    @tornado.web.addslash
    @tornado.web.authenticated
    def get(self):
        #Get published companies, turn each one into an array and put into CSV file
        companies = models.Company.objects()
        #make a csv for states info
        statesCount = []
        for c in companies:
            statesCount.append(c.state)
        count = [(i, statesCount.count(i)) for i in set(statesCount)]
        csvwriter = csv.writer(open(os.path.join(os.path.dirname(__file__), 'static') + "/states.csv", "w"))
        csvwriter.writerow(['abbrev','state','value'])
        for s in states:
            abbrev = s
            stateName = states[s]
            value = 0
            for c in count:
                if c[0] == abbrev:
                    value = c[1]
            newrow = [abbrev, stateName, value]
            for i in range(len(newrow)):  # For every value in our newrow
                    if hasattr(newrow[i], 'encode'):
                        newrow[i] = newrow[i].encode('utf8')
            csvwriter.writerow(newrow)
        #CSV of List of 50
        companies = models.Company.objects(Q(vetted=True) & Q(vettedByCompany=True))
        csvwriter = csv.writer(open(os.path.join(os.path.dirname(__file__), 'static') + "/Preview50_Companies.csv", "w"))
        csvwriter.writerow([
            'CompanyName',
            'URL',
            'city',
            'STATE',
            'abbrev',
            'zipCode',
            'ceoFirstName',
            'ceoLastName',
            'companyPreviousName',
            'yearFounded',
            'FTE',
            'companyType',
            'companyCategory',
            'companyFunction',
            'sectors',
            'revenueSource',
            'descriptionLong',
            'descriptionShort',
            'socialImpact',
            'financialInfo',
            'criticalDataTypes',
            'datasetName',
            'datasetURL',
            'agencyOrDatasetSource',
            'DATASETS'
            ])
        logging.info(len(companies))
        for c in companies:
            if len(c.datasets):
                try: 
                    state = states[str(c.state).replace(" ","")] #I think this is actually the abbreviation
                except: 
                    state = ''
                for d in c.datasets:
                    newrow = [
                        c.companyName,
                        c.url,
                        c.city,
                        state,
                        c.state,
                        c.zipCode,
                        c.ceo.firstName,
                        c.ceo.lastName,
                        c.previousName,
                        c.yearFounded,
                        c.fte,
                        c.companyType,
                        c.companyCategory,
                        c.companyFunction,
                        ', '.join(c.sector),
                        ', '.join(c.revenueSource),
                        c.descriptionLong,
                        c.descriptionShort,
                        c.socialImpact,
                        c.financialInfo,
                        ', '.join(c.criticalDataTypes),
                        d.datasetName,
                        d.datasetURL,
                        d.agency,
                        len(c.datasets)
                    ]
                    for i in range(len(newrow)):  # For every value in our newrow
                        if hasattr(newrow[i], 'encode'):
                            newrow[i] = newrow[i].encode('utf8')
                    csvwriter.writerow(newrow)
            else: 
                try: 
                    stateAbbrev = states[str(c.state).replace(" ","")] #This might the full name, and not the abbrev.
                except: 
                    stateAbbrev = ''
                newrow = [
                        c.companyName,
                        c.url,
                        c.city,
                        stateAbbrev,
                        c.state,
                        c.zipCode,
                        c.ceo.firstName,
                        c.ceo.lastName,
                        c.previousName,
                        c.yearFounded,
                        c.fte,
                        c.companyType,
                        c.companyCategory,
                        c.companyFunction,
                        ', '.join(c.sector),
                        ', '.join(c.revenueSource),
                        c.descriptionLong,
                        c.descriptionShort,
                        c.socialImpact,
                        c.financialInfo,
                        ', '.join(c.criticalDataTypes),
                        '',
                        '',
                        '',
                        len(c.datasets)
                    ]
                for i in range(len(newrow)):  # For every value in our newrow
                    if hasattr(newrow[i], 'encode'):
                        newrow[i] = newrow[i].encode('utf8')
                csvwriter.writerow(newrow)
        #Do that shit again for the 500. 
        companies = models.Company.objects()
        csvwriter = csv.writer(open(os.path.join(os.path.dirname(__file__), 'static') + "/500_Companies.csv", "w"))
        csvwriter.writerow([
            'CompanyName',
            'URL',
            'city',
            'STATE',
            'abbrev',
            'companyCategory',
            'descriptionShort',
            ])
        for c in companies: 
            try: 
                stateAbbrev = states[str(c.state).replace(" ","")] #This might the full name, and not the abbrev.
            except: 
                stateAbbrev = ''
            newrow = [
            c.companyName,
            c.url,
            c.city,
            stateAbbrev,
            c.state,
            c.companyCategory,
            c.descriptionShort
            ]
            for i in range(len(newrow)):  # For every value in our newrow
                if hasattr(newrow[i], 'encode'):
                    newrow[i] = newrow[i].encode('utf8')
            csvwriter.writerow(newrow)
        #Get companies, turn into objects, and then dump into JSON File
        companies = models.Company.objects(Q(vetted=True) & Q(vettedByCompany=True))
        companiesJSON = []
        for c in companies:
            datasetIDs = []
            for d in c.datasets:
                i = str(d.id)
                j, k, l, m = i[:len(i)/4], i[len(i)/4:2*len(i)/4], i[2*len(i)/4:3*len(i)/4], i[3*len(i)/4:]
                datasetIDs.append(l + m + k + j)
            i = str(c.id)
            j, k, l, m = i[:len(i)/4], i[len(i)/4:2*len(i)/4], i[2*len(i)/4:3*len(i)/4], i[3*len(i)/4:]
            companyID = l + m + k + j
            company = {
                "companyID": companyID,
                "companyName": c.companyName,
                "url": c.url,
                "city": c.city,
                "state": c.state,
                "zipCode": c.zipCode,
                "ceoFirstName": c.ceo.firstName,
                "ceoLastName": c.ceo.lastName,
                "previousName": c.previousName,
                "yearFounded": c.yearFounded,
                "fte": c.fte,
                "companyType": c.companyType,
                "companyCategory": c.companyCategory,
                "companyFunction": c.companyFunction,
                "sector": c.sector,
                "revenueSource": c.revenueSource,
                "descriptionLong": c.descriptionLong,
                "descriptionShort": c.descriptionShort,
                "socialImpact": c.socialImpact,
                "socialInfo": c.financialInfo,
                "criticalDataTypes": c.criticalDataTypes,
                "datasets": datasetIDs
            }
            companiesJSON.append(company)
        with open(os.path.join(os.path.dirname(__file__), 'static') + '/OD500_Companies.json', 'w') as outfile:
            json.dump(companiesJSON, outfile)
        #Get Datasets, turn into objects, and then dump into JSON file
        datasets = models.Dataset.objects()
        datasetsJSON = []
        for d in datasets:
            companyIDs = []
            for c in d.usedBy:
                i = str(c.id)
                j, k, l, m = i[:len(i)/4], i[len(i)/4:2*len(i)/4], i[2*len(i)/4:3*len(i)/4], i[3*len(i)/4:]
                companyIDs.append(l + m + k + j)
            i = str(d.id)
            j, k, l, m = i[:len(i)/4], i[len(i)/4:2*len(i)/4], i[2*len(i)/4:3*len(i)/4], i[3*len(i)/4:]
            datasetID = l + m + k + j
            dataset = {
                "datasetID": datasetID,
                "datasetName": d.datasetName,
                "datasetURL": d.datasetURL,
                "source": d.agency,
                "usedByCompany": companyIDs
            }
            datasetsJSON.append(dataset)
        with open(os.path.join(os.path.dirname(__file__), 'static') + '/OD500_Datasets.json', 'w') as outfile:
            json.dump(datasetsJSON, outfile)
        self.redirect('/admin/')


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









































