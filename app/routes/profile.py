import requests

from flask import render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required, logout_user

from app import app
from connection import get_db_connection
from ..config import RAWG_API_KEY, RAWG_BASE_URL


@app.get("/profile/")
@login_required
def get_profile():
    user_id = request.args.get("user_id", current_user.user_id)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT users.username, profile.photo, profile.description 
        FROM users 
        LEFT JOIN profile ON users.user_id = profile.user_id 
        WHERE users.user_id = ?""", (user_id,))
    profile = cursor.fetchone()
    
    cursor.execute("""
        SELECT game_id 
        FROM favorite_games 
        WHERE user_id = ?""", (user_id,))
    favorite_game_ids = cursor.fetchall()
    
    conn.close()
    
    if profile:
        username, photo, description = profile
    else:
        username, photo, description = current_user.username, "", ""
    
    favorite_games = []
    for game_id in favorite_game_ids:
        game_id = game_id[0]
        url = f"{RAWG_BASE_URL}/games/{game_id}?key={RAWG_API_KEY}"
        response = requests.get(url)
        if response.status_code == 200:
            game = response.json()
            favorite_games.append(game["name"])
    
    return render_template("profile.html", username=username, photo=photo, description=description, favorite_games=favorite_games)

@app.get("/edit_profile/")
@login_required
def get_edit_profile():
    user_id = request.args.get("user_id", current_user.user_id)
    if str(user_id) != str(current_user.user_id):
        return redirect(url_for("get_profile", user_id=user_id))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT users.username, profile.photo, profile.description 
        FROM users 
        LEFT JOIN profile ON users.user_id = profile.user_id 
        WHERE users.user_id = ?""", (current_user.user_id,))
    profile = cursor.fetchone()
    conn.close()

    if profile:
        username, photo, description = profile
    else:
        username, photo, description = current_user.username, "", ""
    
    return render_template("edit_profile.html", username=username, photo=photo, description=description)

@app.post("/edit_profile/")
@login_required
def post_edit_profile():
    if "user_id" in request.form and str(request.form["user_id"]) != str(current_user.user_id):
        return redirect(url_for("get_profile"))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET username = ? WHERE user_id = ?", 
                   (request.form["username"], current_user.user_id))
    cursor.execute("SELECT * FROM profile WHERE user_id = ?", (current_user.user_id,))
    profile_exists = cursor.fetchone()

    if profile_exists:
        cursor.execute("UPDATE profile SET photo = ?, description = ? WHERE user_id = ?", 
                       (request.form["photo"], request.form["description"], current_user.user_id))
    else:
        cursor.execute("INSERT INTO profile (user_id, photo, description) VALUES (?, ?, ?)", 
                       (current_user.user_id, request.form["photo"], request.form["description"]))
    conn.commit()
    conn.close()
    return redirect(url_for("get_profile"))

@app.post("/delete_account/")
@login_required
def delete_account():
    user_id = current_user.user_id
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()
    logout_user()
    return redirect(url_for("get_login"))