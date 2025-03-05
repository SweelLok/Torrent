from flask import render_template, request, jsonify, redirect, url_for, flash
from flask_login import current_user, login_required
from ..config import RAWG_BASE_URL, RAWG_API_KEY
from app import app
from connection import get_db_connection
import requests

@app.get("/games_data_json/")
def get_games_json():
    query = request.args.get("search", "")
    url = f"{RAWG_BASE_URL}/games?key={RAWG_API_KEY}&search={query}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        games = response.json().get("results", [])
        return jsonify(games)
    
    return jsonify({"error": "Error to get data base data"}), 500

@app.get("/menu/")
def get_games():
    page = request.args.get("page", 1, type=int)
    query = request.args.get("search", "")
    url = f"{RAWG_BASE_URL}/games?key={RAWG_API_KEY}&search={query}&page={page}&page_size=21"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        games = response.json().get("results", [])
        total_results = response.json().get("count", 0)
        total_pages = (total_results // 21) + (1 if total_results % 21 > 0 else 0)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        favorite_games = cursor.execute("SELECT game_id FROM favorite_games WHERE user_id = ?", (current_user.user_id,)).fetchall()
        favorite_game_ids = [game["game_id"] for game in favorite_games]
        
        return render_template("menu.html", games=games, page=page, total_pages=total_pages, max=max, min=min, query=query, favorite_game_ids=favorite_game_ids)
    
    return render_template("menu.html", games=[], page=page, total_pages=0, max=max, min=min, query=query)

@app.get("/game/<int:game_id>/")
def get_game_details(game_id):
    url = f"{RAWG_BASE_URL}/games/{game_id}?key={RAWG_API_KEY}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        game = response.json()
        return render_template("game_details.html", game=game)
    
    return redirect(url_for("get_games"))

@app.post("/favorite_games/<int:game_id>")
@login_required
def post_favorite_games(game_id):
    user_id = current_user.user_id
    conn = get_db_connection()
    cursor = conn.cursor()
    existing_favorite = cursor.execute("SELECT * FROM favorite_games WHERE user_id = ? AND game_id = ?", (user_id, game_id)).fetchone()
    if existing_favorite:
        cursor.execute("DELETE FROM favorite_games WHERE user_id = ? AND game_id = ?", (user_id, game_id))
        print("Game successfully removed from favorites!")
    else:
        cursor.execute("INSERT INTO favorite_games (user_id, game_id) VALUES (?, ?)", (user_id, game_id))
        print("Game successfully added to favorites!")
    conn.commit()
    conn.close()
    
    page = request.form.get("page", 1, type=int)
    query = request.form.get("search", "")
    return redirect(url_for("get_games", page=page, search=query))