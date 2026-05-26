import sqlite3
import os

DATABASE = os.path.join("instance", "medsafe.db")

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn