import sys
import os

project_home = '/home/Subham8338/Techplement/quote_app_'
if project_home not in sys.path:
    sys.path.insert(0, project_home)
os.environ['FLASK_ENV'] = 'production'
from app import app as application