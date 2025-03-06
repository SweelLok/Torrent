from flask import render_template, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.security import check_password_hash

from app import app
from connection import get_db_connection


@app.get("/admin/")
@login_required
def get_admin():
    conn = get_db_connection()
    curs = conn.cursor()

    #! Take all users
    curs.execute("SELECT user_id, username FROM users")
    all_users = {row[0]: row[1] for row in curs.fetchall()}

    #! Take all feedbacks
    curs.execute("SELECT feedback_id, user_id, text, rating FROM feedback")
    feedbacks = [{"id": row[0], 
                  "user_id": row[1], 
                  "username": all_users.get(row[1], "Unknown"),
                  "text": row[2], 
                  "rating": row[3]} for row in curs.fetchall()]
    
    conn.close()

    if current_user.username == "root" and check_password_hash(current_user.password, "@dm1n"):
        return render_template("admin.html", users=all_users, feedbacks=feedbacks)
    else:
        return redirect(url_for("get_games"))
