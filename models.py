#!/usr/bin/env python
# -*- coding: utf8 -*- 
import os, sys
from mongoengine import *
from datetime import datetime

class Person(EmbeddedDocument):
	firstName = StringField()
	lastName = StringField()
	title = StringField()
	personType = StringField() #submitter, company contact, company CEO?
	email = StringField()
	phone = StringField()
	reason = StringField()
	org = StringField()
	contacted = StringField()
	otherInfo = StringField()
	datasetWishList = StringField()
	companyRec = StringField()
	conferenceRec = StringField()

class Dataset(EmbeddedDocument):
	datasetName = StringField()
	datasetURL = StringField()
	rating = IntField()
	reason = StringField()
	dataType = ListField(StringField())

class Company(Document):
	ts = ComplexDateTimeField(default=datetime.now())
	companyName = StringField()
	url = StringField()
	ceo = EmbeddedDocumentField(Person)
	submitter = EmbeddedDocumentField(Person)
	yearFounded = IntField()
	previousName = StringField()
	fte = IntField()
	companyType = StringField()
	companyFunction = StringField()
	criticalDataTypes = ListField(StringField())
	datasets = ListField(EmbeddedDocumentField(Dataset))
	revenueSource = ListField(StringField())
	sector = ListField(StringField())
	descriptionLong = StringField()
	descriptionShort = StringField()
	socialImpact = StringField()
	financialInfo = StringField()
	vetted = BooleanField()
