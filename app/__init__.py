
from flask import Flask
from markdown import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.extra import ExtraExtension
from micawber import bootstrap_basic, parse_html
from micawber.cache import Cache as OEmbedCache

from peewee import *
from playhouse.flask_utils import FlaskDB, get_object_or_404, object_list




app = Flask(__name__)
app.config.from_object('config')

flask_db = FlaskDB(app)
database = flask_db.database
oembed_providers = bootstrap_basic(OEmbedCache())




from app import views, models
