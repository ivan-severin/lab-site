import os

ADMIN_PASSWORD = 'secret'
APP_DIR = os.path.dirname(os.path.realpath(__file__))
# DATABASE_MIGRATE_REPO = os.path.join(APP_DIR, 'db_repository')
SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % os.path.join(APP_DIR, 'app.db')


DEBUG = True
SECRET_KEY = 'shhh, secret!'  # Used by Flask to encrypt session cookie.
SITE_WIDTH = 800


# After 'Create app'
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = 'rice.main.office@gmail.com'
MAIL_PASSWORD = 'cosmos2016'
MAIL_DEFAULT_SENDER = 'rice.main.office@gmail.com'