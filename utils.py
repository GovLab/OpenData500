#coding: utf8 
from mongoengine import *
import models
from datetime import datetime
import logging
import os
import json
import csv
from collections import Counter
import numpy as np
import re
import bson

#Just some global varbs. 
favicon_path = '/static/img/favicon.ico'
companyType = ['Public', 'Private', 'Nonprofit']
companyFunction = ['Consumer Research and/or Marketing', 'Consumer Services', 'Data Management and Analysis', 'Financial/Investment Services', 'Information for Consumers']
criticalDataTypes = ['Federal Open Data', 'State Open Data', 'City/Local Open Data', 'Private/Proprietary Data Sources']
revenueSource = ['advertising', 'Data Management and Analytic Services', 'Database Licensing', 'Lead Generation To Other Businesses', 'Philanthropy', 'Software Licensing', 'subscriptions', 'User Fees for Web or Mobile Access']
sectors = ['Agriculture', 'Arts, Entertainment and Recreation' 'Crime', 'Education', 'Energy', 'Environmental', 'Finance', 'Geospatial data/mapping', 'Health and Healthcare', 'Housing/Real Estate', 'Manufacturing', 'Nutrition', 'Scientific Research', 'Social Assistance', 'Trade', 'Transportation', 'Telecom', 'Weather']
new_revenueSource = ["Advertising", "Consulting", "Contributions/Donations", "Data analysis for clients", "Database licensing", "Government contract", "Lead generation to other businesses", "Membership fees", "Philanthropic grants", "Software licensing", "Subscriptions", "User fees for web or mobile access"]
datatypes = ['Federal Open Data', 'State Open Data', 'City/Local Open Data']
categories = ["(Select a Category)", 'Business & Legal Services', 'Data/Technology', 'Education', 'Energy', 'Environment & Weather', 'Finance & Investment', 'Food & Agriculture', 'Geospatial/Mapping', 'Governance', 'Healthcare', 'Housing/Real Estate', 'Insurance', 'Lifestyle & Consumer', 'Research & Consulting', 'Scientific Research', 'Transportation']
source_count = ['1-10', '11-50', '51-100', '101+']
states ={ "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas", "CA": "California", "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware", "DC": "District of Columbia", "FL": "Florida", "GA": "Georgia", "HI": "Hawaii", "ID": "Idaho", "IL": "Illinois", "IN": "Indiana", "IA": "Iowa", "KA": "Kansas", "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland", "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi", "MO": "Missouri", "MT": "Montana", "NE": "Nebraska", "NV": "Nevada", "NH": "New Hampshire", "NJ": "New Jersey", "NM": "New Mexico", "NY": "New York", "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio", "OK": "Oklahoma", "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina", "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah", "VT": "Vermont", "VA": "Virginia", "WA": "Washington", "WV": "West Virginia", "WI": "Wisconsin", "WY": "Wyoming", "PR": "Puerto Rico"}
stateListAbbrev = { 
            "us": [ "", "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "DC", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KA", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY", "PR"],
            "ca": ["", "AB", "BC", "MB", "NB", "NL", "NT", "NS", "NU", "ON", "PE", "QC", "SK", "YT"],
            "mx": ["", "AS", "BC", "BS", "CC", "CS", "CH", "CL", "CM", "DF", "DG", "GT", "GR", "HG", "JC", "MC", "MN", "MS", "NT", "NL", "OC", "PL", "QT", "QR", "SP", "SL", "SR", "TC", "TS", "TL", "VZ", "YN", "ZS"]
            }
stateList = {
            "us": ["(Select State)", "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "District of Columbia", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming", "Puerto Rico"],
            "ca": ["(Select Province/Territory)", "Alberta", "British Columbia", "Manitoba", "New Brunswick", "Newfoundland and Labrador", "Northwest Territories", "Nova Scotia", "Nunavut", "Ontario", "Prince Edward Island", "Quebec", "Saskatchewan", "Yukon"],
            "mx": ["(Seleccione un Estado)", "Aguascalientes", "Baja California", "Baja California Sur", "Campeche", "Chiapas", "Chihuahua", "Coahuila", "Colima", "Distrito Federal", "Durango", "Guanajuato", "Guerrero", "Hidalgo", "Jalisco", "México", "Michoacán", "Morelos", "Nayarit", "Nuevo León", "Oaxaca", "Puebla", "Querétaro", "Quintana Roo", "San Luis Potosí", "Sinaloa", "Sonora", "Tabasco", "Tamaulipas", "Tlaxcala", "Veracruz", "Yucatán", "Zacatecas"]
            }
agency_types = ['Federal','State','City/County','University/Institution']
available_countries = ["us", "ca", "mx"]
country_keys = { "us":"United States", "ca":"Canada", "United States":"us", "Canada":"ca",  "Mexico":"mx", "mx":"Mexico"}


class Validators(object):
	def check_for_duplicates(self, companyName):
		#check if companyName exists:
		try: 
			c = models.Company.objects.get(prettyName=re.sub(r'([^\s\w])+', '', companyName).replace(" ", "-").title())
			response = { "error": "This company has already been submitted. Email opendata500@thegovlab.org for questions." }
		except:
			response = 'true'
		return response

class Tools(object):
    def re_do_filters(self, country):
        companies = models.Company.objects(country=country)
        for c in companies:
            filters = []
            filters.append(self.prettify(c.companyCategory))
            filters.append(c.state)
            for a in c.agencies:
                filters.append(a.prettyName)
            if c.submittedSurvey:
                filters.append("survey-company")
            c.filters = filters
            c.save()
        logging.info("Filters Redone.")

    def prettify(self, name):
        return re.sub(r'([^\s\w])+', '', name).replace(" ", "-")

class Form(object):
    def process_new_company(self, arguments):
        #-------------------CONTACT INFO---------------
        firstName = arguments['firstName']
        lastName = arguments["lastName"]
        title = arguments['title']
        email = arguments['email']
        phone = arguments['phone']
        contacted = True if 'contacted' in arguments else False
        contact = models.Person(
            firstName = firstName,
            lastName = lastName,
            title = title,
            email = email,
            phone = phone,
            contacted = contacted,
        )
        #-------------------CEO INFO---------------
        ceoFirstName = arguments['ceoFirstName']
        ceoLastName = arguments['ceoLastName']
        ceo = models.Person(
                firstName = ceoFirstName,
                lastName = ceoLastName,
                title = "CEO"
            )
        #-------------------COMPANY INFO---------------
        url = arguments['url']
        companyName = arguments['companyName']
        prettyName = re.sub(r'([^\s\w])+', '', companyName).replace(" ", "-").title()
        city = arguments['city']
        zipCode = arguments['zipCode']
        state = arguments['state']
        country = country_keys[arguments['country']]
        if 'companyType' in arguments:
            companyType = arguments['otherCompanyType'] if arguments['companyType'] == 'Other' else arguments['companyType']
        else:
            companyType = ''
        yearFounded = 0 if not arguments['yearFounded'] else arguments['yearFounded']
        fte = 0 if not arguments['fte'] else arguments['fte']
        if 'revenueSource' in arguments:
            revenueSource = [] if not arguments['revenueSource'] else arguments['revenueSource'].split(',')
            if 'Other' in revenueSource:
                del revenueSource[revenueSource.index('Other')]
                revenueSource.append(arguments['otherRevenueSource'])
        else:
            revenueSource = []
        if 'category' in arguments:
            companyCategory = arguments['otherCategory'] if arguments['category'] == 'Other' else arguments['category']
            filters = [companyCategory, state, "survey-company"]
        else:
            companyCategory = ''
            filters = []
        description = arguments['description']
        descriptionShort = arguments['descriptionShort']
        financialInfo = arguments['financialInfo']
        datasetWishList = arguments['datasetWishList']
        if 'sourceCount' in arguments:
            sourceCount = arguments['sourceCount']
        else:
            sourceCount = ''
        company = models.Company(
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
            locked=False,
            filters = filters,
            country=country
        )
        company.save()
        return company

    def process_company(self, arguments, id):
        try: 
            c = models.Company.objects.get(id=bson.objectid.ObjectId(id))
        except Exception, e:
            logging.info("Error processing company: " + str(e))
            return
        #-------------------CONTACT INFO---------------
        c.contact.firstName = arguments['firstName']
        c.contact.lastName = arguments["lastName"]
        c.contact.title = arguments['title']
        c.contact.email = arguments['email']
        c.contact.phone = arguments['phone']
        c.contact.contacted = True if 'contacted' in arguments else False
        #-------------------CEO INFO---------------
        c.ceo.firstName = arguments['ceoFirstName']
        c.ceo.lastName = arguments['ceoLastName']
        c.ceo.title = 'CEO'
        #-------------------COMPANY INFO---------------
        c.url = arguments['url']
        c.companyName = arguments['companyName'] if 'companyName' in arguments else c.companyName
        c.prettyName = re.sub(r'([^\s\w])+', '', c.companyName).replace(" ", "-").title()
        c.city = arguments['city']
        c.zipCode = arguments['zipCode']
        c.state = arguments['state']
        c.country = country_keys[arguments['country']]
        if 'companyType' in arguments:
            c.companyType = arguments['otherCompanyType'] if arguments['companyType'] == 'Other' else arguments['companyType']
        else:
            c.companyType = ''
        c.yearFounded = 0 if not arguments['yearFounded'] else arguments['yearFounded']
        c.fte = 0 if not arguments['fte'] else arguments['fte']
        if 'revenueSource' in arguments:
            c.revenueSource = [] if not arguments['revenueSource'] else arguments['revenueSource'].split(',')
            if 'Other' in c.revenueSource:
                del c.revenueSource[c.revenueSource.index('Other')]
                c.revenueSource.append(arguments['otherRevenueSource'])
        else:
            c.revenueSource = []
        if 'category' in arguments:
            c.companyCategory = arguments['otherCategory'] if arguments['category'] == 'Other' else arguments['category']
        else:
            c.companyCategory = ''
        c.filters = [c.companyCategory, c.state, "survey-company"]
        c.description = arguments['description']
        c.descriptionShort = arguments['descriptionShort']
        c.financialInfo = arguments['financialInfo']
        c.datasetWishList = arguments['datasetWishList']
        if 'sourceCount' in arguments:
            c.sourceCount = arguments['sourceCount']
        else:
            c.sourceCount = ''
        c.dataComments = arguments['dataComments'] if arguments['dataComments'] else c.dataComments
        c.vetted = True if 'vetted' in arguments else False
        c.display = True if 'display' in arguments else False
        c.vettedByCompany = True if 'vettedByCompany' in arguments else False
        c.submittedSurvey = True if 'submittedSurvey' in arguments else False
        c.vettedByCompany = False if 'vettedByCompany' in arguments else True
        c.locked = True if 'locked' in arguments else False
        c.lastUpdated = datetime.now()
        c.save()
        return

    def company_update_one(self, id, dictField, value):
        return models.Company.objects(id=bson.objectid.ObjectId(id)).update(**{'set__'+dictField:value})

    def company_has_agency(self, company, agency):
        return company in agency.usedBy

    def company_has_subagency(self, company, agency, subagency_name):
        for s in agency.subagencies:
                if s.name == subagency_name:
                    return company in s.usedBy

    def add_agency_to_company(self, company, agency):
        if agency not in company.agencies:
            company.agencies.append(agency)
            company.lastUpdated = datetime.now()
            if agency.prettyName not in company.filters:
                company.filters.append(agency.prettyName)
        if company not in agency.usedBy:
            agency.usedBy.append(company)
            agency.usedBy_count = len(agency.usedBy)
        agency.save()
        company.save()
        return

    def add_subagency_to_company(self, company, agency, subagency_name):
        if agency not in company.agencies:
            company.agencies.append(agency)
        if company not in agency.usedBy:
            agency.usedBy.append(company)
        for s in agency.subagencies:
            if s.name == subagency_name:
                if company not in s.usedBy:
                    s.usedBy.append(company)
        agency.save()
        company.save()

    def remove_specific_dataset_from_company(self, company, agency, subagency_name, dataset_name):
        if subagency_name == '':
            for d in agency.datasets:
                if d.datasetName == dataset_name:
                    agency.datasets.remove(d)
        else:
            for s in agency.subagencies:
                if s.name == subagency_name:
                    for d in s.datasets:
                        if d.datasetName == dataset_name:
                            s.datasets.remove(d)
        agency.save()
        company.lastUpdated = datetime.now() #Update Company's Time of Last Edit
        company.save()

    def remove_all_datasets_from_company(self, company, agency):
        for d in agency.datasets:
            if company == d.usedBy:
                self.remove_specific_dataset_from_company(company, agency, '', d.datasetName)
        for s in agency.subagencies:
            for d in s.datasets:
                if company == d.usedBy:
                    self.remove_specific_dataset_from_company(company, agency, s.name, d.datasetName)
        company.lastUpdated = datetime.now()
        company.save()
        agency.save()

    def remove_subagency_datasets_from_company(self, company, agency, subagency_name):
        temp = []
        for s in agency.subagencies:
            if s.name == subagency_name:
                for d in s.datasets:
                    if company != d.usedBy:
                        temp.append(d)
                s.datasets = temp
        agency.save()
        company.lastUpdated = datetime.now()
        company.save()

    def remove_subagency_from_company(self, company, agency, subagency_name):
        self.remove_subagency_datasets_from_company(company, agency, subagency_name)
        for s in agency.subagencies:
            if company in s.usedBy and s.name == subagency_name:
                s.usedBy.remove(company)
        agency.save()
        company.lastUpdated = datetime.now()
        company.save()

    def remove_agency_from_company(self, company, agency):
        self.remove_all_datasets_from_company(company, agency)
        for s in agency.subagencies:
            self.remove_subagency_from_company(company, agency, s.name)
        if agency in company.agencies:
            company.agencies.remove(agency)
        if agency.prettyName in company.filters:
            company.filters.remove(agency.prettyName)
        if company in agency.usedBy:
            agency.usedBy.remove(company)
            agency.usedBy_count = len(agency.usedBy)
        agency.save()
        company.lastUpdated = datetime.now()
        company.save()

    def edit_dataset(self, agency, subagency_name, dataset_name, previous_dataset_name, dataset_url, rating):
        logging.info("rating: " + str(rating) + " " + str(type(rating)))
        if subagency_name:
            for s in agency.subagencies:
                if s.name == subagency_name:
                    for d in s.datasets:
                        if d.datasetName == previous_dataset_name:
                            d.datasetName = dataset_name
                            d.datasetURL = dataset_url
                            d.rating = rating
        if subagency_name == '':
            for d in agency.datasets:
                if d.datasetName == previous_dataset_name:
                    d.datasetName = dataset_name
                    d.datasetURL = dataset_url
                    d.rating = rating
        agency.save()

    def add_dataset(self, company, agency, subagency_name, dataset_name, dataset_url, rating):
        dataset = models.Dataset(
                datasetName = dataset_name,
                datasetURL = dataset_url,
                rating = rating,
                usedBy = company)
        if subagency_name == '':
                agency.datasets.append(dataset)
        else:
            for s in agency.subagencies:
                if subagency_name == s.name:
                    s.datasets.append(dataset)
        agency.save()

class StatsGenerator(object):
    def create_new_stats(self, country):
        stats = models.Stats()
        stats.country = country
        stats.lastUpdate = datetime.now()
        stats.totalCompanies = 0
        stats.totalCompaniesWeb = 0
        stats.totalCompaniesSurvey = 0
        stats.totalCompaniesDisplayed = 0
        stats.totalAgencies = 0
        stats.save()
        self.update_all_state_counts(country)

    def get_total_companies(self, country):
        return models.Stats.objects.get(country=country).totalCompanies
    
    def get_total_companies_web(self, country):
        return models.Stats.objects.get(country=country).totalCompaniesWeb
    
    def get_total_companies_surveys(self, country):
        return models.Stats.objects.get(country=country).totalCompaniesSurvey

    def get_total_displayed_companies(self, country):
        return models.Stats.objects.get(country=country).totalCompaniesDisplayed

    def get_total_agencies(self, country):
        return models.Stats.objects.get(country=country).totalAgencies

    def update_total_agencies(self, country):
        s = models.Stats.objects.get(country=country)
        s.totalAgencies = models.Agency.objects(country=country).count()
        s.save()

    def update_totals_companies(self, country):
        s = models.Stats.objects.get(country=country)
        s.totalCompanies = models.Company.objects(country=country).count()
        s.totalCompaniesWeb = models.Company.objects(Q(submittedThroughWebsite = True) & Q(country=country)).count()
        s.totalCompaniesSurvey = models.Company.objects(Q(submittedSurvey = True) & Q(country=country)).count()
        s.totalCompaniesDisplayed = models.Company.objects(Q(displayed=True) & Q(country=country)).count()
        s.save()
    
    def increase_individual_state_count(self, state, country):
        stats = models.Stats.objects.get(country=country)
        for s in stats.states:
            if s.abbrev == state:
                s.count = s.count + 1
        stats.save()

    def decrease_individual_state_count(self, state, country):
        stats = models.Stats.objects.get(country=country)
        for s in stats.states:
            if s.abbrev == state:
                s.count = s.count - 1
        stats.save()

    def update_all_state_counts(self, country):
        stats = models.Stats.objects.get(country=country)
        companies  = models.Company.objects(Q(display=True) & Q(country=country))
        stateCount = []
        for c in companies:
            stateCount.append(c.state)
        stats.states = []
        for i in range(1, len(stateList[country])):
            s = models.States(
                name = stateList[country][i],
                abbrev = stateListAbbrev[country][i],
                count = stateCount.count(stateListAbbrev[country][i]))
            stats.states.append(s)
        stats.save()

    def refresh_stats(self, country):
        stats = models.Stats.objects.get(country=country)
        stats.totalCompanies = models.Company.objects(country=country).count()
        stats.totalCompaniesWeb = models.Company.objects(Q(submittedThroughWebsite = True) & Q(country=country)).count()
        stats.totalCompaniesSurvey = models.Company.objects(Q(submittedSurvey = True) & Q(country=country)).count()
        stats.totalCompaniesDisplayed = models.Company.objects(Q(display=True) & Q(country=country)).count()
        companies  = models.Company.objects(Q(display=True) & Q(country=country))
        stateCount = []
        for c in companies:
            stateCount.append(c.state)
        stats.states = []
        for i in range(1, len(stateList[country])):
            s = models.States(
                name = stateList[country][i],
                abbrev = stateListAbbrev[country][i],
                count = stateCount.count(stateListAbbrev[country][i]))
            stats.states.append(s)
        stats.lastUpdate = datetime.now()
        stats.save()


class FileGenerator(object):
    def generate_company_json(self, country):
        #------COMPANIES JSON---------
        companies = models.Company.objects(Q(display=True) & Q(country=country))
        companiesJSON = []
        for c in companies:
            agencies = []
            for a in c.agencies:
                datasets_agency = []
                for d in a.datasets:
                    if c == d.usedBy:
                        ds = {
                            "datasetName":d.datasetName,
                            "datasetURL":d.datasetURL,
                            "rating":d.rating
                        }
                        datasets_agency.append(ds)
                subagencies = []
                for s in a.subagencies:
                    if c in s.usedBy:
                        datasets_subagency = []
                        for d in s.datasets:
                            if c == d.usedBy:
                                ds = {
                                    "datasetName":d.datasetName,
                                    "datasetURL":d.datasetURL,
                                    "rating":d.rating
                                }
                                datasets_subagency.append(ds)
                        sub = {
                            "name":s.name,
                            "abbrev":s.abbrev,
                            "url":s.url,
                            "datasets":datasets_subagency
                        }
                        subagencies.append(sub)
                ag = {
                    "name": a.name,
                    "abbrev":a.abbrev,
                    "prettyName":a.prettyName,
                    "url": a.url,
                    "type":a.dataType,
                    "datasets":datasets_agency,
                    "subagencies":subagencies
                }
                agencies.append(ag)
            try:
                subagencies
            except Exception, e:
                logging.info("No Subagencies: " + str(e))
                subagencies = []
            company = {
                "company_name_id": c.prettyName,
                "companyName": c.companyName,
                "url": c.url,
                "city": c.city,
                "state": c.state,
                "zipCode": c.zipCode,
                "ceoFirstName": c.ceo.firstName,
                "ceoLastName": c.ceo.lastName,
                "yearFounded": c.yearFounded,
                "fte": c.fte,
                "companyType": c.companyType,
                "companyCategory": c.companyCategory,
                "revenueSource": c.revenueSource,
                "description": c.description,
                "descriptionShort": c.descriptionShort,
                "agencies":agencies,
                "subagencies":subagencies
            }
            companiesJSON.append(company)
        with open(os.path.join(os.path.dirname(__file__), 'static') + "/files/" + country + '_OD500_Companies.json', 'w') as outfile:
            json.dump(companiesJSON, outfile)
        logging.info("Company JSON File Done!")
    def generate_agency_json(self, country):
        #--------------JSON OF AGENCIES------------
        agencies = models.Agency.objects(country=country)
        agenciesJSON = []
        for a in agencies:
            #--------DATASETS AT AGENCY LEVEL------
            datasets_agency = []
            for d in a.datasets:
                ds = {
                    "datasetName":d.datasetName,
                    "datasetURL":d.datasetURL,
                    "rating":d.rating,
                    "usedBy":d.usedBy.prettyName
                }
                datasets_agency.append(ds)
            #--------SUBAGENCIES------
            subagencies = []
            for s in a.subagencies:
                datasets_subagency = []
                for d in s.datasets:
                    #logging.info(d.datasetName)
                    ds = {
                        "datasetName":d.datasetName,
                        "datasetURL":d.datasetURL,
                        "rating":d.rating,
                        "usedBy": d.usedBy.prettyName
                    }
                    datasets_subagency.append(ds)
                usedBy = []
                for u in s.usedBy:
                    usedBy.append(u.prettyName)
                sub = {
                    "name":s.name,
                    "abbrev":s.abbrev,
                    "url":s.url,
                    "datasets":datasets_subagency,
                    "usedBy":usedBy
                }
                subagencies.append(sub)
            #--------SUBAGENCIES------
            usedBy = []
            for u in a.usedBy:
                usedBy.append(u.prettyName)
            ag = {
                "name": a.name,
                "abbrev":a.abbrev,
                "prettyName":a.prettyName,
                "url": a.url,
                "type":a.dataType,
                "datasets":datasets_agency,
                "subagencies":subagencies,
                "usedBy":usedBy
            }
            agenciesJSON.append(ag)
        with open(os.path.join(os.path.dirname(__file__), 'static') + "/files/" + country + '_OD500_Agencies.json', 'w') as outfile:
            json.dump(agenciesJSON, outfile)
        logging.info("Agency JSON File Done!")
    def generate_company_csv(self, country):
        #---CSV OF ALL COMPANIES----
        companies = models.Company.objects(Q(display=True) & Q(country=country))
        csvwriter = csv.writer(open(os.path.join(os.path.dirname(__file__), 'static') + "/files/" + country + "_OD500_Companies.csv", "w"))
        csvwriter.writerow([
            'company_name_id',
            'company_name',
            'url',
            'city',
            'state',
            'zip_code',
            'ceo_first_name',
            'ceo_last_name',
            'year_founded',
            'full_time_employees',
            'company_type',
            'company_category',
            'revenue_source',
            'description',
            'description_short',
            'financial_info',
            'sourceCount'
            ])
        for c in companies:
            newrow = [
                c.prettyName,
                c.companyName,
                c.url,
                c.city,
                c.state,
                c.zipCode,
                c.ceo.firstName,
                c.ceo.lastName,
                c.yearFounded,
                c.fte,
                c.companyType,
                c.companyCategory,
                ', '.join(c.revenueSource),
                c.description,
                c.descriptionShort,
                c.financialInfo,
                c.sourceCount 
            ]
            for i in range(len(newrow)):  # For every value in our newrow
                if hasattr(newrow[i], 'encode'):
                    newrow[i] = newrow[i].encode('utf8')
            csvwriter.writerow(newrow)
        logging.info("Company CSV File Done!")
    def generate_company_all_csv(self, country):
        #---CSV OF ALL COMPANIES----
        companies = models.Company.objects(country=country)
        csvwriter = csv.writer(open(os.path.join(os.path.dirname(__file__), 'static') + "/files/" + country + "_OD500_Companies_All.csv", "w"))
        csvwriter.writerow([
            'company_name_id',
            'company_name',
            'url',
            'city',
            'state',
            'zip_code',
            'contact_first_name',
            'contact_last_name',
            'contact_email',
            'ceo_first_name',
            'ceo_last_name',
            'year_founded',
            'full_time_employees',
            'company_type',
            'company_category',
            'revenue_source',
            'description',
            'description_short',
            'financial_info',
            'source_count',
            'data_comments',
            'dataset_wishlist',
            'confidentiality',
            'ts',
            'survey_submitted',
            'vetted',
            'locked',
            'vettedByCompany',
            'display',
            'notes'
            ])
        for c in companies:
            newrow = [
                c.prettyName,
                c.companyName,
                c.url,
                c.city,
                c.state,
                c.zipCode,
                c.contact.firstName,
                c.contact.lastName,
                c.contact.email,
                c.ceo.firstName,
                c.ceo.lastName,
                c.yearFounded,
                c.fte,
                c.companyType,
                c.companyCategory,
                ', '.join(c.revenueSource),
                c.description,
                c.descriptionShort,
                c.financialInfo,
                c.sourceCount,
                c.dataComments,
                c.datasetWishList,
                c.confidentiality,
                c.ts,
                c.submittedSurvey,
                c.vetted,
                c.locked,
                c.vettedByCompany,
                c.display,
                c.notes
            ]
            for i in range(len(newrow)):  # For every value in our newrow
                if hasattr(newrow[i], 'encode'):
                    newrow[i] = newrow[i].encode('utf8')
            csvwriter.writerow(newrow)
        logging.info("All Companies CSV File Done!")

    def generate_agency_csv(self, country):
        companies = models.Company.objects(Q(country=country) & Q(display=True))
        agencies = models.Agency.objects(country=country)
        csvwriter = csv.writer(open(os.path.join(os.path.dirname(__file__), 'static') + "/files/" + country + "_OD500_Agencies.csv", "w"))
        csvwriter.writerow([
            'agency_name',
            'agency_abbrev',
            'agency_type',
            'subagency_name',
            'subagency_abbrev',
            'url',
            'used_by',
            'used_by_category',
            'dataset_name',
            'dataset_url'
            ])
        index_of_companies = {}
        for c in companies:
            index_of_companies[str(c.id)] = [c.companyName, c.companyCategory]
        AD = []
        SD = []
        S = []
        for a in agencies:
            for d in a.datasets:
                if d.usedBy.display:
                    newrow = [
                        a.name, 
                        a.abbrev, 
                        a.dataType, 
                        "General", 
                        "", 
                        a.url, 
                        index_of_companies[str(d.usedBy.id)][0],
                        index_of_companies[str(d.usedBy.id)][1],
                        d.datasetName,
                        d.datasetURL
                    ]
                    AD.append(str(d.usedBy.companyName + "|"+ a.name))
                    #write csv row here
                    for i in range(len(newrow)):  # For every value in our newrow
                        if hasattr(newrow[i], 'encode'):
                            newrow[i] = newrow[i].encode('utf8')
                    csvwriter.writerow(newrow)
            for s in a.subagencies:
                for d in s.datasets:
                    if d.usedBy.display:
                        newrow = [
                            a.name, 
                            a.abbrev, 
                            a.dataType, 
                            s.name, 
                            s.abbrev, 
                            s.url, 
                            index_of_companies[str(d.usedBy.id)][0],
                            index_of_companies[str(d.usedBy.id)][1],
                            d.datasetName,
                            d.datasetURL
                        ]
                        SD.append(str(d.usedBy.companyName + "|"+ s.name))
                        SD.append(str(d.usedBy.companyName + "|"+ a.name))
                        #write csv row here
                        for i in range(len(newrow)):  # For every value in our newrow
                            if hasattr(newrow[i], 'encode'):
                                newrow[i] = newrow[i].encode('utf8')
                        csvwriter.writerow(newrow)
                for c in s.usedBy:
                    if str(c.companyName + "|"+s.name) not in SD and c.display:
                        newrow = [
                            a.name, 
                            a.abbrev, 
                            a.dataType, 
                            s.name, 
                            s.abbrev, 
                            s.url, 
                            index_of_companies[str(c.id)][0],
                            index_of_companies[str(c.id)][1],
                            "",
                            ""
                        ]
                        S.append(str(c.companyName + "|"+a.name))
                        #write csv row
                        for i in range(len(newrow)):  # For every value in our newrow
                            if hasattr(newrow[i], 'encode'):
                                newrow[i] = newrow[i].encode('utf8')
                        csvwriter.writerow(newrow)
            for c in a.usedBy:
                if str(c.companyName + "|"+a.name) not in SD+AD+S and c.display:
                    newrow = [
                            a.name, 
                            a.abbrev, 
                            a.dataType, 
                            "General", 
                            "", 
                            a.url, 
                            index_of_companies[str(c.id)][0],
                            index_of_companies[str(c.id)][1],
                            "",
                            ""
                        ]
                    #companies_accounted_for.append(d.usedBy)
                    #write csv row
                    for i in range(len(newrow)):  # For every value in our newrow
                        if hasattr(newrow[i], 'encode'):
                            newrow[i] = newrow[i].encode('utf8')
                    csvwriter.writerow(newrow)
        #done, wrap up csv
        logging.info("Agency CSV File Done!")


    def generate_sankey_json(self, country):
        #get qualifying agencies
        agencies = models.Agency.objects(Q(usedBy__not__size=0) & Q(source__not__exact="web") & Q(dataType="Federal")).order_by('name') #federal agencies from official list that are used by a company
        #going to just make a list of all the category-agency combos
        cats = [] #list of used categories
        cats_agency_combo = []
        for a in agencies:
            for c in a.usedBy:
                if c.display:
                    if c.companyCategory in categories: #exclude "Other" Categories, and only displayed companies
                        cats_agency_combo.append(c.companyCategory+"|"+a.name)
                        cats.append(c.companyCategory)
        count = list(Counter(cats_agency_combo).items()) #count repeat combos
        #make dictionary
        cat_v_agencies = {"nodes": [], "links": []}
        #make node list
        cat_agency_list = [] #keep track of category agency list, we're going to need their indeces. 
        for c in categories: #Add categories to node list
            if c in cats: #only add category if used
                cat_v_agencies['nodes'].append({"name":c})
                cat_agency_list.append(c)
        for a in agencies: #add agency names to node list
            used = False
            for c in a.usedBy:
                if c.display:
                    used = True
            if used:
                cat_v_agencies['nodes'].append({"name":a.name})
                cat_agency_list.append(a.name)
        #make the links
        for c in count:
            link = {"source":cat_agency_list.index(c[0].split('|')[0]), "target":cat_agency_list.index(c[0].split('|')[1]), "value":c[1]} #make a link
            cat_v_agencies['links'].append(link)
        for n in cat_v_agencies['nodes']: #Abbreviate Department
            n['name'] = n['name'].replace('Department', 'Dept.')
            n['name'] = n['name'].replace('Administration', 'Admin.')
            n['name'] = n['name'].replace('United States', 'US')
            n['name'] = n['name'].replace('National', "Nat'l")
        with open(os.path.join(os.path.dirname(__file__), 'static') + "/files/" + country + '_sankey.json', 'w') as outfile:
            json.dump(cat_v_agencies, outfile)

    def generate_chord_chart_files(self, country):
        agencies = models.Agency.objects(Q(usedBy__not__size=0) & Q(source__not__exact="web") & Q(dataType="Federal") & Q(country="us")).order_by('name')
        #get agencies that are used
        used_agencies_categories = []
        for a in agencies:
            if a.usedBy and a.source == "dataGov":
                used_agencies_categories.append(a.name)
        #Keep track of # of categories
        num_agencies = len(used_agencies_categories)
        #get categories that are actually used from agencies that are used
        for a in agencies:
            if a.usedBy and a.source == "dataGov":
                for c in a.usedBy:
                    if c.companyCategory in categories and c.companyCategory not in used_agencies_categories:
                        used_agencies_categories.append(c.companyCategory)
        #logging.info(used_agencies_categories)
        name_key = {}
        key_name = {}
        for i, name in enumerate(used_agencies_categories):
            name_key[name] = i
            key_name[str(i)] = name
        #Make matrix
        l = len(name_key)
        matrix = np.matrix([[0]*l]*l)
        #populate matrix
        for a in agencies:
            if a.source == "dataGov":
                for c in a.usedBy:
                    if c.companyCategory in categories: 
                        matrix[name_key[c.companyCategory], name_key[a.name]] += 1
                        matrix[name_key[a.name], name_key[c.companyCategory]] += 1
        #make json
        matrix = matrix.tolist()
        data = {"matrix":matrix, "names":key_name, "num_agencies":num_agencies}
        #abbreviate some stuff
        for key in data['names']:
            data['names'][key] = data['names'][key].replace('Department', 'Dept.')
            data['names'][key] = data['names'][key].replace('Administration', 'Admin.')
            data['names'][key] = data['names'][key].replace('United States', 'US')
            data['names'][key] = data['names'][key].replace('U.S.', 'US')
            data['names'][key] = data['names'][key].replace('National', "Nat'l")
            data['names'][key] = data['names'][key].replace('Federal', "Fed.")
            data['names'][key] = data['names'][key].replace('Commission', "Com.")
            data['names'][key] = data['names'][key].replace('International', "Int'l")
            data['names'][key] = data['names'][key].replace('Development', "Dev.")
            data['names'][key] = data['names'][key].replace('Corporation', "Corp.")
            data['names'][key] = data['names'][key].replace('Institute', "Inst.")
            data['names'][key] = data['names'][key].replace('Administrative', "Admin.")
            data['names'][key] = data['names'][key].replace(' and ', " & ")
            data['names'][key] = data['names'][key].replace('Financial', "Fin.")
            data['names'][key] = data['names'][key].replace('Protection', "Prot.")
            data['names'][key] = data['names'][key].replace('Environmental', "Env.")
        #save to file
        with open(os.path.join(os.path.dirname(__file__), 'static') + '/files/' + country + '_matrix.json', 'w') as outfile:
            json.dump(data, outfile)
        logging.info("Chord Chart File Done!")

    def generate_visit_csv(self, country):
        #---CSV OF ALL COMPANIES----
        visits = models.Visit.objects()
        csvwriter = csv.writer(open(os.path.join(os.path.dirname(__file__), 'static') + "/files/" + country + "_OD500_Visits.csv", "w"))
        csvwriter.writerow([
            'ts',
            'referer',
            'page',
            'user_agent',
            'ip'
            ])
        for v in visits:
            newrow = [
                v.ts,
                v.r,
                v.p,
                v.ua,
                v.ip
            ]
            for i in range(len(newrow)):  # For every value in our newrow
                if hasattr(newrow[i], 'encode'):
                    newrow[i] = newrow[i].encode('utf8')
            csvwriter.writerow(newrow)
        logging.info("Visit CSV File Done!")

    def generate_agency_list(self, country):
        agencies = models.Agency.objects(Q(country=country) & Q(source__not__exact="web"))
        agency_list = []
        for a in agencies:
            label = [a.name, " (", a.abbrev, ")"]
            agency = {
                "label": ''.join(filter(None, label)),
                "a": a.name,
                "aa": a.abbrev,
                "s": "",
                "ss": ""
            }
            agency_list.append(agency)
            if a.subagencies:
                for s in a.subagencies:
                    label = [a.name, " (", a.abbrev, ")", " - ", s.name, " (", s.abbrev, ")"]
                    agency = {
                        "label": ''.join(filter(None, label)),
                        "a": a.name,
                        "aa": a.abbrev,
                        "s": s.name,
                        "ss": s.abbrev
                    }
                    agency_list.append(agency)
        with open(os.path.join(os.path.dirname(__file__), 'static') + "/files/" + country + '_Agency_List.json', 'w') as outfile:
            json.dump(agency_list, outfile)
        logging.info("Agency List Done!")




















