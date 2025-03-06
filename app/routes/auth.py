import sqlite3

from flask import render_template, request, url_for, redirect, session
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from connection import get_db_connection
from app import app, login_manager
from ..models import User


@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    curs = conn.cursor()
    curs.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = curs.fetchone()
    conn.close()

    if user:
        return User(user_id=user[0], username=user[1], password=user[2])
    return None

@app.get("/login/")
def get_login():
    return render_template("login.html")

@app.post("/login/")
def post_login():
    username = request.form["username"].strip()
    password = request.form["password"].strip()

    if not all([username, password]):
        return render_template("login.html", error_message="All fields are required")

    conn = get_db_connection()
    curs = conn.cursor()
    curs.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = curs.fetchone()
    conn.close()

    if not user:
        return render_template("login.html", error_message="User not found")
        
    if not check_password_hash(user[2], password):
        return render_template("login.html", error_message="Invalid password")
        
    user_obj = User(user_id=user[0], username=user[1], password=user[2])
    login_user(user_obj, remember=True)
    session["username"] = user[1]      #?  Load Session username  
    session["password"] = password      #?  Load Session password 

    return redirect(url_for("get_games"))

@app.get("/signup/")
def get_signup():
    return render_template("signup.html")

@app.post("/signup/")
def post_signup():
    username = request.form["username"].strip()
    password = request.form["password"].strip()
    confirm_password = request.form["confirm-password"].strip()
    terms_accepted = request.form.get("terms")

    if not all([username, password, terms_accepted]):
        return render_template("signup.html", error_message="All fields are required and terms must be accepted")
    
    if password != confirm_password:
        return render_template("signup.html", error_message="Passwords do not match")

    if len(username) < 3 or len(username) > 20:
        return render_template("signup.html", error_message="Username must be between 3 and 20 characters")

    if len(password) < 5:
        return render_template("signup.html", error_message="Password must be at least 6 characters long")

    conn = get_db_connection()
    curs = conn.cursor()
    curs.execute("SELECT * FROM users WHERE username = ?", (username,))
    existing_user = curs.fetchone()

    if existing_user:
        conn.close()
        if existing_user[1] == username:
            return render_template("signup.html", error_message="Username already exists")

    hashed_password = generate_password_hash(password)
    curs.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                (username, hashed_password))
    conn.commit()
    user_id = curs.lastrowid

    curs.execute("""INSERT INTO profile (user_id, photo, description, favorite_games) #? Load profile talbe data
                VALUES (?, ?, ?, ?)""", 
                (user_id, "", "", ""))
    conn.commit()
        
    user = User(user_id=user_id, username=username, password=hashed_password)
    login_user(user)
    
    return redirect(url_for("get_login"))

@app.get("/terms/")
def get_terms():
    return render_template("terms.html")

@app.get("/logout/")
def get_logout():
    logout_user()
    session.pop("username", None)   #? Delete Session username
    session.pop("password", None)   #? Delete Session password
    return redirect(url_for("get_games"))