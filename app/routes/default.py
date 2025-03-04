from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_required

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
    if current_user.username == "root" and current_user.password == "@dm1n":
        return redirect(url_for("swagger_ui.show"))
    else:
        flash("You are not an admin!")
        return redirect(url_for("get_games"))