from flask import render_template, request, jsonify
from ..config import RAWG_BASE_URL, RAWG_API_KEY
from app import app
import requests


@app.get("/games_data_json/")
def get_games_json():
    query = request.args.get("search", "")
    url = f"{RAWG_BASE_URL}/games?key={RAWG_API_KEY}&search={query}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        games = response.json().get("results", [])
        return jsonify(games)
    
    return jsonify({"error": "Error to get db data"}), 500

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
        return render_template("menu.html", games=games, page=page, total_pages=total_pages, max=max, min=min, query=query)
    
    return render_template("menu.html", games=[], page=page, total_pages=0, max=max, min=min, query=query)