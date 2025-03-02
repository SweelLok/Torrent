import sqlite3
import smtplib
import random

from flask import render_template, request, url_for, redirect, session
from flask_login import login_user, login_required, logout_user, current_user

from connection import get_db_connection
from app import app, login_manager


@app.route("/send_message/", methods=['POST'])
def send_message():
    name = request.form["name"]
    email = request.form["email"]
    message = request.form["message"]
    
    send_email(email, name)
    
    return redirect(url_for("get_about"))

def send_email(from_addrs, name):
    to_addrs = "hktnadm@gmail.com"
    subject = "Welcome to Our Service."
    body = "Thank you for question! Your answer will be soon!"
    message = f"From: {name} <{from_addrs}>\nTo: {to_addrs}\nSubject: {subject}\n\n{body}"
    
    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(from_addrs, "ttnq zxtl dldo pgrc")
        server.sendmail(from_addrs, to_addrs, message)
        server.quit()
    except Exception as e:
        print("Error sending email:", e)