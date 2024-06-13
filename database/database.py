import sqlite3

def get_db_connection():
    conn = sqlite3.connect('series_registradas.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS series (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            exercicio TEXT NOT NULL,
            tipo_serie TEXT NOT NULL,
            carga REAL NOT NULL,
            reps INTEGER NOT NULL,
            descanso INTEGER NOT NULL,
            esforco_percebido INTEGER NOT NULL,
            obs TEXT,
            data_registro DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
