from flask import render_template, redirect, url_for
from flask_login import login_required

from app import app


@app.get("/")
def get_start():
    return redirect(url_for("get_games"))

@app.get("/about/")
def get_about():
    return render_template("about.html")

@app.get("/swagger/")
@login_required
def get_swagger():
    return(url_for("swagger_ui.show"))