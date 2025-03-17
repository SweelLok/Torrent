from flask import render_template, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.security import check_password_hash

from app import app
from connection import get_db_connection


@app.get("/admin/")
@login_required
def get_admin():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))

    if current_user.username == "root" and \
       current_user.gmail == "hktnadm@gmail.com" and \
       check_password_hash(current_user.password, "@dm1n"):
        
        conn = get_db_connection()
        curs = conn.cursor()

        curs.execute("SELECT user_id, username FROM users")
        all_users = {row[0]: row[1] for row in curs.fetchall()}

        curs.execute("SELECT feedback_id, user_id, text, rating FROM feedback")
        feedbacks = [{"id": row[0], 
                      "user_id": row[1], 
                      "username": all_users.get(row[1], "Unknown"),
                      "text": row[2], 
                      "rating": row[3]} for row in curs.fetchall()]
        
        conn.close()

        return render_template("admin.html", users=all_users, feedbacks=feedbacks)

    return redirect(url_for("get_games"))