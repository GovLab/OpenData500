source .env

HOST=$(echo $MONGOLAB_URI | cut -d '@' -f 2 | cut -d '/' -f 1)
DB=$(echo $MONGOLAB_URI | cut -d '/' -f 4)
USER=$(echo $MONGOLAB_URI | cut -d '/' -f 3 | cut -d ':' -f 1)
PASSWORD=$(echo $MONGOLAB_URI | cut -d '/' -f 3 | cut -d ':' -f 2 | cut -d '@' -f 1)

#for COLLECTION in agency company stats; do
#  mongoexport --jsonArray -h $HOST -d $DB -c $COLLECTION -u $USER -p $PASSWORD -o $COLLECTION.json
#done

ALL_COMPANY_FIELDS=companyName,prettyName,url,contact,ceo,yearFounded,city,state,country,zipCode,fte,companyType,companyCategory,revenueSource,businessModel,socialImpact,description,descriptionShort,financialInfo,sourceCount,dataTypes,dataComments,exampleUses,dataImpacts,dataWishlist,agencies,ts,lastUpdated,display,submittedSurvey,vetted,vettedByCompany,submittedThroughWebsite,locked,notes,filters
PUBLIC_COMPANY_FIELDS=companyName,prettyName,filters,descriptionShort,state,companyCategory,country,url,yearFounded,city,zipCode,fte,companyType,businessModel,revenueSource,socialImpact,sourceCount,description,agencies,display,dataTypes,exampleUses,dataImpacts,financialInfo,lastUpdated
PUBLIC_AGENCY_FIELDS=

agency_name,agency_abbrev,agency_type,subagency_name,subagency_abbrev,url,used_by,used_by_category,used_by_fte,dataset_name,dataset_url


mongoexport --jsonArray -h $HOST -d $DB -c company -u $USER -p $PASSWORD \
  -f $PUBLIC_COMPANY_FIELDS \
  -o company.json

mongoexport --jsonArray -h $HOST -d $DB -c agency -u $USER -p $PASSWORD \
  -o agency.json
  #-f $PUBLIC_AGENCY_FIELDS \

#COMPANY_FIELDS=companyName,prettyName,url,contact,ceo,yearFounded,city,state,country,zipCode,fte,companyType,companyCategory,revenueSource,businessModel,socialImpact,description,descriptionShort,financialInfo,sourceCount,dataTypes,dataComments,exampleUses,dataImpacts,dataWishlist,agencies,ts,lastUpdated,display,submittedSurvey,vetted,vettedByCompany,submittedThroughWebsite,locked,notes,filters
#
#mongoexport --csv -h $HOST -d $DB -c company -u $USER -p $PASSWORD \
#  -f $COMPANY_FIELDS -o company.csv
#
#AGENCY_FIELDS=ts,name,abbrev,prettyName,url,source,subagencies,dataType,datasets,country,usedBy,usedBy_count,notes
#mongoexport --csv -h $HOST -d $DB -c agency -u $USER -p $PASSWORD \
#  -f $AGENCY_FIELDS -o agency.csv
