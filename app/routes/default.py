from flask import render_template, redirect, url_for, request, session
from flask_login import current_user, login_required

from app import app
from connection import get_db_connection


@app.get("/")
def get_start():
    if current_user.is_authenticated:
        return redirect(url_for("get_menu"))
    return redirect(url_for("get_login"))

@app.get("/about/")
def get_about():
    return render_template("about.html")

@app.get("/menu/")
@login_required
def get_menu():
    return render_template("menu.html")