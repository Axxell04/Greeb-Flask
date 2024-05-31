import sqlite3
import os
from dotenv import load_dotenv
from flask import Flask, g
from werkzeug.security import generate_password_hash

load_dotenv()

def get_db() -> sqlite3.Connection:
    if "db" not in g:
        g.db = sqlite3.connect("db.db", detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row
        
    return g.db

def close_db(e: None):
    db = g.pop("db", None)
    
    if db is not None:
        db.close()
        
def init_db(app: Flask):
    db = get_db()
    with app.open_resource("init_db.sql") as file:
        db.executescript(file.read().decode("utf8"))
    
    try:
        db.execute("INSERT INTO user (username, password, admin) VALUES (?, ?, ?)", ("admin", generate_password_hash(os.getenv("ADMIN_PASSWORD")), True))
        db.commit()
    except sqlite3.IntegrityError as e:
        pass