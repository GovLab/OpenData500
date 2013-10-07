#!/usr/bin/env python
# -*- coding: utf8 -*- 
import os, sys
from mongoengine import *

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

class DataSet(EmbeddedDocument):
	name = StringField()
	url = StringField()
	rating = IntField()
	reason = StringField()
	dataType = StringField()

class Company(Document):
	companyName = StringField()
	url = StringField()
	ceo = EmbeddedDocumentField(Person)
	submitter = EmbeddedDocumentField(Person)
	yearFounded = IntField()
	previousName = StringField()
	FTE = IntField()
	companyType = StringField()
	companyFunction = StringField()
	criticalDataTypes = ListField(StringField())
	dataSets = ListField(EmbeddedDocumentField(DataSet))
	revenueSource = ListField(StringField())
	sector = StringField()
	descriptionLong = StringField()
	descriptionShort = StringField()
	socialImpact = StringField()
	financialInfo = StringField()
	vetted = BooleanField()
