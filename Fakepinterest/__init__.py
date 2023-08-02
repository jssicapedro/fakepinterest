from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt


app = Flask(__name__, static_folder="static")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///comunidade.bd"
app.config["SECRET_KEY"] = "91079e75c7a25cd8672a"
app.config["UPLOAD_FOLDER"] = "static/img_posts"

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "homepage"
# isto faz com que o utilizador seja redirecionado para a rota homepage

from Fakepinterest import models, routes
