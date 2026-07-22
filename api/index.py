import sys
import os

# Add the backend directory to the Python path so it can find the app module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from app import create_app

# Vercel looks for this 'app' variable to run the Flask Serverless Function
app = create_app()
