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
	datasetWishList = StringField()
	companyRec = StringField()
	conferenceRec = StringField()
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
	socialImpact = StringField()
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



class Users(Document):
	ts = ComplexDateTimeField(default=datetime.now())
	email = StringField()
	password = StringField()


Dataset.register_delete_rule(Company, "datasets", PULL)
Dataset.register_delete_rule(Person, "submittedDatasets", PULL)
Company.register_delete_rule(Dataset, "usedBy", PULL)
Company.register_delete_rule(Person, "submittedCompany", PULL)
Person.register_delete_rule(Company, "contact", NULLIFY)
Person.register_delete_rule(Company, "ceo", NULLIFY)








