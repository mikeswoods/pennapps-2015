import sys, os, bottle

sys.path = ['/var/www/EmojifyThis/'] + sys.path
os.chdir( os.path.dirname(__file__))

from wa import app

application = app 
