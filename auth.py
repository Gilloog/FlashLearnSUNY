import sqlite3
import hashlib
from database import get_db_connection

def register_user(username, password):
<<<<<<< HEAD
    con = get_db_connection()
    cursor = con.cursor()
=======
    connection = get_db_connection()
    cursor = connection.cursor()
>>>>>>> 1a1052f3cc4f2bcac5ae8c1307f49c52d8e13433
    
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    try: 
        cursor.execute('INSERT INTO users (username, password) VALUES (?,?)', (username, hashed_password))
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
    
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, hashed_password)) 
    user = cursor.fetchone()
    con.close()
    
    if user: 
        print("Welcome, {username}!")
        return user
    else: 
        print("Invalid Login. Try again or register.")
        return None