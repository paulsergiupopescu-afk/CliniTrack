import sqlite3

DB_PATH = "database/dentalclinic.db"

#Conexiune baza de date
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON") #ACTIVEZ FORIEGN KEYS
    return conn


def get_cursor_and_connection():
    """Get cursor and connection (most used)"""
    conn = get_connection()
    cursor = conn.cursor()
    return cursor, conn