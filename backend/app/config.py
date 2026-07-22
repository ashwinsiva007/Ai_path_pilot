import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    basedir = os.path.abspath(os.path.dirname(__file__))
    
    # On Vercel, use /tmp for SQLite database to prevent read-only filesystem errors
    if os.environ.get('VERCEL') == '1':
        db_path = '/tmp/app.db'
    else:
        db_path = os.path.join(basedir, 'app.db')
        
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f'sqlite:///{db_path}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
