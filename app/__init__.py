from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

# General flask and DB setup
app = Flask(__name__)
app.config["SECRET_KEY"] = "hfds98fuzausaujfs7f/HD(dVbQ3pVr7H"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data/rnsm.db"
db = SQLAlchemy(app)

# HTTP Authentication setup
auth = HTTPBasicAuth()
users = {
    "rnsm-admin": generate_password_hash("rnsm"),
}


@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username


from app import routes
