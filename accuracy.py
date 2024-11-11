from database import get_db_connection

def update_user_accuracy(user_id, is_correct):
    con = get_db_connection()
    cursor = con.cursor()
    
    cursor.execute("UPDATE users SET total_attempts = total_attempts + 1 WHERE id = ?", (user_id,))
    if is_correct:
        cursor.execute("UPDATE users SET correct_attempts = correct_attempts + 1 WHERE id = ?", (user_id,))
        
    cursor.execute("SELECT correct_attempts, total_attempts FROM users WHERE id = ?", (user_id,))
    correct_attempts, total_attempts = cursor.fetchone()
    
    accuracy = (correct_attempts)/(total_attempts) * 100 if total_attempts > 0 else 0
    
    con.commit()
    con.close()
    
    print(f"User Accuracy Updated: {accuracy:.2f}%") 
    
def get_user_accuracy(user_id):
    con = get_db_connection()
    cursor = con.cursor()
    
    cursor.execute("SELECT accuracy FROM users WHERE id = ?",(user_id,))
    
    result = cursor.fetchone()
    accuracy = result[0] if result is not None else 0.0
    con.close()
    return accuracy
    
    