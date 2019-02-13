import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
#app.config.from_json('config.json')
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///artlantis.db'
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
#app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_USERNAME'] = "shanelwolfram@gmail.com"
#app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
app.config['MAIL_PASSWORD'] = "Cefroth88"
mail = Mail(app)

from artlantis.views.main import main
from artlantis.views.auth import auth
from artlantis.views.account import account
from artlantis.views.thread import thread

app.register_blueprint(main)
app.register_blueprint(auth)
app.register_blueprint(account)
app.register_blueprint(thread)