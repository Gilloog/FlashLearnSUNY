from database import get_db_connection

def add_flashcard(user_id, front, back):
    con = get_db_connection()
    cursor = con.cursor()
    
    cursor.execute('INSERT INTO flashcards (user_id, front, back) VALUES (?,?,?)', (user_id, front, back))
    con.commit()
    con.close()
    
def get_flashcard(user_id):
    con = get_db_connection
    cursor = con.cursor()
    
    cursor.execute('SELECT front, back FROM flashcards WHERE user_id = ?', (user_id))
    flashcards = cursor.fetchall()
    con.close()
    return flashcards

