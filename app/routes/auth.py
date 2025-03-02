import sqlite3

from flask import render_template, request, url_for, redirect, session
from flask_login import login_user, login_required, logout_user, current_user

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
        return User(user_id=user[0], username=user[1], password=user[2],)
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
        
    if user[2] != password:
        return render_template("login.html", error_message="Invalid password")
        
    user_obj = User(user_id=user[0], username=user[1], password=user[2])
    login_user(user_obj, remember=True)
    return redirect(url_for("chat"))

@app.get("/signup/")
def get_signup():
    return render_template("signup.html")

@app.post("/signup/")
def post_signup():
    username = request.form["username"].strip()
    password = request.form["password"].strip()

    if not all([username, password]):
        return render_template("signup.html", error_message="All fields are required")

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

    try:
        curs.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                     (username, password))
        conn.commit()
        user_id = curs.lastrowid

        curs.execute("""INSERT INTO profile (user_id, photo, description) 
                       VALUES (?, ?, ?)""", 
                    (user_id, "", ""))
        conn.commit()
        
        user = User(user_id=user_id, username=username, password=password)
        login_user(user)
        session["user_id"] = user_id

    except sqlite3.Error as error:
        print("Error", error)
        return render_template("signup.html", error_message="Database error occurred")
    finally:
        conn.close()
    
    return redirect(url_for("get_login"))

@app.get("/logout/")
def get_logout():
    logout_user()
    return redirect(url_for("get_login"))