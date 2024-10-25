import sqlite3

def init_db():
    con = sqlite3.connect('flashlearn.db')
    cursor = con.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE, 
        password TEXT NOT NULL,
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
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    ''')
    
    con.commit()
    con.close()

def get_db_connection():
    con = sqlite3.connect('flashlearn.db')
    return con

if __name__ == "__main__":
    init_db()