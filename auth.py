import sqlite3
from database import get_db_connection
from datetime import datetime, timedelta

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
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT id, username, password, streak, last_login, badges FROM users WHERE username = ? AND password = ?', (username, password)) 
        user = cursor.fetchone()

        if user:
            user_id = user[0]  
            streak = user[3]  if user[3] is not None else 0
            last_login = user[4]  
            badges = user[5] if user[5] else "" 

            today = datetime.now().date()

            
            if last_login:
                last_login_date = datetime.strptime(last_login, '%Y-%m-%d').date()
                if last_login_date == today - timedelta(days=1):
                    streak += 1  
                elif last_login_date < today - timedelta(days=1):
                    streak = 1  
            else:
                streak = 1  

            
            if streak >= 5 and "5-day streak badge" not in badges:
                badges += "5-day streak badge; "
            if streak >= 10 and "10-day streak badge" not in badges:
                badges += "10-day streak badge; "

            
            cursor.execute('UPDATE users SET streak = ?, last_login = ?, badges = ? WHERE id = ?', (streak, today, badges, user_id))
            conn.commit()

            print(f"Welcome, {username}! Your current streak is {streak} days.")
            return user
        else:
            print("Invalid Login. Try again or register.")
            return None
    finally:
        conn.close()   
            