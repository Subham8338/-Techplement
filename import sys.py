import sys
import os

# Set the path to your app directory
path = '/home/Subham83389/-Techplement/quote_app_'
if path not in sys.path:
    sys.path.append(path)

# Import your Flask app
from app import app as application  # Assumes your Flask instance is named 'app' in app.py