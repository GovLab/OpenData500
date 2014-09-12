from base import *
import json

#--------------------------------------------------------LOGIN PAGE------------------------------------------------------------
class LoginHandler(BaseHandler): 
    @tornado.web.addslash
    def get(self):
        with open("templates/us/settings.json") as json_file:
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
        #------------END LANGUAGE
        self.render(
            "admin/" + lan + "/login.html", 
            next=self.get_argument("next","/"), 
            message=self.get_argument("error",""),
            page_title="Please Login",
            page_heading="Login to OD500" ,
            lan=lan,
            country='us',
            menu=settings['menu']['en'],
            settings=settings
            )

    def post(self):
        username = self.get_argument("username", "")
        password = self.get_argument("password", "").encode('utf-8')
        try: 
            user = models.Users.objects.get(username=username)
        except Exception, e:
            logging.info('unsuccessful login')
            error_msg = u"?error=" + tornado.escape.url_escape("User does not exist")
            self.redirect(u"/login" + error_msg)
        if user and user.password and bcrypt.hashpw(password, user.password.encode('utf-8')) == user.password:
            logging.info('successful login for '+username)
            self.set_current_user(username)
            self.redirect("/admin/companies/")
        else: 
            logging.info('unsuccessful login')
            error_msg = u"?error=" + tornado.escape.url_escape("Incorrect Password")
            self.redirect(u"/login" + error_msg)

    def set_current_user(self, user):
        logging.info('setting ' + user)
        if user:
            self.set_secure_cookie("user", tornado.escape.json_encode(user))
        else: 
            self.clear_cookie("user")

#--------------------------------------------------------REGISTER PAGE------------------------------------------------------------
class RegisterHandler(LoginHandler):
    @tornado.web.addslash
    @tornado.web.authenticated
    def get(self):
        try:
            user = models.Users.objects.get(username=self.current_user)
        except Exception, e:
            logging.info("Could not get user: " + str(e))
            self.redirect("/login/")
        country = user.country
        with open("templates/" + country + "/settings.json") as json_file:
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
        #------------END LANGUAGE
        self.render(
                "admin/" + lan +"/register.html", 
                next=self.get_argument("next","/"),
                page_title="Register",
                page_heading="Register for OD500",
                user=self.current_user,
                country = country,
                country_keys=country_keys,
                menu=settings['menu'][lan],
                settings=settings,
                lan=lan
            )

    @tornado.web.authenticated
    def post(self):
        username = self.get_argument("username", "")
        try:
            user = models.Users.objects.get(username=username)
        except:
            user = ''
        if user:
            error_msg = u"?error=" + tornado.escape.url_escape("Login name already taken")
            self.redirect(u"/register" + error_msg)
        else: 
            password = self.get_argument("password", "")
            hashedPassword = bcrypt.hashpw(password, bcrypt.gensalt(8))
            country = self.get_argument("country", None)
            newUser = models.Users(
                username=username,
                password = hashedPassword,
                country=country
                )
            newUser.save()
            self.set_current_user(username)
            self.redirect("/")


#--------------------------------------------------------LOGOUT HANDLER------------------------------------------------------------
class LogoutHandler(BaseHandler): 
    def get(self):
        self.clear_cookie("user")
        #self.clear_cookie("country")
        self.redirect(u"/login")


#--------------------------------------------------------ADMIN PAGE------------------------------------------------------------
class CompanyAdminHandler(BaseHandler):
    @tornado.web.addslash
    @tornado.web.authenticated
    def get(self, country=None, page=None):
        if not page:
            self.redirect("/admin/companies/")
            return
        try:
            user = models.Users.objects.get(username=self.current_user)
        except Exception, e:
            logging.info("Could not get user: " + str(e))
            self.redirect("/login/")
        country = user.country
        logging.info("Working in: " + country)
        with open("templates/"+user.country+"/settings.json") as json_file:
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
        #------------END LANGUAGE
        surveySubmitted = models.Company.objects(Q(submittedSurvey=True) & Q(vetted=True) & Q(country=country)).order_by('prettyName')
        sendSurveys = models.Company.objects(Q(submittedSurvey=False) & Q(country=country))
        needVetting = models.Company.objects(Q(submittedSurvey=True) & Q(vetted=False) & Q(country=country)).order_by('-lastUpdated', 'prettyName')
        try: 
            stats = models.Stats.objects.get(country=country)
        except Exception, e:
            logging.info("Error: " + str(e))
            self.application.stats.create_new_stats(country)
            stats = models.Stats.objects.get(country=country)
        self.render(
            "admin/" + lan + "/admin_companies.html",
            page_title='OpenData500',
            page_heading='Admin - ' + country.upper(),
            surveySubmitted = surveySubmitted,
            needVetting = needVetting,
            user=self.current_user,
            country = country,
            sendSurveys = sendSurveys,
            stats = stats,
            settings=settings,
            lan=lan
        )

    def post(self, country=None, page=None):
        try:
            user = models.Users.objects.get(username=self.current_user)
        except Exception, e:
            logging.info("Could not get user: " + str(e))
            self.redirect("/login/")
        action = self.get_argument("action", None)
        country = user.country
        if action == "refresh":
            self.application.stats.refresh_stats(country)
            self.application.files.generate_visit_csv(country)
            stats = models.Stats.objects.get(country=country)
            self.write({"totalCompanies": stats.totalCompanies, 
                        "totalCompaniesWeb":stats.totalCompaniesWeb, 
                        "totalCompaniesSurvey":stats.totalCompaniesSurvey,
                        "totalCompaniesDisplayed": stats.totalCompaniesDisplayed})
        elif action == "files":
            #self.application.files.generate_company_json(country)
            self.application.files.generate_agency_json(country)
            self.application.files.generate_company_csv(country)
            self.application.files.generate_company_all_csv(country)
            self.application.files.generate_agency_csv(country)
            self.write("success")
        elif action == "vizz":
            #self.application.files.generate_sankey_json()
            self.application.files.generate_chord_chart_files(country)
            self.write("success")
        elif action == 'display':
            try:
                id = self.get_argument("id", None)
                c = models.Company.objects.get(id=bson.objectid.ObjectId(id))
            except Exception, e:
                logging.info("Error: " + str(e))
                self.write(str(e))
            c.display = not c.display
            c.save()
            self.application.stats.update_all_state_counts(country)
            self.write("success")
        elif action == 'agency_csv':
            self.application.files.generate_agency_csv(country)
            self.write("success")
        elif action == 'company_csv':
            self.application.files.generate_company_csv(country)
            self.write("success")
        elif action == 'company_all_csv':
            self.application.files.generate_company_all_csv(country)
            self.write("success")
        elif action == "redo_filters":
            self.application.tools.re_do_filters(country)
            self.write("success")


#--------------------------------------------------------ADMIN AGENCIES PAGE------------------------------------------------------------
class AgencyAdminHandler(BaseHandler):
    @tornado.web.addslash
    @tornado.web.authenticated
    def get(self, country=None, page=None):
        try:
            user = models.Users.objects.get(username=self.current_user)
        except Exception, e:
            logging.info("Could not get user: " + str(e))
            self.redirect("/login/")
        country = user.country
        with open("templates/"+user.country+"/settings.json") as json_file:
            settings = json.load(json_file)
        agencies = models.Agency.objects(country=country).order_by('name')
        stats = models.Stats.objects.get(country=country)
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
        #------------END LANGUAGE
        self.render(
            "admin/" + lan + "/admin_agencies.html",
            page_title='Admin - Agencies - OpenData500',
            page_heading='Admin - ' + country.upper(),
            user=self.current_user,
            stats = stats,
            agencies=agencies,
            settings=settings,
            country=country,
            lan=lan
        )

    @tornado.web.addslash
    @tornado.web.authenticated
    def post(self, country=None, page=None):
        try:
            user = models.Users.objects.get(username=self.current_user)
        except Exception, e:
            logging.info("Could not get user: " + str(e))
            self.redirect("/login/")
        country = user.country
        action = self.get_argument("action", "")
        if action == "agency_list":
            self.application.files.generate_agency_list(country)
            self.write({"message":"All right, I'm done."})
        elif action == "refresh":
            self.application.stats.update_total_agencies(country)
            self.write({"message":"All right, I'm done.", "total_agencies": self.application.stats.get_total_agencies(country)})

#--------------------------------------------------------NEW COMPANY PAGE------------------------------------------------------------
class NewCompanyHandler(BaseHandler):
    @tornado.web.addslash
    @tornado.web.authenticated
    def get(self):
        try:
            user = models.Users.objects.get(username=self.current_user)
        except Exception, e:
            logging.info("Could not get user: " + str(e))
            self.redirect("/login/")
            return
        country = user.country
        with open("templates/"+user.country+"/settings.json") as json_file:
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
        #------------END LANGUAGE
        self.render("admin/" + lan + "/admin_add_company.html",
            page_heading = "New Company",
            companyType = companyType[lan],
            revenueSource = revenueSource[lan],
            business_models = business_models[lan],
            categories=categories[lan],
            social_impacts = social_impacts[lan],
            data_types = data_types[lan],
            data_impacts = data_impacts[lan],
            source_count = source_count,
            stateList = stateList,
            stateListAbbrev=stateListAbbrev,
            user=self.current_user,
            country = country,
            country_keys = country_keys,
            settings = settings,
            lan = lan
        )

    def post(self):
        logging.info(self.request.arguments)
        form_values = {k:','.join(v) for k,v in self.request.arguments.iteritems()}
        company = self.application.form.create_new_company(form_values)
        id = str(company.id)
        form_values['submittedSurvey'] = False
        form_values['vetted'] = False
        form_values['vettedByCompany'] = False
        form_values['submittedThroughWebsite'] = False
        form_values['locked'] = False
        form_values['display'] = False
        try:
            self.application.form.process_company(form_values, id)
            self.application.form.process_company_data_info(form_values,id)
        except Exception, e:
            logging.info("Could not save company: " + str(e))
            logging.info("Aborting")
            self.write("Could not save company: " + str(e))
            company.delete()
            return
        country = country_keys[form_values['country']]
        self.application.stats.update_all_state_counts(country)
        self.write('success')


#--------------------------------------------------------EDIT COMPANY PAGE------------------------------------------------------------
class EditCompanyHandler(BaseHandler):
    @tornado.web.addslash
    def get(self, country=None, page=None, id=None):
        try: 
            company = models.Company.objects.get(id=bson.objectid.ObjectId(id))
        except Exception, e:
            logging.info("Could not get company: " + str(e))
            self.redirect("/404/")
            return
        if company.country != country:
            self.redirect(str('/'+company.country+'/' + page + '/'+id))
            return
        with open("templates/"+company.country+"/settings.json") as json_file:
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
        #------------END LANGUAGE
        if page == 'edit':
            #non-admin edit
            if not company.locked:
                self.render(company.country + "/" + lan + "/editCompany.html",
                    page_heading = "Editing " + company.companyName,
                    company = company,
                    companyType = companyType[lan],
                    revenueSource = revenueSource[lan],
                    business_models = business_models[lan],
                    categories=categories[lan],
                    social_impacts = social_impacts[lan],
                    data_impacts = data_impacts[lan],
                    data_types = data_types[lan],
                    source_count = source_count,
                    stateList = stateList,
                    stateListAbbrev=stateListAbbrev,
                    user=self.current_user,
                    country = company.country,
                    country_keys=country_keys,
                    settings = settings,
                    lan=lan,
                    id = str(company.id)
                )
            else:
                self.redirect('/' + company.country + '/locked/')
                return
        if page == 'admin-edit':
            try:
                user = models.Users.objects.get(username=self.current_user)
            except Exception, e:
                logging.info("Could not get user: " + str(e))
                self.redirect("/login/")
            if user.country != company.country:
                logging.info("This user does not have access to edit this company")
                self.redirect('/' + user.country + '/locked/')
                return
            #lan = settings['default_language']
            self.render("admin/" + lan + "/admin_edit_company.html",
                page_heading = "Editing " + company.companyName + ' (Admin)',
                company = company,
                companyType = companyType[lan],
                revenueSource = revenueSource[lan],
                business_models = business_models[lan],
                categories=categories[lan],
                social_impacts = social_impacts[lan],
                data_types = data_types[lan],
                source_count = source_count,
                data_impacts = data_impacts[lan],
                stateList = stateList,
                stateListAbbrev=stateListAbbrev,
                user=self.current_user,
                country = company.country,
                country_keys = country_keys,
                id = str(company.id),
                settings = settings,
                lan = settings['default_language']
            )

    def post(self, country=None, page=None, id=None):
        logging.info(self.request.arguments)
        form_values = {k:','.join(v) for k,v in self.request.arguments.iteritems()}
        logging.info(self.request.uri)
        if 'admin-edit' in self.request.uri:
            form_values['submittedSurvey'] = True if 'submittedSurvey' in form_values else False
            form_values['vetted'] = True if 'vetted' in form_values else False
            form_values['vettedByCompany'] = True if 'vettedByCompany' in form_values else False
            form_values['submittedThroughWebsite'] = True if 'submittedThroughWebsite' in form_values else False
            form_values['locked'] = True if 'locked' in form_values else False
            form_values['display'] = True if 'display' in form_values else False
        else:
            form_values['vettedByCompany'] = True
        self.application.form.process_company(form_values, id)
        self.application.form.process_company_data_info(form_values,id)
        self.write('success')

#--------------------------------------------------------EDIT AGENCY (ADMIN) PAGE------------------------------------------------------------
class AdminEditAgencyHandler(BaseHandler):
    @tornado.web.addslash
    @tornado.web.authenticated
    def get(self, id=None):
        try:
            user = models.Users.objects.get(username=self.current_user)
        except Exception, e:
            logging.info("Could not get user: " + str(e))
            self.redirect("/login/")
            return
        country = user.country
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
        #------------END LANGUAGE
        if id:
            try:
                agency = models.Agency.objects.get(id=bson.objectid.ObjectId(id))
            except Exception, e:
                logging.info("Could not get agency: " + str(e))
                self.redirect('/404/')
                return
            self.render('admin/' + lan + '/admin_edit_agency.html',
                page_heading="Editing " + agency.name,
                page_title="Editing " + agency.name,
                user=self.current_user,
                agency=agency,
                agency_types=agency_types,
                country = agency.country,
                settings=settings,
                lan=settings['default_language']
            )
        else:
            blank_agency = models.Agency(name="", 
                abbrev="", 
                url="", 
                source="", 
                subagencies=[], 
                datasets=[], 
                usedBy=[], 
                notes="", 
                country=country)
            self.render(
            "admin/" + lan + "/admin_edit_agency.html",
            page_title='Admin - Edit Agencies - OpenData500',
            page_heading='New Agency',
            user=self.current_user,
            country=country,
            agency=blank_agency,
            agency_types=agency_types,
            settings=settings,
            lan=settings['default_language']
        )

    @tornado.web.authenticated
    def post(self, id):
        try:
            user = models.Users.objects.get(username=self.current_user)
        except Exception, e:
            logging.info("Could not get user: " + str(e))
            self.redirect("/login/")
        country = user.country
        action = self.get_argument("action", "")
        if action != "add-agency":
            try:
                agency = models.Agency.objects.get(id=bson.objectid.ObjectId(id))
            except Exception, e:
                logging.info("Could not get agency: " + str(e))
                self.write({"error":"Agency not found."})
        #logging.info(self.request.arguments)
        subagency_old_name = self.get_argument("subagency_old_name","")
        subagency_new_name = self.get_argument("subagency_new_name", "")
        subagency_abbrev = self.get_argument("subagency_abbrev", "")
        subagency_url = self.get_argument("subagency_url", "")
        agency_new_name = self.get_argument("agency_new_name", "")
        agency_old_name = self.get_argument("agency_old_name", None)
        agency_prettyName = re.sub(r'([^\s\w])+', '', agency_new_name).replace(" ", "-").title()
        agency_abbrev = self.get_argument("agency_abbrev", None)
        agency_url = self.get_argument("agency_url", None)
        agency_type = self.get_argument("agency_type", None)
        agency_source = self.get_argument("agency_source", None)
        agency_notes = self.get_argument("agency_notes", None)
        #------------------------------------------ADD NEW AGENCY----------------------------
        if action == "add-agency":
            new_agency = models.Agency()
            new_agency.name = agency_new_name
            new_agency.prettyName = agency_prettyName
            new_agency.abbrev = agency_abbrev
            new_agency.url = agency_url
            new_agency.dataType = agency_type
            new_agency.source = agency_source
            new_agency.notes = agency_notes
            new_agency.country = country
            new_agency.usedBy_count = 0
            new_agency.usedBy = []
            try:
               new_agency.save()
            except Exception, e:
                logging.info("Could not save agency: " + str(e))
                self.write({"error":"Could not save agency"})
                return
            self.write({"message":"Save Successful", "id":str(new_agency.id)})
            self.application.files.generate_agency_list(country)
            return
        #------------------------------------------EDIT SUBAGENCY----------------------------
        if action =="edit-subagency":
            for s in agency.subagencies:
                if s.name.lower() == subagency_new_name.lower() and s.name.lower() != subagency_old_name.lower():
                    self.write({"message":"Another Subagency already has this name."})
                    return
            for s in agency.subagencies:
                if s.name == subagency_old_name:
                    s.name = subagency_new_name
                    s.abbrev = subagency_abbrev
                    s.url = subagency_url
                    agency.save()
                    self.application.files.generate_agency_list(country)
                    self.write({"message":"Edit Successful"})
                    return 
        #------------------------------------------ADD SUBAGENCY----------------------------
        if action == "add-subagency":
            for s in agency.subagencies:
                if s.name.lower() == subagency_new_name.lower() and s.name.lower() != subagency_old_name.lower():
                    self.write({"message":"Another Subagency already has this name.", "error":""})
                    return
            s = models.Subagency(
                name = subagency_new_name,
                abbrev = subagency_abbrev,
                url = subagency_url)
            agency.subagencies.append(s)
            agency.save()
            self.application.files.generate_agency_list(country)
            self.write({"message":"Subagency added!", 
                "heading":s.name, 
                "name":s.name, 
                "abbrev":s.abbrev, 
                "url":s.url, 
                "new_action":"edit-subagency", 
                "button":"Save Edits", 
                "delete_button":""})
            return
        #------------------------------------------DELETE SUBAGENCY----------------------------
        if action == "delete-subagency":
            logging.info("about to delete")
            for s in agency.subagencies:
                if s.name == subagency_old_name:
                    if len(s.usedBy) != 0:
                        self.write({"message": "Subagency is used by a company or companies; cannot delete.", "error":"error"})
                        return
                    else:
                        agency.subagencies.remove(s)
            agency.save()
            self.application.files.generate_agency_list(country)
            self.write({"message":"Subagency deleted :("})
            return
        #------------------------------------------EDIT AGENCY----------------------------
        if action == "edit-agency":
            if agency_new_name != agency_old_name:
                logging.info("name changed")
                try:
                    agency_exists = models.Agency.objects.get(name=agency_new_name)
                except Exception, e:
                    logging.info("Could not find agency, therefore not duplicate name, carry on: " + str(e))
                    agency_exists = False
                if agency_exists:
                    self.write({"message":"Another agency already has that name, try another."})
                    return
            agency.name = agency_new_name
            agency.prettyName = agency_prettyName
            agency.abbrev = agency_abbrev
            agency.url = agency_url
            agency.dataType = agency_type
            agency.source = agency_source
            agency.notes = agency_notes
            agency.save()
            self.application.files.generate_agency_list(country)
            self.write({"message":"Edits saved!"})
            return
        #------------------------------------------DELETE AGENCY----------------------------
        if action == "delete-agency":
            logging.info(self.request.arguments)
            if agency.subagencies:
                for s in agency.subagencies:
                    if len(s.usedBy) != 0:
                        self.write({"message": "Agency has one or more subagencies used by a company or companies; cannot delete."})
                        return
            if agency.usedBy_count or len(agency.usedBy) !=0:
                self.write({"message": "Agency is used by one or more companies; cannot delete."})
                return
            if agency.usedBy_count == 0 and len(agency.usedBy) == 0:
                agency.delete()
                self.application.files.generate_agency_list(country)
                self.write({"message": "Agency Deleted"})
                return


#--------------------------------------------------------DELETE COMPANY------------------------------------------------------------
class DeleteCompanyHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, id):
        try:
            company = models.Company.objects.get(id=bson.objectid.ObjectId(id)) 
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
            for d in a.datasets:
                if d.usedBy == company:
                    a.datasets.remove(d)
            #---REMOVE DATASETS (SUBAGENCY)---
            for s in a.subagencies:
                for d in s.datasets:
                    if d.usedBy == company:
                        s.datasets.remove(d)
                #--REMOVE FROM SUBAGENCIES--
                if company in s.usedBy:
                    s.usedBy.remove(company)
            #-----REMOVE FROM AGENCY----
            a.usedBy.remove(company)
            a.usedBy_count = len(a.usedBy)
            a.save()
        ##----------DELETE COMPANY--------
        company.delete()
        self.redirect('/admin/companies/')













