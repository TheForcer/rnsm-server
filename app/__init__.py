from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SECRET_KEY"] = "hfds98fuzausaujfs7f/HD(dVbQ3pVr7H"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data/rnsm.db"
db = SQLAlchemy(app)

from app import routes
