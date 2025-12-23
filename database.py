import sqlite3

DB = "nutsclub.db"

def conn():
    return sqlite3.connect(DB)

def init_db():
    c = conn()
    cur = c.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        name TEXT,
        phone TEXT,
        points INTEGER DEFAULT 0
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS games (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        title TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS registrations (
        user_id INTEGER,
        game_id INTEGER
    )
    """)

    # выдуманные игроки
    cur.execute("""
    INSERT OR IGNORE INTO users VALUES
    (1,'Алексей','000',120),
    (2,'Дмитрий','000',95),
    (3,'Игорь','000',80)
    """)

    # январское расписание
    cur.execute("""
    INSERT OR IGNORE INTO games VALUES
    (1,'10 января, пятница 19:00','Classic Texas Holdem'),
    (2,'17 января, пятница 19:00','Deep Stack'),
    (3,'24 января, пятница 19:00','Bounty Tournament')
    """)

    c.commit()
    c.close()

def get_user(uid):
    c = conn()
    cur = c.cursor()
    cur.execute("SELECT * FROM users WHERE user_id=?", (uid,))
    r = cur.fetchone()
    c.close()
    return r

def add_user(uid, name, phone):
    c = conn()
    cur = c.cursor()
    cur.execute("INSERT INTO users VALUES (?,?,?,0)", (uid, name, phone))
    c.commit()
    c.close()

def update_name(uid, name):
    c = conn()
    cur = c.cursor()
    cur.execute("UPDATE users SET name=? WHERE user_id=?", (name, uid))
    c.commit()
    c.close()

def update_phone(uid, phone):
    c = conn()
    cur = c.cursor()
    cur.execute("UPDATE users SET phone=? WHERE user_id=?", (phone, uid))
    c.commit()
    c.close()

def games():
    c = conn()
    cur = c.cursor()
    cur.execute("SELECT * FROM games")
    r = cur.fetchall()
    c.close()
    return r

def registrations_count(game_id):
    c = conn()
    cur = c.cursor()
    cur.execute("SELECT COUNT(*) FROM registrations WHERE game_id=?", (game_id,))
    r = cur.fetchone()[0]
    c.close()
    return r

def register_for_game(uid, game_id):
    c = conn()
    cur = c.cursor()
    cur.execute("INSERT INTO registrations VALUES (?,?)", (uid, game_id))
    cur.execute("UPDATE users SET points = points + 10 WHERE user_id=?", (uid,))
    c.commit()
    c.close()

def leaderboard():
    c = conn()
    cur = c.cursor()
    cur.execute("SELECT name, points FROM users ORDER BY points DESC")
    r = cur.fetchall()
    c.close()
    return r
