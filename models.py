#!/usr/bin/env python
# -*- coding: utf8 -*- 
import os, sys
from mongoengine import *
from datetime import datetime

class Person(Document):
	firstName = StringField()
	lastName = StringField()
	title = StringField()
	personType = StringField() #submitter, company contact, company CEO?
	email = StringField()
	phone = StringField()
	org = StringField()
	contacted = StringField()
	otherInfo = StringField()
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
	ratings = ListField(EmbeddedDocumentField('Rating'))
	dataType = ListField(StringField())
	usedBy = ListField(ReferenceField('Company'))

class Company(Document):
	ts = ComplexDateTimeField(default=datetime.now())
	companyName = StringField()
	url = StringField()
	ceo = ReferenceField(Person)
	submitter = ReferenceField(Person)
	yearFounded = IntField()
	previousName = StringField()
	fte = IntField()
	companyType = StringField()
	companyFunction = StringField()
	criticalDataTypes = ListField(StringField())
	datasets = ListField(ReferenceField(Dataset))
	revenueSource = ListField(StringField())
	sector = ListField(StringField())
	descriptionLong = StringField()
	descriptionShort = StringField()
	socialImpact = StringField()
	financialInfo = StringField()
	vetted = BooleanField()


Dataset.register_delete_rule(Company, "datasets", PULL)
Dataset.register_delete_rule(Person, "submittedDatasets", PULL)
Company.register_delete_rule(Dataset, "usedBy", PULL)
Company.register_delete_rule(Person, "submittedCompany", NULLIFY)