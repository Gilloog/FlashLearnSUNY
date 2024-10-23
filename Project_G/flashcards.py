from database import get_db_connection

def add_flashcard(user_id, front, back):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    cursor.execute('INSERT INTO flashcards (user_id, front, back) VALUES (?,?,?)', (user_id, front, back))
    connection.commit()
    connection.close()
    
def get_flashcard(user_id):
    connection = get_db_connection
    cursor = connection.cursor()
    
    cursor.execute('SELECT front, back FROM flashcards WHERE user_id = ?', (user_id))
    flashcards = cursor.fetchall()
    connection.close()
    return flashcards

