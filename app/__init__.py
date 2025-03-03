import os
from datetime import timedelta

from flask import Flask
from flask_login import LoginManager
from flask_compress import Compress
from flask_session import Session
from flask_swagger_ui import get_swaggerui_blueprint

from connection import create_tables


app = Flask(__name__)
Compress(app)
login_manager = LoginManager()
login_manager.init_app(app)

SWAGGER_URL = "/swagger/"
API_URL = "/static/swagger/swagger.json"

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Torrent"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

app.config["SECRET_KEY"] = os.urandom(24)
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=30)
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = os.path.join(app.instance_path, "sessions")
Session(app)

login_manager.login_view = "get_login"
login_manager.login_message = "Please log in to access this page."

create_tables()