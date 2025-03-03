from flask import render_template, redirect, url_for, request, session
from flask_login import current_user, login_required

from app import app
from connection import get_db_connection


@app.get("/")
def get_start():
    # return redirect(url_for("swagger_ui.show"))
    return redirect(url_for("get_games"))

@app.get("/about/")
def get_about():
    return render_template("about.html")

@app.get("/swagger/")
@login_required
def get_swagger():
    return redirect(url_for("swagger_ui.show"))