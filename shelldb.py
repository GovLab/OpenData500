
from mongoengine import *
from models import *

#Connect to mongo `export MONGOLAB_URI=$MONGOLAB_URI`
connect('db', host=os.environ.get('MONGOLAB_URI'))

import pdb
pdb.set_trace()
