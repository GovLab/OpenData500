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
companyType = ['Public', 'Private', 'Nonprofit']
companyFunction = ['Consumer Research and/or Marketing', 'Consumer Services', 'Data Management and Analysis', 'Financial/Investment Services', 'Information for Consumers']
criticalDataTypes = ['Federal Open Data', 'State Open Data', 'City/Local Open Data', 'Private/Proprietary Data Sources']
revenueSource = ['Advertising', 'Data Management and Analytic Services', 'Database Licensing', 'Lead Generation To Other Businesses', 'Philanthropy', 'Software Licensing', 'Subscriptions', 'User Fees for Web or Mobile Access']
sectors = ['Agriculture', 'Arts, Entertainment and Recreation' 'Crime', 'Education', 'Energy', 'Environmental', 'Finance', 'Geospatial data/mapping', 'Health and Healthcare', 'Housing/Real Estate', 'Manufacturing', 'Nutrition', 'Scientific Research', 'Social Assistance', 'Trade', 'Transportation', 'Telecom', 'Weather']
datatypes = ['Federal Open Data', 'State Open Data', 'City/Local Open Data']
categories = ['Business & Legal Services', 'Data/Technology', 'Education', 'Energy', 'Environment & Weather', 'Finance & Investment', 'Food & Agriculture', 'Geospatial/Mapping', 'Governance', 'Healthcare', 'Housing/Real Estate', 'Insurance', 'Lifestyle & Consumer', 'Research & Consulting', 'Scientific Research', 'Transportation']
states ={ "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas", "CA": "California", "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware", "DC": "District of Columbia", "FL": "Florida", "GA": "Georgia", "HI": "Hawaii", "ID": "Idaho", "IL": "Illinois", "IN": "Indiana", "IA": "Iowa", "KA": "Kansas", "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland", "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi", "MO": "Missouri", "MT": "Montana", "NE": "Nebraska", "NV": "Nevada", "NH": "New Hampshire", "NJ": "New Jersey", "NM": "New Mexico", "NY": "New York", "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio", "OK": "Oklahoma", "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina", "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah", "VT": "Vermont", "VA": "Virginia", "WA": "Washington", "WV": "West Virginia", "WI": "Wisconsin", "WY": "Wyoming", "PR": "Puerto Rico"}

# application settings and handle mapping info
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/submitCompany/?", SubmitCompanyHandler),
            (r"/edit/([a-zA-Z0-9]{24})/?", EditCompanyHandler),
            (r"/addData/([a-zA-Z0-9]{24})/?", SubmitDataHandler),
            (r"/editData/([a-zA-Z0-9]{24})/?", EditDataHandler),
            (r"/view/([a-zA-Z0-9]{24})/?", ViewHandler),
            (r"/delete/([a-zA-Z0-9]{24})/?", DeleteCompanyHandler),
            #(r"/recommendCompany/?", RecommendCompanyHandler),
            (r"/admin/?", AdminHandler),
            (r"/admin/edit/([a-zA-Z0-9]{24})/?", AdminEditCompanyHandler),
            (r"/about/?", AboutHandler),
            (r"/resources/?", ResourcesHandler),
            (r"/generateFiles/?", GenerateFilesHandler),
            (r"/download/?", DownloadHandler),
            (r'/download/(.*)/?',tornado.web.StaticFileHandler,{'path':os.path.join(os.path.dirname(__file__), 'static')}),
            #(r"/upload50/?", Upload50Handler),
            #(r"/upload500/?", Upload500Handler),
            (r"/candidates/?", CandidateHandler),
            (r"/preview/?", PreviewHandler),
            (r'/login/?', LoginHandler),
            (r'/logout/?', LogoutHandler),
            (r'/register/?', RegisterHandler),
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
    @tornado.web.authenticated
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
    @tornado.web.authenticated
    def get(self, companyName):
        try:
            company = models.Company.objects.get(prettyName=companyName)
        except: 
            self.render(
                "404.html",
                page_title='404 - Open Data500',
                page_heading='Oh no...',
            )
        logging.info(company.companyName)
        self.render(
            "company.html",
            page_title='Open Data500',
            page_heading=company.companyName,
            company = company,
        )

      
class PreviewHandler(BaseHandler):
    @tornado.web.addslash
    @tornado.web.authenticated
    def get(self):
        #companies = models.Company.objects()
        submittedCompanies = models.Company.objects(Q(vetted=True) & Q(vettedByCompany=True))
        self.render(
            "preview.html",
            page_title='Open Data500',
            page_heading='Preview of the Open Data 500',
            submittedCompanies = submittedCompanies,
        )

class CandidateHandler(BaseHandler):
    @tornado.web.addslash
    @tornado.web.authenticated
    def get(self):
        companies = models.Company.objects()
        stateInfo = []
        with open(os.path.join(os.path.dirname(__file__), 'static') + '/states.csv', 'rb') as csvfile:
            statereader = csv.reader(csvfile, delimiter=',')
            for row in statereader:
                if row[0] != 'abbrev':
                    stateInfo.append({
                        "abbrev": row[0],
                        "STATE": row[1],
                        "VALUE": row[2]
                        })
        self.render(
            "candidates.html",
            page_title='Open Data 500',
            page_heading='Candidates for the OD500',
            companies = companies,
            categories = categories,
            stateInfo=stateInfo
        )

class AboutHandler(BaseHandler):
    @tornado.web.addslash
    @tornado.web.authenticated
    def get(self):
        self.render(
            "about.html",
            page_title='About the OpenData500',
            page_heading='About the OpenData 500'
        )

class ResourcesHandler(BaseHandler):
    @tornado.web.addslash
    @tornado.web.authenticated
    def get(self):
        self.render(
            "resources.html",
            page_title='Open Data Resources',
            page_heading='Open Data Resources'
        )

class Upload50Handler(BaseHandler):
    @tornado.web.addslash
    @tornado.web.authenticated
    def get(self):
        # Preview Survey Companies
        companies = []
        with open('companies.csv', 'rb') as csvfile:
            companyreader = csv.reader(csvfile, delimiter=',')
            for row in companyreader:
                companies.append(row)
        previousName = ""
        id = ''
        for c in companies:
            companyName = c[0]
            if c[0] != 'companyName':
                if companyName != previousName: #New company
                    logging.info(companyName + " <-> " + previousName)
                    dateAdded = c[2]
                    firstName = c[3].lstrip()
                    lastName = c[4]
                    title = c[5]
                    email = c[6]
                    phone = c[7]
                    if c[8] == 'checked':
                        contacted = True
                    else: 
                        contacted = False
                    datasetWishList = c[37]
                    companyRec = c[39]
                    conferenceRec = c[40]
                    #otherInfo = c[]
                    #make contact
                    contact = models.Person(
                        firstName=firstName,
                        lastName=lastName,
                        title=title,
                        personType="Contact",
                        email=email,
                        phone=phone,
                        contacted=contacted,
                        org=companyName,
                        #otherInfo=otherInfo,
                        datasetWishList=datasetWishList,
                        companyRec=companyRec,
                        conferenceRec=conferenceRec,
                        )
                    contact.save()
                    ceoFirstName = c[12].lstrip()
                    ceoLastName = c[13]
                    ceoEmail = c[14]
                    if ceoEmail == email:
                        ceo = contact
                    else: 
                        ceo = models.Person(
                            firstName=ceoFirstName,
                            lastName=ceoLastName,
                            email=ceoEmail,
                            personType="CEO"
                            )
                        ceo.save()
                    prettyName = re.sub(r'([^\s\w])+', '', companyName).replace(" ", "-")
                    url = c[1]
                    city = c[9]
                    state = c[10]
                    try: 
                        zip = int(c[11])
                    except: 
                        zip = 99999
                    if c[15]:
                        yearFounded = c[15]
                    else: 
                        yearFounded = 0
                    previousName = c[16]
                    try: 
                        fte = int(c[17])
                    except: 
                        fte = None
                    companyType = c[18]
                    if c[19]:
                        companyTypeOther = c[19]
                        companyType = companyTypeOther
                    companyFunction = c[20]
                    if c[21]:
                        companyFunctionOther = c[21]
                        companyFunction = companyFunctionOther
                    criticalDataTypes = c[22].split(',')
                    if c[23]:
                        criticalDataTypesOther = c[23]
                        criticalDataTypes.append(criticalDataTypesOther)
                    revenueSource = c[24].split(',')
                    if c[25]:
                        revenueSourceOther = c[25]
                        revenueSource.append(revenueSourceOther)
                    sector = c[26].split(',')
                    if c[27]:
                        sectorOther = c[27]
                        sector.append(sectorOther)
                    companyCategory = c[41]
                    descriptionLong = c[28]
                    descriptionShort = c[29]
                    socialImpact = c[30]
                    financialInfo = c[31]
                    confidentiality = c[38]
                    if c[42] == 'Y':
                        vetted = True
                    else:
                        vetted = False
                    #Make new Company Object and save this stuff
                    company = models.Company(
                        companyName=companyName,
                        prettyName=prettyName,
                        url = url,
                        city=city,
                        state=state,
                        zipCode=zip,
                        yearFounded=yearFounded,
                        previousName=previousName,
                        fte=fte,
                        companyType=companyType,
                        companyFunction=companyFunction,
                        companyCategory=companyCategory,
                        criticalDataTypes=criticalDataTypes,
                        revenueSource=revenueSource,
                        sector=sector,
                        descriptionLong=descriptionLong,
                        descriptionShort=descriptionShort,
                        socialImpact=socialImpact,
                        financialInfo=financialInfo,
                        ceo=ceo,
                        contact=contact,
                        confidentiality = confidentiality,
                        vetted = vetted,
                        vettedByCompany = True
                        )
                    company.save()
                    company.contact.submittedCompany = company
                    #make new dataset object and append to company
                    datasetName = c[32]
                    datasetURL = c[33]
                    agency = c[34]
                    try: 
                        rating = int(c[35])
                    except:
                        rating = None
                    reason = c[36]
                    review = models.Rating(
                        rating=rating,
                        reason=reason,
                        author=contact
                        )
                    #make dataset
                    dataset = models.Dataset(
                        datasetName=datasetName,
                        datasetURL=datasetURL,
                        agency=agency
                        )
                    dataset.save()
                    dataset.ratings.append(review)
                    dataset.usedBy.append(company)
                    dataset.save()
                    company.datasets.append(dataset)
                    company.save()
                    #update previousName
                    id = company.id
                    previousName = companyName
                else: #dealing with same company, add rest of datasets
                    #get company
                    company = models.Company.objects.get(id=bson.objectid.ObjectId(id))
                    logging.info("repeat. Saving datasets to: " + company.companyName)
                    #skip all company info, get dataset info
                    datasetName = c[32]
                    datasetURL = c[33]
                    agency = c[34]
                    try: 
                        rating = int(c[35])
                    except:
                        rating = None
                    reason = c[36]
                    review = models.Rating(
                        rating=rating,
                        reason=reason,
                        author=company.contact
                        )
                    #create new dataset
                    dataset = models.Dataset(
                        datasetName=datasetName,
                        datasetURL=datasetURL,
                        agency=agency,
                        )
                    dataset.save()
                    dataset.ratings.append(review)
                    dataset.usedBy.append(company)
                    dataset.save()
                    #append dataset to company
                    company.contact.submittedDatasets.append(dataset)
                    company.datasets.append(dataset)
                    company.save()
                    #update PreviousName
                    previosName = companyName
        self.redirect('/admin/')

class Upload500Handler(BaseHandler):
    @tornado.web.addslash
    @tornado.web.authenticated
    def get(self):
        #Rest of 500
        companies = []
        with open('500companies.csv', 'rb') as csvfile:
            companyreader = csv.reader(csvfile, delimiter=',')
            for row in companyreader:
                companies.append(row)
        for c in companies:
            companyName = c[0]
            if c[43] != 'Y' and c[42] != 'Y' and c[0] != 'companyName':
                logging.info("Working on " + companyName)
                dateAdded = c[2]
                firstName = c[3].lstrip()
                lastName = c[4]
                title = c[5]
                email = c[6]
                phone = c[7]
                if c[8] == 'checked':
                    contacted = True
                else: 
                    contacted = False
                datasetWishList = c[37]
                companyRec = c[39]
                conferenceRec = c[40]
                #otherInfo = c[]
                #make contact
                contact = models.Person(
                    firstName=firstName,
                    lastName=lastName,
                    title=title,
                    personType="Contact",
                    email=email,
                    phone=phone,
                    contacted=contacted,
                    org=companyName,
                    #otherInfo=otherInfo,
                    datasetWishList=datasetWishList,
                    companyRec=companyRec,
                    conferenceRec=conferenceRec,
                    )
                contact.save()
                ceoFirstName = c[12].lstrip()
                ceoLastName = c[13]
                ceoEmail = c[14]
                if ceoEmail == email:
                    ceo = contact
                else: 
                    ceo = models.Person(
                        firstName=ceoFirstName,
                        lastName=ceoLastName,
                        email=ceoEmail,
                        personType="CEO"
                        )
                    ceo.save()
                prettyName = re.sub(r'([^\s\w])+', '', companyName).replace(" ", "-")
                url = c[1]
                city = c[9]
                state = c[10]
                try: 
                    zip = int(c[11])
                except: 
                    zip = 99999
                if c[15]:
                    yearFounded = c[15]
                else: 
                    yearFounded = 0
                previousName = c[16]
                try: 
                    fte = int(c[17])
                except: 
                    fte = None
                companyType = c[18]
                if c[19]:
                    companyTypeOther = c[19]
                    companyType = companyTypeOther
                companyFunction = c[20]
                if c[21]:
                    companyFunctionOther = c[21]
                    companyFunction = companyFunctionOther
                criticalDataTypes = c[22].split(',')
                if c[23]:
                    criticalDataTypesOther = c[23]
                    criticalDataTypes.append(criticalDataTypesOther)
                revenueSource = c[24].split(',')
                if c[25]:
                    revenueSourceOther = c[25]
                    revenueSource.append(revenueSourceOther)
                sector = c[26].split(',')
                if c[27]:
                    sectorOther = c[27]
                    sector.append(sectorOther)
                companyCategory = c[41]
                descriptionLong = c[28]
                descriptionShort = c[29]
                socialImpact = c[30]
                financialInfo = c[31]
                confidentiality = c[38]
                #Make new Company Object and save this stuff
                company = models.Company(
                    companyName=companyName,
                    prettyName=prettyName,
                    url = url,
                    city=city,
                    state=state,
                    zipCode=zip,
                    yearFounded=yearFounded,
                    previousName=previousName,
                    fte=fte,
                    companyType=companyType,
                    companyFunction=companyFunction,
                    companyCategory=companyCategory,
                    criticalDataTypes=criticalDataTypes,
                    revenueSource=revenueSource,
                    sector=sector,
                    descriptionLong=descriptionLong,
                    descriptionShort=descriptionShort,
                    socialImpact=socialImpact,
                    financialInfo=financialInfo,
                    ceo=ceo,
                    contact=contact,
                    confidentiality = confidentiality,
                    vetted = False,
                    vettedByCompany = False
                    )
                company.save()
                company.contact.submittedCompany = company
        self.redirect('/admin/')

class AdminHandler(BaseHandler):
    @tornado.web.addslash
    @tornado.web.authenticated
    def get(self):
        unvettedCompanies = models.Company.objects(Q(vetted=False) & Q(vettedByCompany=True))
        logging.info(len(unvettedCompanies))
        vettedCompanies = models.Company.objects(Q(vetted=True) & Q(vettedByCompany=True))
        recommendedCompanies = models.Company.objects(Q(vetted=False) & Q(recommended=True))
        unvettedByCompanies = models.Company.objects(Q(vetted=False) & Q(vettedByCompany=False))
        self.render(
            "admin.html",
            page_title='OpenData500',
            page_heading='Welcome to the OpenData 500',
            unvettedCompanies = unvettedCompanies,
            recommendedCompanies = recommendedCompanies,
            vettedCompanies = vettedCompanies,
            unvettedByCompanies = unvettedByCompanies
        )

class SubmitCompanyHandler(BaseHandler):
    @tornado.web.addslash
    @tornado.web.authenticated
    def get(self):
        self.render(
            "submitCompany.html",
            page_title = "Submit Your Company",
            page_heading = "Submit Your Company"
        )

    @tornado.web.authenticated
    def post(self):
        firstName = self.get_argument("firstName", None)
        lastName = self.get_argument("lastName", None)
        title = self.get_argument("title", None)
        #org = self.get_argument("org", None)
        url = self.get_argument('url', None)
        companyName = self.get_argument("companyName", None)
        prettyName = re.sub(r'([^\s\w])+', '', companyName).replace(" ", "-")
        email = self.get_argument("email", None)
        phone = self.get_argument("phone", None)
        city = self.get_argument("city", None)
        zipCode = self.get_argument("zipCode", None)
        if not zipCode:
            zipCode = 0
        ceoFirstName = self.get_argument("ceoFirstName", None)
        ceoLastName = self.get_argument("ceoLastName", None)
        ceoEmail = self.get_argument("ceoEmail", None)
        companyType = self.get_argument("companyType", None)
        try:
            if self.request.arguments['contacted']:
                contacted = True
        except:
            contacted = False
        if companyType == 'other':
            companyType = self.get_argument('otherCompanyType', None)
        yearFounded = self.get_argument("yearFounded", None)
        if not yearFounded:
            yearFounded = 9999
        fte = self.get_argument("fte", None).replace(",","")
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
        companyCategory = self.get_argument("category", None)
        if companyCategory == 'Other':
            companyCategory = self.get_argument('otherCategory', None)
        # try:
        #     sector = self.request.arguments['sector']
        # except:
        #     sector = []
        # if 'Other' in sector:
        #     del sector[sector.index('Other')]
        #     sector.append(self.get_argument('otherSector', None))
        descriptionLong = self.get_argument('descriptionLong', None)
        descriptionShort = self.get_argument('descriptionShort', None)
        socialImpact = self.get_argument('socialImpact', None)
        financialInfo = self.get_argument('financialInfo')
        datasetWishList = self.get_argument('datasetWishList', None)
        companyRec = self.get_argument('companyRec', None)
        conferenceRec = self.get_argument('conferenceRec', None)
        contact = models.Person(
            firstName = firstName,
            lastName = lastName,
            title = title,
            #org = org,
            email = email,
            phone = phone,
            contacted = contacted,
            personType = "Submitter",
            datasetWishList = datasetWishList,
            companyRec = companyRec,
            conferenceRec = conferenceRec
        )
        #if the ceo email and the contact email are the same, then we only save one person.
        if email == ceoEmail:
            ceo = contact
            ceo.personType = "CEO"
            ceo.save()
            contact.save()
        else:
            ceo = models.Person(
                firstName = ceoFirstName,
                lastName = ceoLastName,
                email = ceoEmail,
                personType = "CEO"
            )
            contact.save()
            ceo.save()
        company = models.Company(
            companyName = companyName,
            prettyName = prettyName,
            url = url,
            ceo = ceo,
            city = city,
            zipCode = zipCode,
            yearFounded = yearFounded,
            fte = fte,
            companyType = companyType,
            companyFunction = companyFunction,
            criticalDataTypes = criticalDataTypes,
            revenueSource = revenueSource,
            companyCategory = companyCategory,
            descriptionLong = descriptionLong,
            descriptionShort = descriptionShort,
            socialImpact = socialImpact,
            financialInfo = financialInfo,
            contact = contact,
            vetted = False,
            vettedByCompany = True,
            recommended = False #this was submitted not recommended. 
        )
        company.save()
        contact.submittedCompany = company
        contact.save()
        id = str(company.id)
        self.redirect("/addData/" + id)

class RecommendCompanyHandler(BaseHandler):
    @tornado.web.addslash
    @tornado.web.authenticated
    def get(self, id=None):
        try:
            recommenderId = models.Person.objects.get(id=bson.objectid.ObjectId(id))
        except:
            recommenderId = None
        self.render(
            "recommendCompany.html",
            page_title = "Recommend a Company",
            page_heading = "Recommend a Company",
            recommenderId = recommenderId
        )

    @tornado.web.authenticated
    def post(self): #A person has just recommended a company
        #Recommenders info:
        firstName = self.get_argument("firstName", None)
        lastName = self.get_argument("lastName", None)
        org = self.get_argument("org", None)
        email = self.get_argument("email", None)
        otherInfo = self.get_argument("otherInfo", None) #What else you got to say?
        #Check to see if Recommender exists already (via email or ID)
        try: 
            recommender = models.Person.objects.get(email=email) #if Recommender exists, update the info:
            recommender.firstName = firstName
            recommender.lastName = lastName
            recommender.org = org
            recommender.otherInfo.append(otherInfo)
            recommender.save()
        except: #not found by email, try by ID (If the user clicks on "Recommend another Company")
            try:
                recommenderId = self.get_argument('recommenderId', None)
                recommender = models.Person.objects.get(id=bson.objectid.ObjectId(recommenderId))
            except:
                recommender = None
        if not recommender: #If we don't have a recommender already, save a new one.
            recommender = models.Person(
                firstName = firstName, 
                lastName = lastName,
                org = org,
                email = email,
                personType = "Recommender"
            )
            recommender.otherInfo.append(otherInfo)
            recommender.save()
        #Company Info:
        companyName = self.get_argument("companyName", None)
        url = self.get_argument('url', None)
        reasonForRecommending = self.get_argument("reasonForRecommending", None)
        #Contact Info
        firstNameContact = self.get_argument("firstNameContact", None)
        lastNameContact = self.get_argument("lastNameContact", None)
        emailContact = self.get_argument("emailContact", None)
        #Save the contact
        if emailContact:
            contact = models.Person(
                firstName = firstNameContact,
                lastName = lastNameContact,
                email =emailContact,
                personType = "Contact",
                org = companyName
            )
            contact.save()
        else: 
            contact = None
        #Create new company and save the company Info
        company = models.Company(
            companyName = companyName,
            url = url,
            reasonForRecommending = reasonForRecommending,
            vetted = False,
            vettedByCompany = False,
            recommended = True
        )
        company.save()
        if contact:
            company.contact = contact
        recommender.submittedCompany = company
        recommender.save()
        company.recommendedBy = recommender
        company.save()
        #Add Another? Redirect to form
        if self.get_argument('submit', None) == 'Recommend Another Company':
            self.render(
                "recommendCompany.html", 
                page_title = "Recommend a Company",
                page_heading = "Recommend a Company",
                recommenderId = str(recommender.id)
            )
        #Done recommending? Redirect back home
        else: 
            self.redirect("/")


class SubmitDataHandler(BaseHandler):
    @tornado.web.addslash
    @tornado.web.authenticated
    def get(self, id):
        #Make not whether we are submitting a Co. and adding a dataset or editing a Co. and adding a dataset
        #get company
        company = models.Company.objects.get(id=bson.objectid.ObjectId(id))
        page_heading = "Enter Data Sets for " + company.companyName
        self.render("submitData.html",
            page_title = "Submit Data Sets For Company",
            page_heading = page_heading,
            id = id #Company id.
        )

    @tornado.web.authenticated
    def post(self, id):
        #get the company we are dealing with:
        id = self.get_argument('id', None)
        company = models.Company.objects.get(id=bson.objectid.ObjectId(id))
        #get dataset fields from form:
        datasetName = self.get_argument('datasetName', None)
        datasetURL = self.get_argument('datasetURL', None)
        agency = self.get_argument('agency', None)
        try: #get all entered dataTypes
            dataType = self.request.arguments['dataType']
        except: #if none, then make empty attay
            dataType = []
        if 'Other' in dataType: #if Other, add the other.
            del dataType[dataType.index('Other')]
            dataType.append(self.get_argument('otherDataType', None))
        ratingSubmitted = self.get_argument('rating', None)
        if not ratingSubmitted:
            ratingSubmitted = 9999
        reason = self.get_argument('reason', None)
        #The author of this dataset review is always the contact.
        author = company.contact
        #Can't check if dataset exists. If check by URL, if someone enters data.gov instead of specific URL, 
        #datasets might be different but same URL.
        #Just save them all.
        #Are we making a new one, or editing?
        dataset = models.Dataset(
            datasetName = datasetName,
            datasetURL = datasetURL,
            agency=agency,
            dataType = dataType,
        )
        #save the rating
        rating = models.Rating(
            author = author,
            rating =ratingSubmitted,
            reason = reason
        )
        #Save ratings, datasets, author, and company
        dataset.ratings.append(rating)
        dataset.usedBy.append(company)
        dataset.save()
        author.submittedDatasets.append(dataset)
        author.save()
        company.datasets.append(dataset)
        company.save()
        #If want to add another, redirect to form again. 
        if self.get_argument('submit', None) == 'Add Another':
            logging.info('adding another')
            self.redirect("/addData/" + id)
        if self.get_argument('submit', None) == 'Done': #else, you're done, go home.
            self.redirect("/")

class EditCompanyHandler(BaseHandler):
    @tornado.web.addslash
    @tornado.web.authenticated
    def get(self, id):
        try: 
            company = models.Company.objects.get(id=bson.objectid.ObjectId(id))
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
            sectors = sectors,
            datatypes = datatypes,
            action = 'editing',
            id = str(company.id)
        )

    @tornado.web.authenticated
    def post(self, id):
        #get the company you will be editing
        company = models.Company.objects.get(id=bson.objectid.ObjectId(id))
        #Submitter info
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
        company.contact.save()
        #CEO Info
        company.ceo.firstName = self.get_argument("ceoFirstName", None)
        company.ceo.lastName = self.get_argument("ceoLastName", None)
        company.ceo.email = self.get_argument("ceoEmail", None)
        company.ceo.save()
        #Company Info
        company.companyName = self.get_argument("companyName", None)
        company.prettyName = re.sub(r'([^\s\w])+', '', company.companyName).replace(" ", "-")
        url = self.get_argument('url', None)
        company.city = self.get_argument('city', None)
        company.zipCode = self.get_argument('zipCode', None)
        company.companyType = self.get_argument("companyType", None)
        if company.companyType == 'other': #if user entered custom option for Type
            company.companyType = self.get_argument('otherCompanyType', None)
        company.yearFounded = self.get_argument("yearFounded", 9999)
        company.fte = self.get_argument("fte", 0)
        company.companyFunction = self.get_argument("companyFunction", None)
        if company.companyFunction == 'other': #if user entered custom option for Function
            company.companyFunction = self.get_argument('otherCompanyFunction', None)
        try: #try and get all checked items. 
            company.criticalDataTypes = self.request.arguments['criticalDataTypes']
        except: #if no checked items, then make it into an empty array (form validation should prevent this always)
            company.criticalDataTypes = []
        if 'Other' in company.criticalDataTypes: #if user entered a custom option for Data Type
            del company.criticalDataTypes[company.criticalDataTypes.index('Other')] #delete 'Other' from list
            if self.get_argument('otherCriticalDataTypes', None):
                company.criticalDataTypes.append(self.get_argument('otherCriticalDataTypes', None)) #add custom option to list.
        try: #try and get all checked items. 
            company.revenueSource = self.request.arguments['revenueSource']
        except: #if no checked items, then make it into an empty array (form validation should prevent this always)
            company.revenueSource = []
        if 'Other' in company.revenueSource: #if user entered a custom option for Revenue Source
            del company.revenueSource[company.revenueSource.index('Other')] #delete 'Other' from list
            if self.get_argument('otherRevenueSource', None):
                company.revenueSource.append(self.get_argument('otherRevenueSource', None)) #add custom option to list.
        try: #try and get all checked items. 
            company.sector = self.request.arguments['sector']
        except: #if no checked items, then make it into an empty array (form validation should prevent this always)
            company.sector = []
        if 'Other' in company.sector: #if user entered a custom option for Sector
            del company.sector[company.sector.index('Other')] #delete 'Other' from list
            if self.get_argument('otherSector', None):
                company.sector.append(self.get_argument('otherSector', None)) #add custom option to list.
        company.descriptionLong = self.get_argument('descriptionLong', None)
        company.descriptionShort = self.get_argument('descriptionShort', None)
        company.socialImpact = self.get_argument('socialImpact', None)
        company.financialInfo = self.get_argument('financialInfo', None)
        if self.get_argument('vettedByCompany') == 'True':
            company.vettedByCompany = True
        elif self.get_argument('vettedByCompany') == 'False':
            company.vettedByCompany = False
        company.save()
        self.redirect('/')

#Editing section for Admins
class AdminEditCompanyHandler(BaseHandler):
    @tornado.web.addslash
    @tornado.web.authenticated
    def get(self, id):
        company = models.Company.objects.get(id=bson.objectid.ObjectId(id))
        page_heading = "Editing " + company.companyName
        page_title = "Editing " + company.companyName
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
            categories=categories
        )

    @tornado.web.authenticated
    def post(self, id):
        #get the company you will be editing
        company = models.Company.objects.get(id=bson.objectid.ObjectId(id))
        #Contact info
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
        company.contact.save()
        if company.ceo: #Is there a CEO?
            #CEO Info
            company.ceo.firstName = self.get_argument("ceoFirstName", None)
            company.ceo.lastName = self.get_argument("ceoLastName", None)
            company.ceo.email = self.get_argument("ceoEmail", None)
            company.ceo.save()
        else: #No previously recorded CEO, make a new one.
            ceo = models.Person(
                firstName = self.get_argument("ceoFirstName", None),
                lastName = self.get_argument("ceoLastName", None),
                email = self.get_argument("ceoEmail", None),
                org = self.get_argument("companyName", None),
                personType = "CEO"
            )
            ceo.save()
            company.ceo = ceo
            company.save()
        #Company Info
        companyName = self.get_argument("companyName", None)
        company.companyName = companyName
        company.prettyName = re.sub(r'([^\s\w])+', '', companyName).replace(" ", "-")
        url = self.get_argument('url', None)
        company.city = self.get_argument('city', None)
        company.zipCode = self.get_argument('zipCode', None)
        if not company.zipCode:
            company.zipCode = 0
        company.companyType = self.get_argument("companyType", None)
        if company.companyType == 'Other': #if user entered custom option for Type
            company.companyType = self.get_argument('otherCompanyType', None)
        company.yearFounded = self.get_argument("yearFounded", None)
        if not company.yearFounded: #Did not enter year?
            company.yearFounded = 0
        company.fte = self.get_argument("fte", 0)
        if not company.fte: #did not enter fte?
            company.fte = 0
        company.companyFunction = self.get_argument("companyFunction", None)
        if company.companyFunction == 'Other': #if user entered custom option for Function
            company.companyFunction = self.get_argument('otherCompanyFunction', None)
        try: #try and get all checked items. 
            company.criticalDataTypes = self.request.arguments['criticalDataTypes']
        except: #if no checked items, then make it into an empty array (form validation should prevent this always)
            company.criticalDataTypes = []
        if 'Other' in company.criticalDataTypes: #if user entered a custom option for Data Type
            del company.criticalDataTypes[company.criticalDataTypes.index('Other')] #delete 'Other' from list
            if self.get_argument('otherCriticalDataTypes', None):
                company.criticalDataTypes.append(self.get_argument('otherCriticalDataTypes', None)) #add custom option to list.
        try: #try and get all checked items. 
            company.revenueSource = self.request.arguments['revenueSource']
        except: #if no checked items, then make it into an empty array (form validation should prevent this always)
            company.revenueSource = []
        if 'Other' in company.revenueSource: #if user entered a custom option for Revenue Source
            del company.revenueSource[company.revenueSource.index('Other')] #delete 'Other' from list
            if self.get_argument('otherRevenueSource', None):
                company.revenueSource.append(self.get_argument('otherRevenueSource', None)) #add custom option to list.
        company.companyCategory = self.get_argument("category", None)
        if company.companyCategory == 'Other': #if user entered custom option for Category
            company.companyCategory = self.get_argument('otherCategory', None)
        # try: #try and get all checked items. 
        #     company.sector = self.request.arguments['sector']
        # except: #if no checked items, then make it into an empty array (form validation should prevent this always)
        #     company.sector = []
        # if 'Other' in company.sector: #if user entered a custom option for Sector
        #     del company.sector[company.sector.index('Other')] #delete 'Other' from list
        #     if self.get_argument('otherSector', None):
        #         company.sector.append(self.get_argument('otherSector', None)) #add custom option to list.
        company.descriptionLong = self.get_argument('descriptionLong', None)
        company.descriptionShort = self.get_argument('descriptionShort', None)
        company.socialImpact = self.get_argument('socialImpact', None)
        company.financialInfo = self.get_argument('financialInfo', None)
        if self.get_argument('vetted') == 'True':
            company.vetted = True
        elif self.get_argument('vetted') == 'False':
            company.vetted = False
        if self.get_argument('vettedByCompany') == 'True':
            company.vettedByCompany = True
        elif self.get_argument('vettedByCompany') == 'False':
            company.vettedByCompany = False
        company.save()
        self.redirect('/admin/')

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
        #get values
        id = self.get_argument("id", None)
        datasetName = self.get_argument('datasetName', None)
        datasetURL = self.get_argument('datasetURL', None)
        agency = self.get_argument('agency', None)
        dataType = self.request.arguments['dataType']
        if 'Other' in dataType:
            del dataType[dataType.index('Other')]
            dataType.append(self.get_argument('otherDataType', None))
        rating = self.get_argument('rating', None)
        reason = self.get_argument('reason', None)
        #try: #to find existing dataset
        dataset = models.Dataset.objects.get(id=bson.objectid.ObjectId(id))
        dataset.datasetName = datasetName
        dataset.datasetURL = datasetURL
        dataset.dataType = dataType
        dataset.agency = agency
        for r in dataset.ratings: #get review that corresponds with this author and save the info.
            if str(r.author.id) == str(self.get_argument('authorID', None)):
                r.rating = rating
                r.reason = reason
        dataset.save()
        #except: #make a new one, for current company
            # company = models.Company.objects.get(id=bson.objectid.ObjectId(id))
            # dataset = models.Dataset(
            #     datasetName = datasetName,
            #     datasetURL = datasetURL,
            #     dataType = dataTypes,
            #     agency = agency
            # )
            # dataset.usedBy.append(company)
            # rating = models.Rating(
            #     author = company.contact,
            #     rating =rating,
            #     reason = reason
            # )
            # dataset.ratings.append(rating)
            # dataset.save()
            # company.datasets.append(dataset)
            # company.save()
        self.redirect("/")

class DeleteCompanyHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, id):
        try:
            company = models.Company.objects.get(id=bson.objectid.ObjectId(id)) 
            #we're deleting a company. Need to delete CEO, delete 
            if company.ceo:
                ceo = company.ceo
                ceo.delete()
            if company.contact:
                contact = company.contact
                contact.delete()
            #delete its datasets
            for d in company.datasets:
                d.delete()
            company.delete()
        except:
            dataset = models.Dataset.objects.get(id=bson.objectid.ObjectId(id))
            dataset.delete()
        self.redirect('/admin/')

class ViewHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, id):
        # c = models.Company.objects.get(id=bson.objectid.ObjectId(id))
        # d = []
        # for s in c.datasets:
        #     ratings = []
        #     for r in s.ratings:
        #         ratings.append({
        #             "author": str(r.author.id),
        #             "rating": r.rating,
        #             "reason": r.reason
        #         })
        #     companies = []
        #     for comps in s.usedBy:
        #         companies.append({
        #             "companyID": str(comps.id)
        #         })
        #     d.append({
        #         "ts": str(s.ts),
        #         "datasetName": s.datasetName,
        #         "datasetURL": s.datasetURL,
        #         "ratings": ratings,
        #         "dataType": s.dataType,
        #         "usedBy": companies
        #     })
        # obj = {
        #     "_id": {
        #         "$oid": str(c.id)
        #     },
        #     "ceo": {
        #         "firstName": c.ceo.firstName,
        #         "lastName": c.ceo.lastName,
        #         "personType": c.ceo.personType,
        #         "email": c.ceo.email,
        #         "ratings": [],
        #         "submittedDatasets": []
        #     },
        #     "companyFunction": c.companyFunction,
        #     "companyName": c.companyName,
        #     "companyType": c.companyType,
        #     "criticalDataTypes": c.criticalDataTypes,
        #     "datasets": d,
        #     "descriptionLong": c.descriptionLong,
        #     "descriptionShort": c.descriptionShort,
        #     "financialInfo": c.financialInfo,
        #     "fte": c.fte,
        #     "revenueSource": c.revenueSource,
        #     "sector": c.sector,
        #     "socialImpact": c.socialImpact,
        #     "submitter": {
        #         "firstName": c.submitter.firstName,
        #         "lastName": c.submitter.lastName,
        #         "personType": c.submitter.personType,
        #         "email": c.submitter.email,
        #         "submittedDatasets": str(c.submitter.submittedDatasets)
        #     },
        #     "ts": str(c.ts),
        #     "url": c.url,
        #     "vetted": c.vetted,
        #     "yearFounded": c.yearFounded
        # }
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
    @tornado.web.authenticated
    def get(self):
        self.render(
            "download.html",
            page_title='Download Data',
            page_heading='Download Data',
        )

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
        #CSV of all 500 companies
        csvwriter = csv.writer(open(os.path.join(os.path.dirname(__file__), 'static') + "/OD500_Companies.csv", "w"))
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
                for d in c.datasets:
                    newrow = [
                        c.companyName,
                        c.url,
                        c.city,
                        states[str(c.state).replace(" ","")],
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
                    stateAbbrev = states[str(c.state).replace(" ","")]
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
        #Get companies, turn into objects, and then dump into JSON File
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









































