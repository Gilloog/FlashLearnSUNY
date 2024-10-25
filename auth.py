import sqlite3
from database import get_db_connection

def register_user(username, password):
    con = get_db_connection()
    cursor = con.cursor()
    
    
    try: 
        cursor.execute('INSERT INTO users (username, password) VALUES (?,?)', (username, password))
        con.commit()
        print("User has been registered.")
        return True
    except sqlite3.IntegrityError:
        print("That user already exists.")
        return False
    finally: 
        con.close()
        
def login_user(username, password):
    con = get_db_connection()
    cursor = con.cursor()
    
    
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)) 
    user = cursor.fetchone()
    con.close()
    
    if user: 
        print("Welcome, {username}!")
        return user
    else: 
        print("Invalid Login. Try again or register.")
        return None