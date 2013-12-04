#!/usr/bin/env python
# -*- coding: utf8 -*- 
import os, sys
from mongoengine import *
from datetime import datetime

class Person(Document):
	firstName = StringField()					#String limit to 35 characters	#Required
	lastName = StringField()					#String limit to 35 characters	#Required
	title = StringField()						#String limit to 35 characters	#Required
	personType = StringField() 					#Assigned automatically: Submitter, Recommender, CEO, Contact
	email = StringField()						#Valid email					#Required
	phone = StringField()						#Valid Phone Num				#NOT Required
	org = StringField()							#Character limit to 100 char 	#NOT Required
	contacted = BooleanField()					#BooleanField 					#NOT Required
	otherInfo = ListField(StringField())
	datasetWishList = StringField()												#NOT Required
	companyRec = StringField()													#NOT Required
	conferenceRec = StringField()												#NOT Required
	submittedCompany = ListField(ReferenceField('Company'))							#Required (Entered below)
	submittedDatasets = ListField(ReferenceField('Dataset'))					#Required (Entered below)

class Rating(EmbeddedDocument):
	author = ReferenceField(Person)				
	rating = IntField()							#Integer, from 1 to 5			#Required
	reason = StringField()						#Max 300 characters				#NOT Required

class Dataset(Document):
	ts = ComplexDateTimeField(default=datetime.now())
	datasetName = StringField()					#String limit to 100 characters	#Required
	datasetURL = StringField()					#Valid URL 						#Required
	ratings = ListField(EmbeddedDocumentField('Rating'))
	dataType = ListField(StringField())											#Required
	usedBy = ListField(ReferenceField('Company'))

class Company(Document):
	ts = ComplexDateTimeField(default=datetime.now())
	companyName = StringField()					#String limit 70				#Required
	url = StringField()							#Valid URL 						#Required
	ceo = ReferenceField(Person)				#Person, see above				#NOT Required
	#submitter = ReferenceField(Person)			#Person, see above				#Required
	recommendedBy = ReferenceField(Person)
	recommended = BooleanField()				#Recommended or Submitted?
	yearFounded = IntField()					#Valid year Integer				#NOT Required
	previousName = StringField()				#String limit 70				#NOT Required
	city = StringField()						#String, limit 80 chars?		#NOT Required
	zipCode = IntField()						#Int, 5 Digits					#NOT Required
	fte = IntField()							#Integer, 0-1,000,000			#NOT Required
	companyType = StringField()													#Required
	companyFunction = StringField()												#Required
	criticalDataTypes = ListField(StringField())								#Required
	datasets = ListField(ReferenceField(Dataset))								#Required, see above
	revenueSource = ListField(StringField())									#Required
	sector = ListField(StringField())											#Required
	descriptionLong = StringField()				#70 words						#Required
	descriptionShort = StringField()			#25 words						#Required
	socialImpact = StringField()				#70 words						#NOT Required
	financialInfo = StringField()				#70 words						#NOT Required
	vetted = BooleanField()						#Automatic set to False
	vettedByCompany = BooleanField()
	submitType = StringField()
	contact = ReferenceField(Person)
	reasonForRecommending = StringField()


Dataset.register_delete_rule(Company, "datasets", PULL)
Dataset.register_delete_rule(Person, "submittedDatasets", PULL)
Company.register_delete_rule(Dataset, "usedBy", PULL)
Company.register_delete_rule(Person, "submittedCompany", PULL)








