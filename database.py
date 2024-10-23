import sqlite3

def init_db():
    connection = sqlite3.connect('flashlearn.db')
    cursor = connection.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE, 
        password TEXT NOT NULL
        streak INTEGER DEFAULT 0, 
        accuracy REAL DEFAULT 0.0
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS flashcards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER, 
        front TEXT NOT NULL, 
        back TEXT NOT NULL, 
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    ''')
    
    connection.commit()
    connection.close()

def get_db_connection():
    return sqlite3.connect('flashlearn.db')