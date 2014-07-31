from base import *
import json


#--------------------------------------------------------MAIN PAGE------------------------------------------------------------
class MainHandler(BaseHandler):
    @tornado.web.addslash
    #@tornado.web.authenticated
    def get(self, country=None):
        if not country:
            country = "us"
        if country not in available_countries:
            self.redirect("/404/")
            return
        with open("templates/"+country+"/settings.json") as json_file:
            settings = json.load(json_file)
        # lan = self.get_argument("lan", "")
        # if lan and lan != self.get_cookie("lan"):
        #     self.set_cookie("lan", lan)
        # if not lan:
        #     lan = self.get_cookie("lan")
        # if not lan: or lan not in settings["available_languages"]:
        #     lan = settings['default_language']
        #     self.set_cookie("lan", lan)
        lan = self.get_cookie("lan")
        if not lan:
            lan = settings['default_language']
        self.render(
            country.lower()+ "/" + lan + "/index.html",
            settings = settings,
            menu=settings['menu'][lan],
            user=self.current_user,
            lan = lan,
            country=country
        )

#--------------------------------------------------------TEST PAGE------------------------------------------------------------
class TestHandler(BaseHandler):
    @tornado.web.addslash
    #@tornado.web.authenticated
    def get(self, number):
        self.render(
            "index_" + number + ".html",
            user=self.current_user,
            page_title='Open Data500',
            page_heading='Welcome to the Open Data 500 Pre-Launch',
        )

#--------------------------------------------------------ROUNDATABLE PAGE------------------------------------------------------------
class RoundtableHandler(BaseHandler):
    @tornado.web.addslash
    #@tornado.web.authenticated
    def get(self, country, rt=None):
        if self.request.uri == "/roundtables/doc/":
            self.redirect("/us/roundtables/?rt=doc")
        if not country:
            self.redirect("/us/roundtables/")
            return
        rt = self.get_argument("rt", "main")
        with open("templates/us/settings.json") as json_file:
            settings = json.load(json_file)
        logging.info("Country: " + country + " RT: " + rt)
        self.render(
            "us/en/"+rt+"_roundtable.html",
            page_title = "Open Data Roundtables",
            page_heading = "Open Data Roundtables",
            user=self.current_user,
            country=country,
            settings=settings,
            menu=settings['menu']['en'],
            lan="en"
        )


#--------------------------------------------------------STATIC PAGE------------------------------------------------------------
class StaticPageHandler(BaseHandler):
    @tornado.web.addslash
    #@tornado.web.authenticated
    def get(self, country=None, page=None):
        #check if company page, get company if so
        try:
            company = models.Company.objects.get(Q(prettyName=page) & Q(display=True))
            if company.country != country:
                self.redirect("/" + company.country + "/" + company.prettyName + "/")
                return
        except DoesNotExist:
            company = None
        except MultipleObjectsReturned:
            company = models.Company.objects(Q(prettyName=page) & Q(country=country) & Q(display=True))[0]
            if company.country != country:
                self.redirect("/" + company.country + "/" + company.prettyName + "/")
                return
        except Exception, e:
            logging.info("Uncaught Exception: " + str(e))
            self.render(
                "500.html",
                page_title='500 - Server Error',
                user=self.current_user,
                page_heading='Uh oh... You broke it.',
                message = "I'm telling."
            )
            return
        #country, language, settings for page
        if not country:
            country = "us" #us default country
        if country not in available_countries:
            self.redirect("/404/")
            return
        with open("templates/"+country+"/settings.json") as json_file:
            settings = json.load(json_file)
        lan = self.get_cookie("lan")
        if not lan:
            lan = settings['default_language']
        if company: 
            self.render(
                company.country + "/" + lan + "/company.html",
                page_title=company.companyName,
                user=self.current_user,
                page_heading=company.companyName,
                company = company,
                menu=settings['menu'][lan],
                settings=settings,
                country=country,
                lan=lan
            )
            return
        else:
            try:
                page_title=settings['page_titles'][lan][page]
            except:
                page_title="OD500"
            try: 
                self.render(
                    country + "/" + lan + "/" + page + ".html",
                    user=self.current_user,
                    country=country,
                    menu=settings['menu'][lan],
                    settings=settings,
                    page_title=page_title,
                    lan=lan
                )
                return
            except Exception, e:
                self.render(country + "/" + lan + '/404.html',
                    user=self.current_user,
                    country=country,
                    page_title=page_title,
                    menu=settings['menu'][lan],
                    settings=settings,
                    lan=lan,
                    error=e
                )
                return



#--------------------------------------------------------FULL LIST PAGE------------------------------------------------------------
class ListHandler(BaseHandler):
    @tornado.web.addslash
    #@tornado.web.authenticated
    def get(self, country=None, name=None):
        if name == "candidates":
            self.redirect("/us/list/")
            return 
        if not country:
            country = "us"
        if country not in available_countries:
            self.redirect("/404/")
            return
        with open("templates/"+country+"/settings.json") as json_file:
                settings = json.load(json_file)
        lan = self.get_cookie("lan")
        if not lan:
            lan = settings['default_language']
        companies = models.Company.objects(Q(display=True) & Q(country=country)).order_by('prettyName')
        agencies = models.Agency.objects(Q(usedBy__not__size=0) & Q(source="dataGov") & Q(dataType="Federal")).order_by("-usedBy_count").only("name", "abbrev", "prettyName")[0:16]
        stats = models.Stats.objects().first()
        try:
            page_title=settings['page_titles'][lan]["list"]
        except:
            page_title="OD500"
        self.render(
            country+"/" + lan + "/list.html",
            companies = companies,
            stats = stats,
            states = states,
            agencies = agencies,
            categories = categories,
            user = self.current_user,
            country = country,
            menu=settings['menu'][lan],
            page_title=page_title,
            settings=settings,
            lan=lan
        )

#--------------------------------------------------------CHART PAGE------------------------------------------------------------
class ChartHandler(BaseHandler):
    @tornado.web.addslash
    def get(self):
        #log visit
        try: 
            visit = models.Visit()
            if self.request.headers.get('Referer'):
                visit.r = self.request.headers.get('Referer')
                logging.info("Chart requested from: " + self.request.headers.get('Referer'))
            else:
                visit.r = ''
                logging.info("Chart requested from: Cannot get referer")
            visit.p = "/chart/"
            visit.ua = self.request.headers.get('User-Agent')
            visit.ip = self.request.headers.get('X-Forwarded-For', self.request.headers.get('X-Real-Ip', self.request.remote_ip))
            if visit.r != "http://www.opendata500.com/" or visit.r != "http://www.opendata500.com":
                visit.save()
        except Exception, e:
            logging.info("Could not save visit information: " + str(e))
        finally:
            self.render("solo_chart.html")


#--------------------------------------------------------VALIDATE COMPANY EXISTS PAGE------------------------------------------------------------
#------SHOULD MOVE TO UTILS-------
class ValidateHandler(BaseHandler):
    def post(self):
        #check if companyName exists:
        country = self.get_argument("country", None)
        if not country:
            country = 'us'
        companyName = self.get_argument("companyName", None)
        prettyName = re.sub(r'([^\s\w])+', '', companyName).replace(" ", "-").title()
        try: 
            c = models.Company.objects.get(Q(country=country) & Q(prettyName=prettyName))
            logging.info('company exists.')
            self.set_status(404)
        except:
            logging.info('company does not exist. Carry on.')
            self.set_status(200)

#--------------------------------------------------------SURVEY PAGE------------------------------------------------------------
class SubmitCompanyHandler(BaseHandler):
    @tornado.web.addslash
    #@tornado.web.authenticated
    def get(self, country=None):
        if not country:
            country = "us"
        if country not in available_countries:
            self.redirect("/404/")
            return
        with open("templates/"+country+"/settings.json") as json_file:
                settings = json.load(json_file)
        lan = self.get_cookie("lan")
        if not lan:
            lan = settings['default_language']
        try:
            page_title=settings['page_titles'][lan]["submit"]
        except:
            page_title="OD500"
        self.render(
            country+ "/" + lan + "/submitCompany.html",
            page_title = page_title,
            country=country,
            country_keys=country_keys,
            companyType = companyType,
            companyFunction = companyFunction,
            criticalDataTypes = criticalDataTypes,
            revenueSource = revenueSource,
            categories=categories,
            datatypes = datatypes,
            stateList = stateList,
            user=self.current_user,
            menu=settings['menu'][lan],
            stateListAbbrev=stateListAbbrev,
            settings=settings,
            lan=lan
        )

    #@tornado.web.authenticated
    def post(self, country=None):
        #print all arguments to log:
        logging.info("Submitting New Company")
        logging.info(self.request.arguments)
        form_values = {k:','.join(v) for k,v in self.request.arguments.iteritems()}
        self.application.form.process_new_company(form_values)
        self.application.stats.update_all_state_counts(country)
        id = str(company.id)
        self.write({"id": id})


#--------------------------------------------------------DATA SUBMIT PAGE------------------------------------------------------------
class SubmitDataHandler(BaseHandler):
    @tornado.web.addslash
    #@tornado.web.authenticated
    def get(self, country, id):
        if not country:
            country = "us"
        if country not in available_countries:
            self.redirect("/404/")
            return
        with open("templates/"+country+"/settings.json") as json_file:
                settings = json.load(json_file)
        lan = self.get_cookie('lan')
        if not lan or lan not in settings["available_languages"]:
            lan = settings["default_language"]
        company = models.Company.objects.get(id=bson.objectid.ObjectId(id))
        if company.country != country:
            self.redirect(str('/'+company.country+'/addData/'+id))
            return
        try:
            page_title=settings['page_titles'][lan]['submitData']
        except:
            page_title="OD500"
        self.render(company.country + "/" + lan + "/submitData.html",
            page_title=page_title,
            page_heading = "Agency and Data Information for " + company.companyName,
            company = company,
            user=self.current_user,
            settings=settings,
            country=country,
            lan=lan
        )

    #@tornado.web.authenticated
    def post(self, country, id):
        logging.info("Submitting Data: "+ self.get_argument("action", None))
        logging.info(self.request.arguments)
        try:
            company = models.Company.objects.get(id=bson.objectid.ObjectId(id))
        except Exception, e:
            logging.info("Could not get company: " + str(e))
            self.set_status(400)
        country = company.country
        with open("templates/"+country+"/settings.json") as json_file:
                settings = json.load(json_file)
        lan = self.get_cookie("lan")
        if not lan:
            lan = settings['default_language']
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
            self.write({"result":"success", "redirect":"/"+ country + "/thanks/?lan=" + lan})
        #------------------------------------ADDING AGENCY/SUBAGENCY------------------------
        if action == "add agency":
            #Existing AGENCY
            logging.info("Trying to get: " + agencyName)
            try:
                agency = models.Agency.objects.get(Q(name=agencyName) & Q(country=company.country))
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
            if agency.prettyName not in company.filters:
                company.filters.append(agency.prettyName)
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
                if agency.prettyName in company.filters: #remove from list of filters
                    company.filters.remove(agency.prettyName)
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
                agency = models.Agency.objects.get(Q(name = agencyName) & Q(country = company.country))
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
            dataset = models.Dataset(
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
                agency = models.Agency.objects.get(Q(name = agencyName) & Q(country = company.country))
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
                agency = models.Agency.objects.get(Q(name = agencyName) & Q(country = company.country))
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








