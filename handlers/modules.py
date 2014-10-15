from base import *
import json




class FormModule(tornado.web.UIModule):
    def render(self, country, lan, required, edit, company=None):
        with open("templates/modules/module_text/form.json") as json_file:
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
            full_time_employees=full_time_employees,
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
        with open("templates/modules/module_text/formData.json") as json_file:
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
    def render(self, country, lan, company=None):
        with open("templates/modules/module_text/agencyAdd.json") as json_file:
                form = json.load(json_file)
        return self.render_string(
            'modules/agencyAdd.html', 
            c=company, 
            country=country, 
            lan=lan, 
            form=form[lan]
            )

class AdminSettingsModule(tornado.web.UIModule):
	def render(self, country, lan, company=None):
		with open("templates/modules/module_text/agencyAdd.json") as json_file:
			form = json.load(json_file)
		return self.render_string(
			'modules/adminSettings.html',
			c=company,
			country=country,
			lan=lan,
			form=form[lan])

















