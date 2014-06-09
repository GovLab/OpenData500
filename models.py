#!/usr/bin/env python
# -*- coding: utf8 -*- 
import os, sys
from mongoengine import *
from datetime import datetime


class Person2(EmbeddedDocument):
	firstName = StringField()
	lastName = StringField()
	title = StringField()
	email = StringField()
	phone = StringField()
	org = StringField()
	contacted = BooleanField()

class Company(Document):
	companyName = StringField()
	prettyName = StringField()
	url = StringField()
	contact = EmbeddedDocumentField(Person2)
	ceo = EmbeddedDocumentField(Person2)
	yearFounded = IntField()
	previousName = StringField()
	city = StringField()
	state = StringField()
	country = StringField()
	zipCode = StringField()
	fte = IntField()
	companyType = StringField() #Public, Private, etc
	companyCategory = StringField() #Categories
	revenueSource = ListField(StringField()) #checkbox with options
	description = StringField()
	descriptionShort = StringField()
	financialInfo = StringField() #long question, write paragraph
	datasetWishList = StringField() #What datasets...
	sourceCount = StringField() #From how many sources does your company use data?
	dataComments = StringField() #Please give comments, good or bad....
	confidentiality = StringField() #What info does the contact want to hide?
	agencies = ListField(ReferenceField('Agency'))
	ts = ComplexDateTimeField(default=datetime.now())
	lastUpdated = ComplexDateTimeField()
	display = BooleanField() #Display on site
	submittedSurvey = BooleanField()
	vetted = BooleanField() #vetted by us
	vettedByCompany = BooleanField() #vetted by them
	submittedThroughWebsite = BooleanField() #submitted through website
	locked = BooleanField() #Locked from public editing
	notes = StringField() #notes by admin
	filters = ListField(StringField()) #Filters for the full list page. 

	@queryset_manager
	def objects(doc_cls, queryset):
		return queryset.order_by('prettyName')

class Agency(Document):
	ts = ComplexDateTimeField(default=datetime.now())
	name = StringField()
	abbrev = StringField()
	prettyName = StringField()
	url = StringField() #for whatever is more specific, agency or subagency
	source = StringField() #DATA.GOV WEBSITE OR USER INPUT
	subagencies = ListField(EmbeddedDocumentField('Subagency'))
	dataType = StringField() #Federal, State, City/County, Other
	datasets = ListField(EmbeddedDocumentField('Dataset'))
	country = StringField()
	usedBy = ListField(ReferenceField(Company))
	usedBy_count = IntField()
	notes = StringField()

class Subagency(EmbeddedDocument):
	name = StringField()
	abbrev = StringField()
	url = StringField()
	datasets = ListField(EmbeddedDocumentField('Dataset'))
	usedBy = ListField(ReferenceField(Company))

class Dataset(EmbeddedDocument):
	datasetName = StringField()
	datasetURL = StringField()
	rating = IntField()
	usedBy = ReferenceField(Company)

class Users(Document):
	ts = ComplexDateTimeField(default=datetime.now())
	username = StringField()
	password = StringField()
	country = StringField()

class States(EmbeddedDocument):
	name = StringField()
	abbrev = StringField()
	count = IntField()

class Stats(Document):
	lastUpdate = ComplexDateTimeField()
	totalCompanies = IntField() #total
	totalCompaniesWeb = IntField() #submitted through web survey
	totalCompaniesSurvey = IntField() #completed surveys
	states = ListField(EmbeddedDocumentField(States))
	country = StringField()

class Visit(Document):
	ts = ComplexDateTimeField(default=datetime.now())
	r = StringField() #referer
	p = StringField() #page
	ua = StringField() #userAgent
	ip = StringField()



# Dataset.register_delete_rule(Company, "datasets", PULL)
# Dataset.register_delete_rule(Person, "submittedDatasets", PULL)
# Company.register_delete_rule(Dataset, "usedBy", PULL)
# Company.register_delete_rule(Person, "submittedCompany", PULL)
# Person.register_delete_rule(Company, "contact", NULLIFY)
# Person.register_delete_rule(Company, "ceo", NULLIFY)

Agency.register_delete_rule(Company, "agencies", PULL)
# Company.register_delete_rule(Dataset, 'usedBy', NULLIFY)
# Company.register_delete_rule(Subagency, 'usedBy', PULL)
Company.register_delete_rule(Agency, 'usedBy', PULL)




