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
        last_login DATE, 
        badges TEXT DEFAULT '', 
        accuracy REAL DEFAULT 0.0
    )
    ''')
    
    cursor.execute("PRAGMA table_info(users)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if 'total_attempts' not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN total_attempts INTEGER DEFAULT 0")
    if 'correct_attempts' not in columns: 
        cursor.execute("ALTER TABLE users ADD COLUMN correct_attempts INTEGER DEFAULT 0")
        
        
    
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
    
def reset_attempts(user_id):
        con = get_db_connection()
        cursor = con.cursor()
        
        cursor.execute("""UPDATE users SET total_attempts = 0, correct_attempts = 0 WHERE id = ?""", (user_id,)) 
        
        con.commit()
        con.close()
        
def get_db_connection():
    con = sqlite3.connect('flashlearn.db')
    return con

if __name__ == "__main__":
    init_db()