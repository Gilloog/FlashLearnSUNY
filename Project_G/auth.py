import sqlite3
import hashlib
from database import get_db_connection

def register_user(username, password):
    connection = get_db_connection
    cursor = connection.cursor()
    
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    try: 
        cursor.execute('INSERT INTO users (username, password) VALUES (?,?)', (username, hashed_password))
        connection.commit()
        print("User has been registered.")
        return True
    except sqlite3.IntegrityError:
        print("That user already exists.")
        return False
    finally: 
        connection.close()
        
def login_user(username, password):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, hashed_password)) 
    user = cursor.fetchone()
    connection.close()
    
    if user: 
        print("Welcome, {username}!")
        return user
    else: 
        print("Invalid Login. Try again or register.")
        return None