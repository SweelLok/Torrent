import sqlite3


def get_db_connection():
    connection = sqlite3.connect("database.db", timeout=5)
    connection.row_factory = sqlite3.Row
    return connection
        
def create_tables():
    connection = sqlite3.connect("database.db")
    with open("schema.sql") as f:
        connection.executescript(f.read())