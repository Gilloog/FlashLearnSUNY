import sqlite3
from database import get_db_connection
from datetime import datetime, timedelta

def register_user(username, password):
    con = get_db_connection()
    cursor = con.cursor()
    
    if (len(username) or len(password) < 8) :
         print("username/password too short")
         return False

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
def update_streak_badges(streak, badges):
                streak_badges = { 
                    1: "1-day streak badge",
                    5: "5-day streak badge",
                    10: "10-day streak badge", 
                    15: "15-day streak badge", 
                    20: "20-day streak badge", 
                    30: "30-day streak badge", 
                    50: "50-day streak badge", 
                    100: "100-day streak badge", }
                
                for days, badge in streak_badges.items():
                    if streak >= days and badge not in badges:
                        badges += f"{badge}"
                return badges.strip(";")       
def login_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT id, username, password, streak, last_login FROM users WHERE username = ? AND password = ?', (username, password)) 
        user = cursor.fetchone()

        if user:
            user_id = user[0]  
            streak = user[3]  if user[3] is not None else 0
            last_login = user[4]  
             

            today = datetime.now().date()

            
            if last_login:
                last_login_date = datetime.strptime(last_login, '%Y-%m-%d').date()
                if last_login_date == today - timedelta(days=1):
                    streak += 1  
                elif last_login_date < today - timedelta(days=1):
                    streak = 1  
            else:
                streak = 1  
                
            cursor.execute('UPDATE users SET streak = ?, last_login = ? WHERE id = ?', (streak, today, user_id))
            conn.commit()

            print(f"Welcome, {username}! Your current streak is {streak} days.")
            return user
        else:
            print("Invalid Login. Try again or register.")
            return None
    finally:
        conn.close()   
            