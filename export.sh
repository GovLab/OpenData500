source .env

HOST=$(echo $MONGOLAB_URI | cut -d '@' -f 2 | cut -d '/' -f 1)
DB=$(echo $MONGOLAB_URI | cut -d '/' -f 4)
USER=$(echo $MONGOLAB_URI | cut -d '/' -f 3 | cut -d ':' -f 1)
PASSWORD=$(echo $MONGOLAB_URI | cut -d '/' -f 3 | cut -d ':' -f 2 | cut -d '@' -f 1)

for COLLECTION in agency company stats; do
  mongoexport --jsonArray -h $HOST -d $DB -c $COLLECTION -u $USER -p $PASSWORD -o $COLLECTION.json
done

#COMPANY_FIELDS=companyName,prettyName,url,contact,ceo,yearFounded,city,state,country,zipCode,fte,companyType,companyCategory,revenueSource,businessModel,socialImpact,description,descriptionShort,financialInfo,sourceCount,dataTypes,dataComments,exampleUses,dataImpacts,dataWishlist,agencies,ts,lastUpdated,display,submittedSurvey,vetted,vettedByCompany,submittedThroughWebsite,locked,notes,filters
#
#mongoexport --csv -h $HOST -d $DB -c company -u $USER -p $PASSWORD \
#  -f $COMPANY_FIELDS -o company.csv
#
#AGENCY_FIELDS=ts,name,abbrev,prettyName,url,source,subagencies,dataType,datasets,country,usedBy,usedBy_count,notes
#mongoexport --csv -h $HOST -d $DB -c agency -u $USER -p $PASSWORD \
#  -f $AGENCY_FIELDS -o agency.csv
