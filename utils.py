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
companyType = {
                "en": ['Public', 'Private', 'Nonprofit'],
                "es": ['Pública', 'Privada', 'Sin Fines de Lucro']
            }
business_models = {
                    "en": [
                        'Business to Business', 'Business to Consumer', 
                        'Business to Government'],
                    "es": [
                        'Empresa a Empresa', 'Empresa a Consumidor', 
                        'Empresa a Gobierno']
                }
revenueSource = {
                "en": [
                    "Advertising", "Consulting", "Contributions/Donations", 
                    "Data analysis for clients", "Database licensing", 
                    "Government contract", "Lead generation to other businesses", 
                    "Membership fees", "Philanthropic grants", 
                    "Software licensing", "Subscriptions", 
                    "User fees for web or mobile access"],
                "es": [
                    "Análisis de datos", "Consultoría", 
                    "Contratos gubernamentales", "Contribuciones/Donaciones", 
                    "Tarifas para el servicio móvil/internet", "Filantropía", 
                    "Generación de clientes", "Licencias de software", 
                    "Licencias de bases de datos", "Cuotas de membresía", 
                    "Publicidad", "Suscripciones"]
            }
datatypes = ['Federal Open Data', 'State Open Data', 'City/Local Open Data']
categories = {
                "en": {
                    "us": [
                        'Business & Legal Services', 'Data/Technology', 
                        'Education', 'Energy', 'Environment & Weather', 
                        'Finance & Investment', 'Food & Agriculture', 
                        'Geospatial/Mapping', 'Governance', 'Healthcare', 
                        'Housing/Real Estate', 'Insurance', 'Lifestyle & Consumer', 
                        'Media', 'Research & Consulting', 'Scientific Research', 
                        'Transportation'],
                    "mx": [
                        'Business & Legal Services', 'Data/Technology', 
                        'Education', 'Energy', 'Environment & Weather', 
                        'Finance & Investment', 'Food & Agriculture', 
                        'Geospatial/Mapping', 'Governance', 'Healthcare', 
                        'Housing/Real Estate', 'Insurance', 'Lifestyle & Consumer', 
                        'Media', 'Research & Consulting', 'Scientific Research', 
                        'Transportation'],
                    "au": [
                        'Business & Legal Services', 'Data/Technology', 
                        'Education', 'Energy', 'Environment & Weather', 
                        'Finance & Investment', 'Food & Agriculture', 
                        'Geospatial/Mapping', 'Mining/Manufacturing', 
                        'Healthcare', 'Housing/Real Estate', 'Insurance', 
                        'Lifestyle & Consumer', 'Media', 'Research & Consulting', 
                        'Telecommunications / ISP\'s', 'Transportation']
                },
                "es": {
                    "mx": [
                        "Agricultura y Alimentación", "Vivienda/Bienes Raíces", 
                        "Clima y Medio Ambiente", "Educación", "Energía", 
                        "Estilos de vida y Consumidores", "Finanzas e Inversiones", 
                        "Gobierno", "Investigación Científica", 
                        "Investigación y Consultoría", "Mapeo/Geoespacial", 
                        "Medios", "Salud", "Seguros", "Servicios Legales", 
                        "Tecnología/Datos", "Transporte"]
                }
            }
social_impacts = {
                "en": [
                    'Citizen engagement and participation', 
                    'Consumer empowerment', 'Educational opportunity', 
                    'Environment and climate change', 'Financial access', 
                    'Food access and supply', 'Good governance', 
                    'Healthcare access', 'Housing access', 'Public safety'],
                "es": [
                    "Acceso a la salud", "Acceso a la vivienda", 
                    "Acceso financiero", "Acceso y suministro de alimentos", 
                    '"Buen Gobierno"', "Empoderamiento al consumidor", 
                    "Medio ambiente y cambio climático", 
                    "Oportunidades educacionales", "Participación ciudadana", 
                    "Seguridad pública"]
            }
data_types = {
                "en": [
                    "Agriculture & Food", "Business", "Consumer", 
                    "Demographics & Social", "Economics", "Education", 
                    "Energy", "Environment", "Finance", "Geospatial/Mapping", 
                    "Government Operations", "Health/Healthcare", "Housing", 
                    "International/Global Development", "Legal", "Manufacturing", 
                    "Science and Research", "Public Safety", "Tourism", 
                    "Transportation", "Weather"],
                "es": [
                    "Agricultura y Alimentación", "Ciencia e investigación", 
                    "Clima", "Consumidor", "Demografía y Población", 
                    "Desarrollo internacional", "Economía", "Educación", 
                    "Empresas", "Energía", "Finanzas", "Legal", "Manufactura",
                    "Mapeo/Geoespacial", "Medio Ambiente", 
                    "Operaciones gubernamentales", "Salud", 
                    "Seguridad pública", "Transporte", "Turismo", "Vivienda"]
            }
data_impacts = {
                "en": [
                    "Cost efficiency", "New or improved product/service", 
                    "Job growth", "Revenue growth", "Identify new opportunities", 
                    "New/improved research"],
                "es": [
                    "Eficiencia económica", 
                    "Servicios/productos nuevos o mejorados", 
                    "Crecimiento de empleo", "Crecimiento de las ganancias", 
                    "Identificación de nuevas oportunidades", 
                    "Nuevas / mejoradas Investigaciones"]
            }
source_count = ['1-10', '11-50', '51-100', '101+']
full_time_employees = [
                    '1-10', '11-50', '51-200', '201-500', '501-1,000', 
                    '1,001-5,000', '5,001-10,000', '10,001+']

states ={ 
            "us": {
                "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", 
                "AR": "Arkansas", "CA": "California", "CO": "Colorado", 
                "CT": "Connecticut", "DE": "Delaware", "DC": "District of Columbia", 
                "FL": "Florida", "GA": "Georgia", "HI": "Hawaii", "ID": "Idaho", 
                "IL": "Illinois", "IN": "Indiana", "IA": "Iowa", "KA": "Kansas", 
                "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", 
                "MD": "Maryland", "MA": "Massachusetts", "MI": "Michigan", 
                "MN": "Minnesota", "MS": "Mississippi", "MO": "Missouri", 
                "MT": "Montana", "NE": "Nebraska", "NV": "Nevada", 
                "NH": "New Hampshire", "NJ": "New Jersey", "NM": "New Mexico", 
                "NY": "New York", "NC": "North Carolina", "ND": "North Dakota", 
                "OH": "Ohio", "OK": "Oklahoma", "OR": "Oregon", 
                "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina", 
                "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", 
                "UT": "Utah", "VT": "Vermont", "VA": "Virginia", "WA": "Washington", 
                "WV": "West Virginia", "WI": "Wisconsin", "WY": "Wyoming", 
                "PR": "Puerto Rico"},
            "mx": {
                "AS":"Aguascalientes", "BC":"Baja California", 
                "BS":"Baja California Sur", "CC":"Campeche", "CS":"Chiapas", 
                "CH":"Chihuahua", "CL":"Coahuila", "CM":"Colima", 
                "DF":"Distrito Federal", "DG":"Durango", "GT":"Guanajuato", 
                "GR":"Guerrero", "HG":"Hidalgo", "JC":"Jalisco", 
                "MC":"Estado de México", "MN":"Michoacán", "MS":"Morelos", 
                "NT":"Nayarit", "NL":"Nuevo León", "OC":"Oaxaca", "PL":"Puebla", 
                "QT":"Querétaro", "QR":"Quintana Roo", "SP":"San Luis Potosí", 
                "SL":"Sinaloa", "SR":"Sonora", "TC":"Tabasco", "TS":"Tamaulipas", 
                "TL":"Tlaxcala", "VZ":"Veracruz", "YN":"Yucatán", "ZS":"Zacatecas"},
            "au": {
                "ACT":"Australian Capital Territory", "NSW":"New South Wales", 
                "NT":"Northern Territory", "QLD":"Queensland", 
                "SA":"South Australia", "TAS":"Tasmania", "VIC":"Victoria", 
                "WA":"Western Australia"}
        }
stateListAbbrev = { 
            "us": [
                "", "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "DC", "FL", 
                "GA", "HI", "ID", "IL", "IN", "IA", "KA", "KY", "LA", "ME", "MD", 
                "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", 
                "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", 
                "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY", "PR"],
            "ca": [
                "", "AB", "BC", "MB", "NB", "NL", "NT", "NS", "NU", "ON", "PE", 
                "QC", "SK", "YT"],
            "au": [
                "", "ACT", "NSW", "NT", "QLD", "SA", "TAS", "VIC", "WA"],
            "mx": [
                "", "AS", "BC", "BS", "CC", "CS", "CH", "CL", "CM", "DF", "DG", 
                "MC", "GT", "GR", "HG", "JC", "MN", "MS", "NT", "NL", "OC", "PL", 
                "QT", "QR", "SP", "SL", "SR", "TC", "TS", "TL", "VZ", "YN", "ZS"]
            }
stateList = {
            "us": [
                "(Select State)", "Alabama", "Alaska", "Arizona", "Arkansas", 
                "California", "Colorado", "Connecticut", "Delaware", 
                "District of Columbia", "Florida", "Georgia", "Hawaii", "Idaho", 
                "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", 
                "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", 
                "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", 
                "New Hampshire", "New Jersey", "New Mexico", "New York", 
                "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", 
                "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", 
                "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", 
                "West Virginia", "Wisconsin", "Wyoming", "Puerto Rico"],
            "ca": [
                "(Select Province/Territory)", "Alberta", "British Columbia", 
                "Manitoba", "New Brunswick", "Newfoundland and Labrador", 
                "Northwest Territories", "Nova Scotia", "Nunavut", "Ontario", 
                "Prince Edward Island", "Quebec", "Saskatchewan", "Yukon"],
            "au": [
                "(Select Province/Territory)", "Australian Capital Territory", 
                "New South Wales", "Northern Territory", "Queensland", 
                "South Australia", "Tasmania", "Victoria", "Western Australia"],
            "mx": [
                "(Seleccione un Estado)", "Aguascalientes", "Baja California", 
                "Baja California Sur", "Campeche", "Chiapas", "Chihuahua", 
                "Coahuila", "Colima", "Distrito Federal", "Durango", 
                "Estado de México", "Guanajuato", "Guerrero", "Hidalgo", 
                "Jalisco", "Michoacán", "Morelos", "Nayarit", "Nuevo León", 
                "Oaxaca", "Puebla", "Querétaro", "Quintana Roo", 
                "San Luis Potosí", "Sinaloa", "Sonora", "Tabasco", "Tamaulipas", 
                "Tlaxcala", "Veracruz", "Yucatán", "Zacatecas"]
            }
agency_types = ['Federal','State','City/County','University/Institution']
available_countries = ["us", "au", "mx"]
country_keys = { 
    "us":"United States", "au":"Australia", "United States":"us", 
    "Australia":"au",  "Mexico":"mx", "mx":"Mexico"}
company_fields = [
    'companyName', 'url', 'yearFounded', 'city', 'state', 'zipCode', 
    'description', 'descriptionShort', 'financialInfo', 'notes']
company_fields_checkboxes = ['revenueSource', 'businessModel', 'socialImpact']
company_fields_radio = ['companyCategory', 'companyType', 'fte']
company_contact_fields = ['firstName', 'lastName', 'title', 'email', 'phone']
company_data_fields = ['sourceCount', 'dataComments', 'exampleUses']
company_admin_booleans = [
    'display', 'submittedSurvey','vetted', 'vettedByCompany', 
    'submittedThroughWebsite', 'locked']

class Tools(object):
    def re_do_filters(self, country):
        companies = models.Company.objects(country=country).only(
            'companyCategory', 'state', 'agencies', 
            'submittedSurvey', 'filters')
        for c in companies:
            filters = []
            filters.append(self.prettify(c.companyCategory))
            filters.append(c.state)
            filters += [a.prettyName for a in c.agencies]
            if c.submittedSurvey:
                filters.append("survey-company")
            c.filters = filters
            c.save()
        logging.info("Filters Redone.")

    @classmethod
    def re_do_company_filter(self, id):
        try: 
            c = models.Company.objects(id=bson.objectid.ObjectId(id)).only(
                'companyCategory', 'state', 'agencies', 
                'submittedSurvey', 'filters').first()
        except Exception, e:
            logging.info("Error creating filter: " + str(e))
            return
        filters = []
        filters.append(self.prettify(c.companyCategory))
        filters.append(c.state)
        filters += [a.prettyName for a in c.agencies]
        if c.submittedSurvey:
            filters.append("survey-company")
        return filters

    @classmethod
    def prettify(self, name):
        return re.sub(r'([^\s\w])+', '', name).replace(" ", "-").lower()

    def get_list_of_agencies(self, country):
        agencies = models.Agency.objects(country=country).only(
            'name', 'abbrev', 'subagencies.name', 'subagencies.abbrev')
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
                    label = [
                        a.name, " (", a.abbrev, ")", 
                        " - ", s.name, 
                        " (", s.abbrev, ")"]
                    agency = {
                        "label": ''.join(filter(None, label)),
                        "a": a.name,
                        "aa": a.abbrev,
                        "s": s.name,
                        "ss": s.abbrev
                    }
                    agency_list.append(agency)
        return agency_list

    def states_for_map(self, country):
        stats = models.Stats.objects.get(country=country)
        #abbrev, STATE, VALUE
        state_counts = []
        state_data = []
        for s in stats.states:
            state_data.append({
                "abbrev":s.abbrev.encode('utf-8'),
                "STATE":s.name.encode('utf-8'),
                "VALUE":s.count
            })
        return state_data


class Form(object):
    def create_new_company(self, arguments):
        company = models.Company(
            companyName = arguments['companyName'],
            state = arguments['state'],
            country = country_keys[arguments['country']])
        company.save()
        return company

    def process_company_data_info(self, arguments, id):
        try: 
            c = models.Company.objects.get(id=bson.objectid.ObjectId(id))
        except Exception, e:
            logging.info("Error processing company: " + str(e))
            return
        #-------------------DATA INFO---------------
        for item in company_data_fields:
            if item in arguments:
                models.Company.objects(
                    id=bson.objectid.ObjectId(id)).update(
                        **{'set__'+item:arguments[item]})
        #DATA TYPES
        if 'dataTypes' in arguments:
            c.dataTypes = [] if not arguments['dataTypes'] else arguments['dataTypes'].split(',')
            if 'Other' in c.dataTypes:
                del c.dataTypes[c.dataTypes.index('Other')]
                c.dataTypes.append(arguments['otherDataType'])
        else:
            c.dataTypes = []
        if 'dataImpacts' in arguments:
            c.dataImpacts = [] if not arguments['dataImpacts'] else arguments['dataImpacts'].split(',')
            if 'Other' in c.dataImpacts:
                del c.dataImpacts[c.dataImpacts.index('Other')]
                c.dataImpacts.append(arguments['otherdataImpacts'])
        c.lastUpdated = datetime.now()
        c.filters = Tools().re_do_company_filter(c.id)
        c.save()


    def process_company(self, arguments, id):
        try: 
            c = models.Company.objects.get(id=bson.objectid.ObjectId(id))
        except Exception, e:
            logging.info("Error processing company: " + str(e))
            return
        #-------------------CONTACT INFO---------------
        for item in company_contact_fields:
            if item in arguments:
                models.Company.objects(id=bson.objectid.ObjectId(id)).update(**{'set__contact__'+item:arguments[item]})
        #-------------------TEXTFIELDS---------------
        for item in company_fields:
            if item in arguments:
                models.Company.objects(id=bson.objectid.ObjectId(id)).update(**{'set__'+item:arguments[item]})
        c.prettyName = Tools.prettify(c.companyName)
        c.country = country_keys[arguments['country']]
        #-------------------CHECKBOXES---------------
        for item in company_fields_checkboxes:
            if item in arguments:
                models.Company.objects(id=bson.objectid.ObjectId(id)).update(**{'set__'+item:arguments[item].split(',')})
                if 'Other' in arguments[item]:
                    models.Company.objects(id=bson.objectid.ObjectId(id)).update(**{'pull__'+item:'Other'})
                    models.Company.objects(id=bson.objectid.ObjectId(id)).update(**{'push__'+item:arguments['other'+item]})
            else:
                models.Company.objects(id=bson.objectid.ObjectId(id)).update(**{'set__'+item:[]})
        #-------------------RADIO BUTTONS---------------
        for item in company_fields_radio:
            if item in arguments:
                if arguments[item] == 'Other':
                    models.Company.objects(id=bson.objectid.ObjectId(id)).update(**{'set__'+item:arguments['other' +item]})
                else:
                    models.Company.objects(id=bson.objectid.ObjectId(id)).update(**{'set__'+item:arguments[item]})
            else:
                models.Company.objects(id=bson.objectid.ObjectId(id)).update(**{'set__'+item:''})
        c.filters = Tools.re_do_company_filter(id)
        #-------------------BOOLEANS---------------
        for item in company_admin_booleans:
            if item in arguments:
                models.Company.objects(id=bson.objectid.ObjectId(id)).update(**{'set__'+item:arguments[item]})
        #-------------------SAVE---------------
        c.lastUpdated = datetime.now()
        c.filters = Tools().re_do_company_filter(c.id)
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
        company.lastUpdated = datetime.now()
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
        stats = models.Stats.objects(country=country).only('states').first()
        companies  = models.Company.objects(
            Q(display=True) & 
            Q(country=country)).only('state')
        total_states = Counter([c.state for c in companies])
        stats.states = []
        for key in states[country]:
            s = models.States(
                name= states[country][key],
                abbrev = key,
                count = total_states[key] if key in total_states else 0
            )
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
                "yearFounded": c.yearFounded,
                "city": c.city,
                "state": c.state,
                "country": c.country,
                "zipCode": c.zipCode,
                "fte": c.fte,
                "companyType": c.companyType,
                "companyCategory": c.companyCategory,
                "revenueSource": c.revenueSource,
                "businessModel": c.businessModel,
                'socialImpact': c.socialImpact,
                "description": c.description,
                "descriptionShort": c.descriptionShort,
                "sourceCount": c.sourceCount,
                "dataTypes": c.dataTypes,
                "exampleUses": c.exampleUses,
                "dataImpacts": c.dataImpacts,
                "lastUpdated": c.lastUpdated,
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
            'year_founded',
            'city',
            'state',
            'country',
            'zip_code',
            'full_time_employees',
            'company_type',
            'company_category',
            'revenue_source',
            'business_model',
            'social_impact',
            'description',
            'description_short',
            'source_count',
            'data_types',
            'example_uses',
            'data_impacts',
            'financial_info',
            'last_updated'
            ])
        for c in companies:
            newrow = [
                c.prettyName,
                c.companyName,
                c.url,
                c.yearFounded,
                c.city,
                c.state,
                c.country,
                c.zipCode,
                c.fte,
                c.companyType,
                c.companyCategory,
                ', '.join(c.revenueSource),
                ', '.join(c.businessModel),
                ', '.join(c.socialImpact),
                c.description,
                c.descriptionShort,
                c.sourceCount,
                ', '.join(c.dataTypes),
                c.exampleUses,
                c.dataImpacts,
                c.financialInfo,
                c.lastUpdated
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
            'contact_first_name',
            'contact_last_name',
            'contact_title',
            'contact_email',
            'contact_phone',
            'city',
            'state',
            'country',
            'zip_code',
            'year_founded',
            'full_time_employees',
            'company_type',
            'company_category',
            'revenue_source',
            'business_model',
            'social_impact',
            'description',
            'description_short',
            'financial_info',
            'source_count',
            'data_types',
            'data_comments',
            'example_uses',
            'data_impacts',
            'ts',
            'last_updated',
            'display',
            'survey_submitted',
            'vetted',
            'vettedByCompany',
            'submitted_through_website',
            'locked',
            'notes'
            ])
        for c in companies:
            newrow = [
                c.prettyName,
                c.companyName,
                c.url,
                c.contact.firstName,
                c.contact.lastName,
                c.contact.title,
                c.contact.email,
                c.contact.phone,
                c.city,
                c.state,
                c.country,
                c.zipCode,
                c.yearFounded,
                c.fte,
                c.companyType,
                c.companyCategory,
                ', '.join(c.revenueSource),
                ', '.join(c.businessModel),
                ', '.join(c.socialImpact),
                c.description,
                c.descriptionShort,
                c.financialInfo,
                c.sourceCount,
                ', '.join(c.dataTypes),
                c.dataComments,
                c.exampleUses,
                c.dataImpacts,
                c.ts,
                c.lastUpdated,
                c.display,
                c.submittedSurvey,
                c.vetted,
                c.vettedByCompany,
                c.submittedThroughWebsite,
                c.locked,
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
            'used_by_fte',
            'dataset_name',
            'dataset_url'
            ])
        index_of_companies = {}
        for c in companies:
            index_of_companies[str(c.id)] = [c.companyName, c.companyCategory, c.fte]
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
                        index_of_companies[str(d.usedBy.id)][2],
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
                            index_of_companies[str(d.usedBy.id)][2],
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
                            index_of_companies[str(c.id)][2],
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
                            index_of_companies[str(c.id)][2],
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
                    if c.companyCategory in categories['en']['us'] and c.companyCategory not in used_agencies_categories:
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
                    if c.companyCategory in categories['en']['us']: 
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


    def generate_mex_chord_chart(self, country):
        agencies = models.Agency.objects(Q(usedBy__not__size=0) & Q(country="mx")).order_by('name')
        #get agencies that are used
        used_agencies_categories = []
        for a in agencies:
            if a.usedBy:
                used_agencies_categories.append(a.name)
        #Keep track of # of categories
        num_agencies = len(used_agencies_categories)
        #get categories that are actually used from agencies that are used
        for a in agencies:
            if a.usedBy:
                for c in a.usedBy:
                    if c.companyCategory in categories['es']['mx'] and c.companyCategory not in used_agencies_categories:
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
            for c in a.usedBy:
                if c.companyCategory in categories['es']['mx']: 
                    matrix[name_key[c.companyCategory], name_key[a.name]] += 1
                    matrix[name_key[a.name], name_key[c.companyCategory]] += 1
        #make json
        matrix = matrix.tolist()
        data = {"matrix":matrix, "names":key_name, "num_agencies":num_agencies}
        #abbreviate some stuff
        for key in data['names']:
            data['names'][key] = data['names'][key].replace('Instituto', 'Inst.')
            data['names'][key] = data['names'][key].replace('Secretaría'.decode('utf-8'), 'Sec.')
        #save to file
        with open(os.path.join(os.path.dirname(__file__), 'static') + '/files/mx_matrix.json', 'w') as outfile:
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



















