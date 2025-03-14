import smtplib

from flask import request, url_for, redirect

from app import app


@app.route("/send_message/", methods=["POST"])
def send_message():
    name = request.form["name"]
    from_addrs = request.form["email"]
    message = request.form["message"]
    send_email(from_addrs, name, message)
    
    return redirect(url_for("get_about"))

def send_email(from_addrs, name, message):
    to_addrs = "hktnadm@gmail.com"
    subject = "Hello! This message abot your website."
    message = f"From: {name} <{from_addrs}>\nTo: {to_addrs}\nSubject: {subject}\n\n{message}"

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(from_addrs, "tjyk bunj mqqp iurk ")     #? Google tokin
    server.sendmail(from_addrs, to_addrs, message)
    server.quit()