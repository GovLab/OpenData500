
#Mongo
from mongoengine import *
import models
import csv
import utils
import os
import codecs


#Connect to mongo `export MONGOLAB_URI=$MONGOLAB_URI`
connect('db', host=os.environ.get('MONGOLAB_URI'))

#csvfile = codecs.open('korea.csv', 'r', encoding='utf-8', errors='strict')
csvfile = open('korea.csv', 'r')
reader = csv.DictReader( csvfile )
Form = utils.Form()

models.Company.objects(Q(country='kr')).delete()

output=[]
for row in reader:
    #arguments={}
    #for i in header:
    #    arguments[i]=each[i]
    try:
        company = Form.create_new_company(arguments={
            'country': 'Korea',
            'companyName': row['Company Name'].decode('utf8'),
            'state': row['State'].decode('utf8'),
            'comnayCategory': row['Company Category'].decode('utf8'),
            'descriptionShort': row['Company Description'].decode('utf8'),
            'agencies': row['Company Agencies'].decode('utf8')
        })
        company.display = True
        company.save()
    except UnicodeError as e:
        import pdb
        pdb.set_trace()
    #print u'saved: {}'.format(company.companyName)
# print output
