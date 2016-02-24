
#Mongo
from mongoengine import *
from utils import StatsGenerator, Tools, FileGenerator
import models
import csv
import utils
import os
import codecs


#Connect to mongo `export MONGOLAB_URI=$MONGOLAB_URI`
connect('db', host=os.environ.get('MONGOLAB_URI'))

csvfile = open('korea_Raw4.csv', 'rU')
reader = csv.DictReader(csvfile, dialect=csv.excel)
Form = utils.Form()

stats = StatsGenerator()

models.Company.objects(Q(country='Korea')).delete()
models.Company.objects(Q(country='kr')).delete()
models.Stats.objects(Q(country='kr')).delete()
models.Agency.objects(Q(country='kr')).delete()

# Issues:
#  * Company description is missing.  what should we show instead?
#  * Company category column has several categories, we can only show one.  Please pick one category for each company. Right now we're just showing the first listed category.

# MAX_ROWS = 10000 # CHANGE ME WHEN YOU RUN FOR REAL!!!!

output=[]
for rownum, row in enumerate(reader):
    #arguments={}
    #for i in header:
    #    arguments[i]=each[i]
    company = Form.create_new_company(arguments={
        'country': 'Korea', # this will be stored as 'kr'
        'companyName': row['company_name'].decode('utf8', errors='ignore'),
        'state': row['state'].decode('utf8', errors='ignore')
    })
    company.url = row['url'].decode('utf8', errors='ignore')
    company.yearFounded = row['year_founded'].decode('utf8', errors='ignore')
    company.city = row['city'].decode('utf8', errors='ignore')
    company.zipCode = row['zip_code'].decode('utf8', errors='ignore').zfill(5) 
    company.companyCategory = row['company_category'].decode('utf8', errors='ignore')
    company.companyType = row['company_type'].decode('utf8', errors='ignore')
    company.fte = row['full_time_employees'].decode('utf8', errors='ignore')
    company.revenueSource = row['revenue_source'].decode('utf8', errors='ignore').split(', ')
    company.businessModels = row['business_model'].decode('utf8', errors='ignore')
    company.socialImpact = row['social_impact'].decode('utf8', errors='ignore').split(', ')
    company.description = row['description'].decode('utf8', errors='ignore')
    company.prettyName = Tools.prettify(company['companyName'])
    company.filters = []

    if company.companyType.lower() == 'nonprofit':
        company.companyType = 'Non-profit'

    if company.fte == '10-Jan':
        company.fte = '1 - 10'
    elif company.fte == 'Nov-50':
        company.fte = '11 - 50'

    company.companyCategory = company.companyCategory.split(',')[0]

    agency_names = row['agencies'].decode('utf8', errors='ignore').split(', ')
    agencies = []
    for agency_name in agency_names:
        if agency_name == '':
            continue
        else:
            agency_name = agency_name.strip()
        agency = models.Agency.objects(Q(country='kr') & Q(name=agency_name)).first()
        if not agency:
            agency = models.Agency(name=agency_name,
                prettyName=Tools.prettify(agency_name),
                abbrev="",
                url="", 
                source="", 
                subagencies=[], 
                datasets=[], 
                usedBy=[], 
                notes="", 
                dataType='Federal', # only federal agencies are shown in the filter list
                country='kr')
            agency.save()
        agencies.append(agency)

    company.display = True
    company.save()

    for agency in agencies:
        Form.add_agency_to_company(company, agency)

    # if rownum > MAX_ROWS:
    #     break

    #print u'saved: {}'.format(company.companyName)
# print output

stats.create_new_stats('kr')
stats.refresh_stats('kr')
Tools().re_do_filters('kr')
FileGenerator().generate_company_csv('kr')
FileGenerator().generate_company_all_csv('kr')
FileGenerator().generate_agency_csv('kr')
FileGenerator().generate_chord_chart_files('kr','en')
