#!/usr/bin/env python
# -*- coding: utf8 -*- 
import os, sys
from mongoengine import *
from datetime import datetime

class Person(Document):
	ts = ComplexDateTimeField(default=datetime.now())
	firstName = StringField()
	lastName = StringField()
	title = StringField()
	personType = StringField()
	email = StringField()
	phone = StringField()
	org = StringField()
	contacted = BooleanField()
	otherInfo = ListField(StringField())
	datasetWishList = StringField() #DEPRECATED
	companyRec = StringField() #DEPRECATED
	conferenceRec = StringField() #DEPRECATED
	submittedCompany = ReferenceField('Company')
	submittedDatasets = ListField(ReferenceField('Dataset'))

class Rating(EmbeddedDocument):
	author = ReferenceField(Person)				
	rating = IntField()
	reason = StringField()

class Dataset(Document):
	ts = ComplexDateTimeField(default=datetime.now())
	datasetName = StringField()
	datasetURL = StringField()
	agency = StringField()
	ratings = ListField(EmbeddedDocumentField('Rating'))
	dataType = ListField(StringField())
	usedBy = ListField(ReferenceField('Company'))

class Company(Document):
	companyName = StringField()
	prettyName = StringField()
	url = StringField()
	ceo = ReferenceField(Person)
	yearFounded = IntField()
	previousName = StringField()
	city = StringField()
	state = StringField()
	zipCode = IntField()
	fte = IntField()
	companyType = StringField()
	companyCategory = StringField()
	companyFunction = StringField()
	criticalDataTypes = ListField(StringField())
	revenueSource = ListField(StringField())
	sector = ListField(StringField())
	descriptionLong = StringField()
	descriptionShort = StringField()
	socialImpact = StringField() #DEPRECATED
	financialInfo = StringField()
	confidentiality = StringField() #What info does the contact want to hide?
	contact = ReferenceField(Person)
	recommendedBy = ReferenceField(Person) #DEPRECATED
	recommended = BooleanField() #DEPRECATED
	reasonForRecommending = StringField() #DEPRECATED
	datasets = ListField(ReferenceField(Dataset))
	ts = ComplexDateTimeField(default=datetime.now())
	preview50 = BooleanField() #Soon to be DEPRECATED
	display = BooleanField() #Changed Name to Display
	submittedSurvey = BooleanField()
	vetted = BooleanField() #vetted by us
	vettedByCompany = BooleanField() #vetted by them
	submittedThroughWebsite = BooleanField() #submitted through website

class Person2(EmbeddedDocument):
	firstName = StringField()
	lastName = StringField()
	title = StringField()
	email = StringField()
	phone = StringField()
	org = StringField()
	contacted = BooleanField()

class Company2(Document):
	companyName = StringField()
	prettyName = StringField()
	url = StringField()
	contact = EmbeddedDocumentField(Person2)
	ceo = EmbeddedDocumentField(Person2)
	yearFounded = IntField()
	previousName = StringField()
	city = StringField()
	state = StringField()
	zipCode = IntField()
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
	datasets = ListField(EmbeddedDocumentField('Dataset2'))
	usedBy = ListField(ReferenceField(Company2))

class Subagency(EmbeddedDocument):
	name = StringField()
	abbrev = StringField()
	url = StringField()
	datasets = ListField(EmbeddedDocumentField('Dataset2'))
	usedBy = ListField(ReferenceField(Company2))

class Dataset2(EmbeddedDocument):
	datasetName = StringField()
	datasetURL = StringField()
	rating = IntField()
	usedBy = ReferenceField(Company2)

class Users(Document):
	ts = ComplexDateTimeField(default=datetime.now())
	email = StringField()
	password = StringField()

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



Dataset.register_delete_rule(Company, "datasets", PULL)
Dataset.register_delete_rule(Person, "submittedDatasets", PULL)
Company.register_delete_rule(Dataset, "usedBy", PULL)
Company.register_delete_rule(Person, "submittedCompany", PULL)
Person.register_delete_rule(Company, "contact", NULLIFY)
Person.register_delete_rule(Company, "ceo", NULLIFY)

Agency.register_delete_rule(Company2, "agencies", PULL)
Company2.register_delete_rule(Agency, 'usedBy', PULL)






