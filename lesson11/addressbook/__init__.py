#import imp
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#app.config['SECRET_KEY'] = 'your-not-pass'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///addressbookdb.db"
db = SQLAlchemy(app)

from addressbook import routes, models
