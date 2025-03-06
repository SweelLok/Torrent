import os
from datetime import timedelta

from flask import Flask
from flask_login import LoginManager
from flask_compress import Compress
from flask_session import Session

from connection import create_tables


app = Flask(__name__)           #? Flask configuration
Compress(app)
login_manager = LoginManager()
login_manager.init_app(app)

app.config["SECRET_KEY"] = os.urandom(24)                           #? Session configuration
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=30)
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = os.path.join(app.instance_path, "sessions")
Session(app)

login_manager.login_view = "get_login"                                  #? Login configuration
login_manager.login_message = "Please log in to access this page."

create_tables()