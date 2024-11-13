import tkinter as tk
import random as rand
from tkinter import messagebox, ttk
from auth import register_user, login_user, update_streak_badges
from accuracy import update_user_accuracy, get_user_accuracy
from database import init_db
from database import get_db_connection, reset_attempts
from flashcards import add_flashcard, get_flashcard
import pyttsx3 

class FlashLearnApp: 
    def __init__(self, root):
        self.root = root
        self.root.title("FlashLearnSUNY")
        self.root.geometry("600x400")
        self.engine = pyttsx3.init()
        self.current_page = 0
        self.acc_page = 0

        init_db()
        
        self.user_id = None
        self.current_page = None
        self.show_login_screen()
        
    def get_streaks_and_badges(self, user_id):
        con = get_db_connection()
        cursor = con.cursor()
        cursor.execute("SELECT streak, badges FROM users WHERE id = ?", (user_id,))
        result = cursor.fetchone()
        con.close()
        
        if result: 
            streak, badges = result
            return streak, badges or ""
        else:
            return 0, ""
        
    def setup_layout(self):
        self.menu_frame = tk.Frame(self.root, width=150, bg="#E9D9C2")
        self.menu_frame.pack(side="left", fill="y")
        
        self.content_frame = tk.Frame(self.root, bg="#C8BAAE")
        self.content_frame.pack(side="right", expand=True, fill="both")
        ttk.Label(self.menu_frame, text="Welcome to FlashLearnSUNY").pack()
        ttk.Button(self.menu_frame, text="Main Menu", command=self.show_main_menu).pack(fill="x", pady=5)
        ttk.Button(self.menu_frame, text="Study Mode", command=self.show_study_mode).pack(fill="x", pady=5)
        ttk.Button(self.menu_frame, text="Edit Flashcards", command=self.show_edit_flashcards_screen).pack(fill="x", pady=5)
        ttk.Button(self.menu_frame, text="View Badges", command=self.show_badges_page).pack(fill="x", pady=5)
        ttk.Button(self.menu_frame, text="Accuracy Stats", command=self.show_acc_page).pack(fill="x", pady=5)
        ttk.Button(self.menu_frame, text="Log Out", command=self.show_login_screen).pack(pady=20)
        
    def show_login_screen(self):
        if hasattr(self, 'menu_frame') and hasattr(self, 'content_frame'):
            self.menu_frame.pack_forget()
            self.content_frame.pack_forget()
        
        
        
        self.clear_frame(self.root) 
        ttk.Label(self.root, text="Username:").pack() 
        self.username_entry = tk.Entry(self.root) 
        self.username_entry.pack() 
        ttk.Label(self.root, text="Password").pack() 
        self.password_entry = tk.Entry(self.root, show='*') 
        self.password_entry.pack() 
        ttk.Button(self.root, text='Login', command=self.login).pack() 
        ttk.Button(self.root, text='Register', command=self.register).pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user = login_user(username, password)
    
        if (user) and (username != ''): 
            
            self.user_id = user[0]
            self.clear_frame(self.root)
            self.setup_layout()
            self.show_main_menu()
        else:
            messagebox.showerror("Error", "Invalid Login")
    
    def register(self): 
        username = self.username_entry.get()
        password = self.password_entry.get()
    
        if register_user(username, password):
            messagebox.showinfo("Success", "User Registered")
        else: 
            messagebox.showerror("Error", "Registration Failed.")
        
    def show_main_menu(self):
        self.current_page = 0
        self.clear_frame(self.content_frame)
        ttk.Label(self.content_frame, text="Main Menu", style="Header.TLabel").pack(pady=10)
        ttk.Label(self.content_frame, text="Welcome to FLASHLEARN SUNY", style="Header.TLabel").pack(pady=40)
        
    
    def show_create_flashcards(self):
        self.clear_frame(self.content_frame)
        ttk.Label(self.content_frame, text="Flashcard Create Mode").pack()
    
        self.front_entry = ttk.Entry(self.content_frame)
        self.front_entry.pack()
        self.front_entry.insert(0,"Enter Front Text")
    
        self.back_entry = tk.Entry(self.content_frame)
        self.back_entry.pack()
        self.back_entry.insert(0, "Enter Back Text")
    
        ttk.Button(self.content_frame, text="Add Flashcard", command=self.add_flashcard).pack()
        ttk.Button(self.content_frame, text="Back", command=self.show_edit_flashcards_screen).pack()
    
    def add_flashcard(self):
        front_text = self.front_entry.get()
        back_text = self.back_entry.get()
        
        if hasattr(self, 'user_id'):
            
            add_flashcard(self.user_id, front_text, back_text)
            messagebox.showinfo("Success", "Flashcard Added")
            self.show_edit_flashcards_screen()
        else: 
            messagebox.showerror("Error", "User is not Logged in!")
    
    def show_study_mode(self):
        self.clear_frame(self.content_frame)
        ttk.Label(self.content_frame, text="Study Mode", style="Header.TLabel").pack(pady=10)
    
        user_id = self.user_id
        self.flashcards = get_flashcard(user_id)
        reset_attempts(user_id)
          
        if self.flashcards:
            self.shuffle_order = self.shuffle(self.flashcards) 
            self.shown_flashcards = 0
            self.display_flashcard()
        else:
            ttk.Label(self.root, text="No Flashcards Found", style="TLabel").pack()
                               
    def display_flashcard(self):
        
        self.clear_frame(self.content_frame)
    
        if self.shown_flashcards < len(self.flashcards):
            front_card, back_card = self.flashcards[self.shuffle_order[self.shown_flashcards]]   
            
           
            self.flip_card(front_card, back_card, show_front=True)
            
            if not hasattr(self, 'card_frame'):
                self.card_frame = ttk.Frame(self.root)
                self.card_frame.pack(pady=10)
                
                
            
        else:
            ttk.Label("You have completed all flashcards!", style="TLabel").pack(pady=10)
            
    def flip_card(self, front_card, back_card, show_front=True):
        
        self.clear_frame(self.content_frame)
          
        if show_front:
            ttk.Label(self.content_frame, text=f"Front: {front_card}", style="TLabel").pack(pady=10)
            ttk.Button(self.content_frame, text="Flip To Back", command=lambda: self.flip_card(front_card, back_card, show_front=False)).pack(pady=10)
            ttk.Button(self.content_frame, text="Read Aloud", command=lambda: self.read_aloud(True,back_card,front_card)).pack(pady=10)
            ttk.Button(self.content_frame, text="Correct", command=lambda: self.record_answer(True)).pack(pady=10)
            ttk.Button(self.content_frame, text="Incorrect", command=lambda: self.record_answer(False)).pack(pady=10)
            accuracy =  get_user_accuracy(self.user_id)
            ttk.Label(self.content_frame, text=f"Overall Accuracy: {accuracy:.2f}%", style="TLabel").pack(pady=10)
            ttk.Button(self.content_frame, text="Next Flashcard", command=lambda: self.next_flashcard()).pack(pady=10)
            
            
        else: 
            ttk.Label(self.content_frame, text=f"Back: {back_card}", style="TLabel").pack(pady=10)
            ttk.Button(self.content_frame, text="Flip to Front", command=lambda: self.flip_card(front_card, back_card, show_front=True)).pack(pady=10)
            ttk.Button(self.content_frame, text="Read Aloud", command=lambda: self.read_aloud(False,back_card,front_card)).pack(pady=10)
            ttk.Button(self.content_frame, text="Correct", command=lambda: self.record_answer(True)).pack(pady=10)
            ttk.Button(self.content_frame, text="Incorrect", command=lambda: self.record_answer(False)).pack(pady=10)
            accuracy =  get_user_accuracy(self.user_id)
            ttk.Label(self.content_frame, text=f"Overall Accuracy: {accuracy:.2f}%", style="TLabel").pack(pady=10)
            ttk.Button(self.content_frame, text="Next Flashcard", command=lambda: self.next_flashcard()).pack(pady=10)

        if not hasattr(self, 'card_frame'):
                self.card_frame = ttk.Frame(self.content_frame)
                self.card_frame.pack(pady=10)
                 
            
    def read_aloud(self, side, back_card, front_card):
        if side:
            self.engine.say([front_card])
        else:
            self.engine.say([back_card])
        self.engine.runAndWait()

    def record_answer(self, is_correct):
        update_user_accuracy(self.user_id, is_correct)
        self.display_flashcard()
        
    def next_flashcard(self):
        user_id = self.user_id 
        if self.flashcards and self.shown_flashcards < len(self.flashcards)-1: 
            self.shown_flashcards += 1
            self.clear_frame(self.content_frame)
            self.display_flashcard()
        else: 
            self.clear_frame(self.content_frame)
            ttk.Label(self.content_frame, text="End of Flashcards.\n")
            accuracy =  get_user_accuracy(self.user_id)
            #print(type(accuracy))
            self.save_deck_accuracy(self.user_id, accuracy)
            ttk.Label(self.content_frame, text=f"Overall Accuracy: {accuracy:.2f}%", style="TLabel").pack(pady=10)
            
            
            ttk.Button(self.content_frame, text="Restart Flashcards", command=self.show_study_mode).pack(pady=10)
            con = get_db_connection()
            cursor = con.cursor()
            cursor.execute("UPDATE users SET accuracy = 0 WHERE id = ?", (user_id,))
            con.commit()
            con.close()
    
    def save_deck_accuracy(self, user_id, accuracy):
        con = get_db_connection()
        cursor = con.cursor()
        cursor.execute('INSERT INTO deck_accuracies (user_id, accuracy) VALUES (?, ?)', (user_id, accuracy))
        con.commit()
        con.close()

    def show_edit_flashcards_screen(self):
        self.clear_frame(self.content_frame)
        self.content_frame.pack(side="right", expand=True, fill="both")
        
        ttk.Label(self.content_frame, text="Edit Flashcards").grid(row=0, column=0, columnspan=2, pady=10)
        
        ttk.Button(self.content_frame, text="Create Flashcard", command=self.show_create_flashcards).grid(row=8, column=1, columnspan=2, pady=5)
        ttk.Button(self.content_frame, text="Delete Flashcard", command=self.show_edit_flashcards_screen_delete).grid(row=8, column=0, columnspan=2, pady=5)
        

        self.flashcards = self.get_flashcards(self.user_id)
        if self.flashcards is None:
            self.flashcards = []

        #self.current_page = 0
        self.flashcards_per_page = 5
        self.display_flashcards()

        ##tk.Button(self.root, text="Back to Main Menu", command=self.show_main_menu).grid(row=5, column=0, columnspan=2, pady=10)

    def display_flashcards(self):
        start_index = self.current_page * self.flashcards_per_page
        end_index = start_index + self.flashcards_per_page
        row = 1
        col = 0
        for i, flashcard in enumerate(self.flashcards[start_index:end_index]):
            ttk.Label(self.content_frame, text=f"Flashcard {i+1+start_index}:").grid(row=row, column=col, padx=5, pady=5)
            col += 1
            front, back = flashcard[1], flashcard[2]
            front_entry = ttk.Entry(self.content_frame)
            front_entry.insert(0, front)
            front_entry.grid(row=row, column=col, padx=5, pady=5)
            front_entry.bind("<FocusOut>", lambda e, f=flashcard, entry=front_entry: self.update_flashcard_front(f, entry))
            col += 1

            back_entry = ttk.Entry(self.content_frame)
            back_entry.insert(0, back)
            back_entry.grid(row=row, column=col, padx=5, pady=5)
            back_entry.bind("<FocusOut>", lambda e, f=flashcard, entry=back_entry: self.update_flashcard_back(f, entry))
            col += 1
            if col > 2:
                col = 0
                row += 1

        if (end_index < len(self.flashcards)) & (self.current_page > 0):
            ttk.Button(self.content_frame, text="Next", command=self.next_page).grid(row=row +1, column=1, pady=10)
            ttk.Button(self.content_frame, text="Prev", command=self.prev_page).grid(row=row+1, column=0, pady=10)
        elif end_index < len(self.flashcards):
            ttk.Button(self.content_frame, text="Next", command=self.next_page).grid(row=row +1, column=1, pady=10)
        elif self.current_page > 0:
            ttk.Button(self.content_frame, text="Prev", command=self.prev_page).grid(row=row +1, column=0, pady=10)
            
    
    def show_edit_flashcards_screen_delete(self):
        self.clear_frame(self.content_frame)
        ttk.Label(self.content_frame, text="Delete Flashcards").grid(row=0, column=0, columnspan=2, pady=10)
        ttk.Button(self.content_frame, text="Done", command=self.show_edit_flashcards_screen).grid(row=9, column=0, columnspan=2, pady=5)

        self.flashcards = self.get_flashcards(self.user_id)
        if self.flashcards is None:
            self.flashcards = []

        #self.current_page = 0
        self.flashcards_per_page = 5
        self.display_flashcards_delete()
    
    
    def display_flashcards_delete(self):
        start_index = self.current_page * self.flashcards_per_page
        end_index = start_index + self.flashcards_per_page
        row = 1
        col = 0
        for i, flashcard in enumerate(self.flashcards[start_index:end_index]):
            ttk.Label(self.content_frame, text=f"Flashcard {i+1+start_index}:").grid(row=row, column=col, padx=5, pady=5)
            col += 1
            front, back = flashcard[1], flashcard[2]
            button_text = f"Front: {front}"
            ttk.Button(self.content_frame, text=button_text, command=lambda f=flashcard: self.delete_flashcard(f[0])).grid(row=row, column=col, padx=5, pady=5)
            col += 1
            bt2 = f"Back: {back}"
            ttk.Button(self.content_frame, text=bt2, command=lambda f=flashcard: self.delete_flashcard(f[0])).grid(row=row, column=col, padx=5, pady=5)
            col += 1
            if col > 2:
                col = 0
                row += 1
           
           
        if (end_index < len(self.flashcards)) & (self.current_page > 0):
            ttk.Button(self.content_frame, text="Next", command=self.next_page_delete).grid(row=row +1, column=1, pady=10)
            ttk.Button(self.content_frame, text="Prev", command=self.prev_page_delete).grid(row=row +1, column=0, pady=10)
        elif end_index < len(self.flashcards):
            ttk.Button(self.content_frame, text="Next", command=self.next_page_delete).grid(row=row +1, column=1, pady=10)
        elif self.current_page > 0:
            ttk.Button(self.content_frame, text="Prev", command=self.prev_page_delete).grid(row=row +1, column=0, pady=10)
            
    def next_page(self):
        self.current_page += 1
        self.show_edit_flashcards_screen()
        
    def prev_page(self):
        self.current_page -= 1
        self.show_edit_flashcards_screen()
        
    def next_page_delete(self):
        self.current_page += 1
        self.show_edit_flashcards_screen_delete()
        
    def prev_page_delete(self):
        self.current_page -= 1
        self.show_edit_flashcards_screen_delete()
        
        
    def get_flashcards(self, user_id):
        con = get_db_connection()
        cursor = con.cursor()
        cursor.execute('SELECT id, front, back FROM flashcards WHERE user_id = ?', (user_id,))
        flashcards = cursor.fetchall()
        con.close()
        return flashcards
    
    
    def update_flashcard_front(self, flashcard, entry):
        #flashcard[1] = entry.get()
        self.save_flashcard_front(flashcard[0], entry.get())

    def update_flashcard_back(self, flashcard, entry):
        self.save_flashcard_back(flashcard[0], entry.get())
     
            
    def edit_flashcard(self, flashcard):
        self.clear_frame(self.content_frame)
        ttk.Label(self.content_frame, text="Edit Flashcard").pack()

        front_text = ttk.Entry(self.content_frame)
        front_text.insert(0, flashcard[1])
        front_text.pack(pady=5)

        back_text = ttk.Entry(self.content_frame)
        back_text.insert(0, flashcard[2])
        back_text.pack(pady=5)

        ttk.Button(self.content_frame, text="Save", command=lambda: self.save_flashcard(flashcard[0], front_text.get(), back_text.get())).pack(pady=5)
        ttk.Button(self.content_frame, text="Delete", command=lambda: self.delete_flashcard(flashcard[0])).pack(pady=5)
        ttk.Button(self.content_frame, text="Back", command=self.show_edit_flashcards_screen).pack(pady=10)
        
    def save_flashcard(self, flashcard_id, front, back):
        con = get_db_connection()
        cursor = con.cursor()
        cursor.execute('UPDATE flashcards SET front = ?, back = ? WHERE id = ?', (front, back, flashcard_id))
        con.commit()
        con.close()
        messagebox.showinfo("Success", "Flashcard Changed")
        self.show_edit_flashcards_screen()

    def save_flashcard_front(self, flashcard_id, front):
        con = get_db_connection()
        cursor = con.cursor()
        cursor.execute('UPDATE flashcards SET front = ? WHERE id = ?', (front, flashcard_id))
        con.commit()
        con.close()
        #messagebox.showinfo("Success", "Flashcard Front Changed")
        self.show_edit_flashcards_screen()

    def save_flashcard_back(self, flashcard_id, back):
        con = get_db_connection()
        cursor = con.cursor()
        cursor.execute('UPDATE flashcards SET back = ? WHERE id = ?', (back, flashcard_id))
        con.commit()
        con.close()
        #messagebox.showinfo("Success", "Flashcard Back Changed")
        self.show_edit_flashcards_screen()


    def delete_flashcard(self, flashcard_id):
        con = get_db_connection()
        cursor = con.cursor()
        cursor.execute('DELETE FROM flashcards WHERE id = ?', (flashcard_id,))
        con.commit()
        con.close()
        messagebox.showinfo("Success", "Flashcard Deleted")
        self.show_edit_flashcards_screen_delete()

    def update_user_badges(self, user_id, badges):
        
        con = get_db_connection()
        cursor = con.cursor()
        cursor.execute("UPDATE users SET badges = ? WHERE id = ?", (badges, user_id))
        con.commit()
        con.close()
        
    def show_badges_page(self):
        self.clear_frame(self.content_frame)
        
        streak, badges = self.get_streaks_and_badges(self.user_id)
        
        user_badges = update_streak_badges(streak, badges)
        
        if user_badges != badges: 
            self.update_user_badges(self.user_id, user_badges)
            badges = user_badges
            
        ttk.Label(self.content_frame, text="Earned Badges", font=("Arial", 20)).pack(pady=10)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT badges FROM users WHERE id = ?", (self.user_id,))
        result = cursor.fetchone()
        conn.close()
        
        badges = result[0] if result is not None else ""
        
        if badges: 
            badge_list = badges.split(";")
            
            for badge in badge_list:
                if badge.strip():
                    ttk.Label(self.content_frame, text=f"- {badge.strip()}", font=("Arial",12)).pack(pady=10)
        else: 
            ttk.Label(self.content_frame, text="No badges earned yet.", font=("Arial", 12)).pack(pady=20)
        
        ttk.Button(self.content_frame, text="Main Menu", command=self.show_main_menu).pack()
        
        
    
    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()    


    def shuffle(self,cards):
        shuffled = []
        numbers = list(range(len(cards)))
        while numbers :
            i = rand.randint(0,len(numbers)-1)
            shuffled.append(numbers[i])
            numbers.pop(i)
        return shuffled
    
    
    def show_acc_page(self):
        self.clear_frame(self.content_frame)
        tk.Label(self.content_frame, text="Accuracy History").pack(pady=10)
    
        con = get_db_connection()
        cursor = con.cursor()
        cursor.execute('SELECT accuracy FROM deck_accuracies WHERE user_id = ?', (self.user_id,))
        accuracies = cursor.fetchall()
        con.close()

        total_accuracy = 0
        for i, (accuracy,) in enumerate(accuracies):
            tk.Label(self.content_frame, text=f"Attempt {i}: {accuracy:.2f}%").pack(padx=10, pady=5)
            total_accuracy += accuracy

        if accuracies: 
            overall_accuracy = total_accuracy / len(accuracies) 
            tk.Label(self.content_frame, text=f"Overall Accuracy: {overall_accuracy:.2f}%").pack(pady=10) 
        else:
            tk.Label(self.content_frame, text="No attempts recorded.").pack(pady=10)
        
        tk.Button(self.content_frame, text="Back to Main Menu", command=self.show_main_menu).pack(pady=10)
        tk.Button(self.content_frame, text="Clear Accuracy History", command=lambda: self.clear_deck_accuracies(self.user_id)).pack(pady=10)
        
        
    def clear_deck_accuracies(self, user_id):
        con = get_db_connection()
        cursor = con.cursor()
        cursor.execute('DELETE FROM deck_accuracies WHERE user_id = ?', (user_id,))
        con.commit()
        con.close()
        self.show_acc_page()






        
if __name__ == "__main__":
    root = tk.Tk()
    app = FlashLearnApp(root)
    root.mainloop()
