from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3

from database import registrations_count
from config import MAX_PLAYERS

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DB = "nutsclub.db"

def conn():
    return sqlite3.connect(DB)

# ---------- PROFILE ----------
@app.get("/profile/{user_id}")
def profile(user_id: int):
    c = conn()
    cur = c.cursor()
    cur.execute("SELECT name, points FROM users WHERE user_id=?", (user_id,))
    user = cur.fetchone()
    c.close()

    if not user:
        return {"name": "Гость", "points": 0}

    return {"name": user[0], "points": user[1]}

# ---------- LEADERBOARD ----------
@app.get("/leaderboard")
def leaderboard():
    c = conn()
    cur = c.cursor()
    cur.execute("SELECT name, points FROM users ORDER BY points DESC")
    data = cur.fetchall()
    c.close()
    return [{"name": n, "points": p} for n, p in data]

# ---------- GAMES ----------
@app.get("/games")
def games():
    c = conn()
    cur = c.cursor()
    cur.execute("SELECT id, date, title FROM games")
    rows = cur.fetchall()

    result = []
    for game_id, date, title in rows:
        count = registrations_count(game_id)
        result.append({
            "id": game_id,
            "date": date,
            "title": title,
            "registered": count,
            "max": MAX_PLAYERS
        })

    c.close()
    return result

# ---------- ROOT ----------
@app.get("/")
def root():
    return {
        "status": "ok",
        "service": "The NUTS Club Mini App API"
    }
