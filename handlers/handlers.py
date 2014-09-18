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
        #------------LOAD LANGUAGE
        lan = self.get_argument("lan", None)
        if lan:
            if lan != self.get_cookie('lan') and lan in settings['available_languages']:
                self.set_cookie("lan", lan)
                self.redirect("/" + country + "/")
                return
            if lan not in settings['available_languages']:
                lan = settings['default_language']
        elif not lan and self.get_cookie('lan') in settings['available_languages']:
            lan = self.get_cookie('lan')
        else:
            lan = settings['default_language']
        #------------END LANGUAGE
        self.render(
            country.lower()+ "/" + lan + "/index.html",
            settings = settings,
            #menu=settings['menu'][lan],
            user=self.current_user,
            lan = lan,
            country=country
        )

#--------------------------------------------------------TEST PAGE------------------------------------------------------------
class TestHandler(BaseHandler):
    @tornado.web.addslash
    #@tornado.web.authenticated
    def get(self, number):
        with open("templates/us/settings.json") as json_file:
            settings = json.load(json_file)
        self.render(
            "index_" + number + ".html",
            user=self.current_user,
            page_title='Open Data500',
            page_heading='Welcome to the Open Data 500 Pre-Launch',
            settings=settings,
            lan='en',
            country='us'
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
        #------------LOAD LANGUAGE
        lan = self.get_argument("lan", None)
        if lan:
            if lan != self.get_cookie('lan') and lan in settings['available_languages']:
                self.set_cookie("lan", lan)
                self.redirect(self.request.uri)
                return
            if lan not in settings['available_languages']:
                lan = settings['default_language']
        elif not lan and self.get_cookie('lan') in settings['available_languages']:
            lan = self.get_cookie('lan')
        else:
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
        #------------LOAD LANGUAGE
        lan = self.get_argument("lan", None)
        if lan:
            if lan != self.get_cookie('lan') and lan in settings['available_languages']:
                self.set_cookie("lan", lan)
                self.redirect(self.request.uri)
                return
            if lan not in settings['available_languages']:
                lan = settings['default_language']
        elif not lan and self.get_cookie('lan') in settings['available_languages']:
            lan = self.get_cookie('lan')
        else:
            lan = settings['default_language']
        companies = models.Company.objects(Q(display=True) & Q(country=country)).order_by('prettyName')
        if country != 'mx':
            agencies = models.Agency.objects(Q(usedBy__not__size=0) & Q(source="dataGov") & Q(dataType="Federal") & Q(country=country)).order_by("-usedBy_count").only("name", "abbrev", "prettyName")[0:16]
        if country == 'mx':
            agencies = models.Agency.objects(Q(dataType="Federal") & Q(country=country)).order_by("-usedBy_count").only("name", "abbrev", "prettyName")[0:16]
        stats = models.Stats.objects.get(country=country)
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
            categories = categories[lan],
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
        prettyName = self.application.tools.prettify(companyName)
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
        #------------LOAD LANGUAGE
        lan = self.get_argument("lan", None)
        if lan:
            if lan != self.get_cookie('lan') and lan in settings['available_languages']:
                self.set_cookie("lan", lan)
                self.redirect(self.request.uri)
                return
            if lan not in settings['available_languages']:
                lan = settings['default_language']
        elif not lan and self.get_cookie('lan') in settings['available_languages']:
            lan = self.get_cookie('lan')
        else:
            lan = settings['default_language']
        with open("templates/form.json") as json_file:
                form = json.load(json_file)
        self.render(
            country+ "/" + lan + "/submitCompany.html",
            country=country,
            country_keys=country_keys,
            companyType = companyType[lan],
            revenueSource = revenueSource[lan],
            business_models = business_models[lan],
            social_impacts = social_impacts[lan],
            source_count = source_count,
            categories=categories[lan],
            data_types = data_types[lan],
            stateList = stateList,
            user=self.current_user,
            menu=settings['menu'][lan],
            stateListAbbrev=stateListAbbrev,
            settings=settings,
            form = form[lan],
            lan=lan
        )

    #@tornado.web.authenticated
    def post(self, country=None):
        logging.info("Submitting New Company")
        logging.info(self.request.arguments)
        form_values = {k:','.join(v) for k,v in self.request.arguments.iteritems()}
        company = self.application.form.create_new_company(form_values)
        id = str(company.id)
        form_values['submittedSurvey'] = True
        form_values['vetted'] = False
        form_values['vettedByCompany'] = True
        form_values['submittedThroughWebsite'] = True
        form_values['locked'] = False
        form_values['display'] = False
        try:
            self.application.form.process_company(form_values, id)
        except Exception, e:
            logging.info("Could not save company: " + str(e))
            logging.info("Aborting")
            self.write("Could not save company: " + str(e))
            company.delete()
            return
        country = country_keys[form_values['country']]
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
        #------------LOAD LANGUAGE
        lan = self.get_argument("lan", None)
        if lan:
            if lan != self.get_cookie('lan') and lan in settings['available_languages']:
                self.set_cookie("lan", lan)
                self.redirect(self.request.uri)
                return
            if lan not in settings['available_languages']:
                lan = settings['default_language']
        elif not lan and self.get_cookie('lan') in settings['available_languages']:
            lan = self.get_cookie('lan')
        else:
            lan = settings['default_language']
        company = models.Company.objects.get(id=bson.objectid.ObjectId(id))
        if company.country != country or '/'+company.country+'/' not in self.request.uri:
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
            lan=lan,
            source_count = source_count,
            data_types = data_types[lan],
            data_impacts = data_impacts[lan]
        )

    #@tornado.web.authenticated
    def post(self, country, id):
        #logging.info("Submitting Data: "+ self.get_argument("action", None))
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
        #varbs
        a_id = self.get_argument("a_id", None)
        agency_name = self.get_argument("agency", None)
        subagency_name = self.get_argument("subagency", None)
        dataset_name = self.get_argument("dataset_name", None)
        previous_dataset_name = self.get_argument('previous_dataset_name', None)
        dataset_url = self.get_argument("dataset_url", None)
        try:
            rating = int(self.get_argument("rating", None))
        except:
            rating = 0
        action = self.get_argument("action", None)
        if action != 'submit-form':
            try:
                agency = models.Agency.objects.get(Q(name=agency_name) & Q(country=company.country))
            except Exception, e:
                logging.info("Error: " + str(e))
                self.set_status(400)
        response = {"message":"", "agency":0, "subagency":0, "dataset":0}
        #------------------------------------JUST SAVE DATA COMMENT QUESTION------------------------
        if action == "submit-form":
            try:
                form_values = {k:','.join(v) for k,v in self.request.arguments.iteritems()}
                self.application.form.process_company_data_info(form_values, id)
                self.write({"response":"success", "redirect":"/"+ country + "/thanks/"})
            except Exception, e:
                logging.info("Error: " + str(e))
                self.write({"response":"error"})
        #------------------------------------ADDING AGENCY/SUBAGENCY------------------------
        if action == 'add':
            try: 
                if not self.application.form.company_has_agency(company, agency):
                    self.application.form.add_agency_to_company(company, agency)
                    response["agency"] = 1
                if subagency_name:
                    if not self.application.form.company_has_subagency(company, agency, subagency_name):
                        self.application.form.add_subagency_to_company(company, agency, subagency_name)
                        response['subagency'] = 1
                self.write(response)
            except Exception, e:
                logging.info("Could not add agency/subagency: " + str(e))
                response['message'] = 'error'
                self.write(response)
        #------------------------------------DELETING AGENCY------------------------
        if action == "delete agency":
            try: 
                self.application.form.remove_agency_from_company(company, agency)
                response['agency'] = -1
                self.write(response)
            except Exception, e:
                logging.info("Could not delete agency: " + str(e))
                response['message'] = 'error'
                self.write(response)
        #------------------------------------DELETING SUBAGENCY------------------------
        if action == 'delete subagency':
            try: 
                self.application.form.remove_subagency_from_company(company, agency, subagency_name)
                response['subagency'] = -1
                self.write(response)
            except Exception, e:
                logging.info("Could not delete subagency: " + str(e))
                response['message'] = 'error'
                self.write(response)
        #------------------------------------ADDING DATASET------------------------
        if action == "add dataset":
            try:
                self.application.form.add_dataset(company, agency, subagency_name, dataset_name, dataset_url, rating)
                response['dataset'] = 1
                self.write(response)
            except Exception, e:
                logging.info("Could not add dataset: " + str(e))
                response['message'] = 'error'
                self.write(response)
        #------------------------------------EDITING DATASET------------------------
        if action == "edit dataset":
            try: 
                self.application.form.edit_dataset(agency, subagency_name, dataset_name, previous_dataset_name, dataset_url, rating)
                response['dataset'] = 2
                self.write(response)
            except Exception, e:
                logging.info("Could not modify dataset: " + str(e))
                response['message'] = 'error'
                self.write(response)
        #------------------------------------DELETING DATASET------------------------
        if action == "delete dataset":
            try:
                self.application.form.remove_specific_dataset_from_company(company, agency, subagency_name, dataset_name)
                response['dataset'] = -1
                self.write(response)
            except Exception, e:
                logging.info("Error deleting dataset: " + str(e))
                self.write(response)

class NotFoundHandler(BaseHandler):
    def get(self):
        self.render('404.html',
            lan='english',
            country='us')

class FormModule(tornado.web.UIModule):
    def render(self, country, lan, required, edit, company=None):
        with open("templates/form.json") as json_file:
                form = json.load(json_file)
        return self.render_string(
            'modules/form.html', 
            c=company, 
            country=country, 
            lan=lan, 
            required=required, 
            edit=edit,
            form=form[lan],
            country_keys=country_keys,
            companyType = companyType[lan],
            revenueSource = revenueSource[lan],
            business_models = business_models[lan],
            social_impacts = social_impacts[lan],
            source_count = source_count,
            categories=categories[lan],
            data_types = data_types[lan],
            stateList = stateList,
            stateListAbbrev=stateListAbbrev
            )

class FormDataModule(tornado.web.UIModule):
    def render(self, country, lan, required, company=None):
        with open("templates/formData.json") as json_file:
                form = json.load(json_file)
        return self.render_string(
            'modules/formData.html', 
            c=company, 
            country=country, 
            lan=lan, 
            required=required, 
            form=form[lan],
            source_count = source_count,
            data_types = data_types[lan],
            data_impacts = data_impacts[lan]
            )

class AgencyAddModule(tornado.web.UIModule):
    def render(self, country, lan, required, edit, company=None):
        with open("templates/agencyAdd.json") as json_file:
                form = json.load(json_file)
        return self.render_string(
            'modules/agencyAdd.html', 
            c=company, 
            country=country, 
            lan=lan, 
            required=required, 
            edit=edit,
            form=form[lan],
            source_count = source_count,
            data_types = data_types[lan],
            data_impacts = data_impacts[lan]
            )

