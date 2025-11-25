import sqlite3

DATABASE_NAME = "holyweb.db"

def criar_conexao():
    return sqlite3.connect(DATABASE_NAME, timeout=5)

def criar_tabelas():
    con = criar_conexao()
    cursor = con.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        );
    """)
    con.commit()
    con.close()