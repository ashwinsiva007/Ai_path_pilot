import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-super-secret-key-for-dev'
    basedir = os.path.abspath(os.path.dirname(__file__))
    
    # On Vercel, use /tmp for SQLite database to prevent read-only filesystem errors
    if os.environ.get('VERCEL') == '1':
        db_path = '/tmp/app.db'
    else:
        db_path = os.path.join(basedir, 'app.db')
        
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f'sqlite:///{db_path}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
