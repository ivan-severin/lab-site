import os

ADMIN_PASSWORD = 'secret'
APP_DIR = os.path.dirname(os.path.realpath(__file__))
DATABASE_MIGRATE_REPO = os.path.join(APP_DIR, 'db_repository')
DATABASE = 'sqliteext:///%s' % os.path.join(APP_DIR, 'app.db')
DEBUG = True
SECRET_KEY = 'shhh, secret!'  # Used by Flask to encrypt session cookie.
SITE_WIDTH = 800