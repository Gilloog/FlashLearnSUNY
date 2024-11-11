import tkinter as tk
from tkinter import messagebox, ttk
from auth import register_user, login_user
from accuracy import update_user_accuracy, get_user_accuracy
from database import init_db
from database import get_db_connection
from flashcards import add_flashcard, get_flashcard
import pyttsx3 

class FlashLearnApp: 
    def __init__(self, root):
        self.root = root
        self.root.title("FlashLearnSUNY")
        self.root.geometry("400x300")
        self.engine = pyttsx3.init()
        self.current_page = 0
        init_db()
        
        self.show_login_screen()
        
    def show_login_screen(self):
        self.clear_frame()
    
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
        self.clear_frame()
        ttk.Label(self.root, text="Welcome to FlashLearnSUNY").pack()
    
        #tk.Button(self.root, text="Create Mode", command=self.show_create_flashcards).pack()
        ttk.Button(self.root, text="Study Mode", command=self.show_study_mode).pack()

        ttk.Button(self.root, text="Edit Flashcards", command=self.show_edit_flashcards_screen).pack()
        
        ttk.Button(self.root, text="View Badges", command=self.show_badges_page).pack()
        
        ttk.Button(self.root, text="Log Out", command=self.show_login_screen).pack(pady = 50)
    
    def show_create_flashcards(self):
        self.clear_frame()
        ttk.Label(self.root, text="Flashcard Create Mode").pack()
    
        self.front_entry = ttk.Entry(self.root)
        self.front_entry.pack()
        self.front_entry.insert(0,"Enter Front Text")
    
        self.back_entry = tk.Entry(self.root)
        self.back_entry.pack()
        self.back_entry.insert(0, "Enter Back Text")
    
        ttk.Button(self.root, text="Add Flashcard", command=self.add_flashcard).pack()
        ttk.Button(self.root, text="Back to Main Menu", command=self.show_main_menu).pack()
    
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
        self.clear_frame()
        ttk.Label(self.root, text="Study Mode", style="Header.TLabel").pack(pady=10)
    
        user_id = self.user_id
        self.flashcards = get_flashcard(user_id)
          
        if self.flashcards: 
            self.current_flashcard = 0
            self.display_flashcard()
        else:
            ttk.Label(self.root, text="No Flashcards Found", style="TLabel").pack()
            
    def clear_main_frame(self):
        for widget in self.root.winfo_children():
            if widget != self.card_frame:
                widget.destroy()
                
                        
    def display_flashcard(self):
        
        self.clear_frame()
        
        if self.current_flashcard < len(self.flashcards):
            front_card, back_card = self.flashcards[self.current_flashcard]   
            
           
            self.flip_card(front_card, back_card, show_front=True)
            
            if not hasattr(self, 'card_frame'):
                self.card_frame = ttk.Frame(self.root)
                self.card_frame.pack(pady=10)
                
            ttk.Button(self.root, text="Next Flashcard", command=self.next_flashcard).pack(pady=10)
            ttk.Button(self.root, text="Main Menu", command=self.show_main_menu).pack(pady=10)
            ttk.Button(self.root, text="Correct", command=lambda: self.record_answer(True)).pack(pady=10)
            ttk.Button(self.root, text="Incorrect", command=lambda: self.record_answer(False)).pack(pady=10)
            
            
            accuracy =  get_user_accuracy(self.user_id)
            ttk.Label(self.root, text=f"Overall Accuracy: {accuracy:.2f}%", style="TLabel").pack(pady=10) 
        else:
            ttk.Label("You have completed all flashcards!", style="TLabel").pack(pady=10)
            ttk.Button(self.root, text="Main Menu", command=self.show_main_menu).pack(pady=10)
            
    def flip_card(self, front_card, back_card, show_front=True):
        
        self.clear_main_frame()
          
        if show_front:
            ttk.Label(self.root, text=f"Front: {front_card}", style="TLabel").pack(pady=10)
            ttk.Button(self.root, text="Flip To Back", command=lambda: self.flip_card(front_card, back_card, show_front=False)).pack(pady=10)
            
        else: 
            ttk.Label(self.root, text=f"Back: {back_card}", style="TLabel").pack(pady=10)
            ttk.Button(self.root, text="Flip to Front", command=lambda: self.flip_card(front_card, back_card, show_front=True)).pack(pady=10)
            
        if not hasattr(self, 'card_frame'):
                self.card_frame = ttk.Frame(self.root)
                self.card_frame.pack(pady=10)
                
        ttk.Button(self.root, text="Next Flashcard", command=self.next_flashcard).pack(pady=10)
        ttk.Button(self.root, text="Main Menu", command=self.show_main_menu).pack(pady=10)
        ttk.Button(self.root, text="Correct", command=lambda: self.record_answer(True)).pack(pady=10)
        ttk.Button(self.root, text="Incorrect", command=lambda: self.record_answer(False)).pack(pady=10)
            
            
        accuracy =  get_user_accuracy(self.user_id)
        ttk.Label(self.root, text=f"Overall Accuracy: {accuracy:.2f}%", style="TLabel").pack(pady=10) 
            

    def record_answer(self, is_correct):
        update_user_accuracy(self.user_id, is_correct)
        self.display_flashcard()
               
    def next_flashcard(self):
        if self.flashcards and self.current_flashcard < len(self.flashcards)-1: 
            self.current_flashcard += 1
            self.clear_frame()
            self.display_flashcard()
        else: 
            messagebox.showinfo("Info", "You have reached the end of the flashcards.")
        
    
            
            
    

    def show_edit_flashcards_screen(self):
        self.clear_frame()
        ttk.Label(self.root, text="Edit Flashcards").grid(row=0, column=0, columnspan=2, pady=10)
        ttk.Button(self.root, text="Create Flashcard", command=self.show_create_flashcards).grid(row=0, column=0, columnspan=2, pady=5)
        ttk.Button(self.root, text="Back to Main Menu", command=self.show_main_menu).grid(row=5, column=0, columnspan=2, pady=5)

        self.flashcards = self.get_flashcards(self.user_id)
        if self.flashcards is None:
            self.flashcards = []

        #self.current_page = 0
        self.flashcards_per_page = 6
        self.display_flashcards()

        ##tk.Button(self.root, text="Back to Main Menu", command=self.show_main_menu).grid(row=5, column=0, columnspan=2, pady=10)

    def display_flashcards(self):
        start_index = self.current_page * self.flashcards_per_page
        end_index = start_index + self.flashcards_per_page
        row = 1
        col = 0
        for i, flashcard in enumerate(self.flashcards[start_index:end_index]):
            front, back = flashcard[1], flashcard[2]
            button_text = f"Front: {front}\nBack: {back}"
            ttk.Button(self.root, text=button_text, command=lambda f=flashcard: self.edit_flashcard(f)).grid(row=row, column=col, padx=5, pady=5)
            col += 1
            if col > 1:
                col = 0
                row += 1

        if (end_index < len(self.flashcards)) & (self.current_page > 0):
            ttk.Button(self.root, text="Next", command=self.next_page).grid(row=4, column=1, columnspan=1, pady=10)
            ttk.Button(self.root, text="Prev", command=self.prev_page).grid(row=4, column=0, columnspan=1, pady=10)
        elif end_index < len(self.flashcards):
            ttk.Button(self.root, text="Next", command=self.next_page).grid(row=4, column=0, columnspan=2, pady=10)
        elif self.current_page > 0:
            ttk.Button(self.root, text="Prev", command=self.prev_page).grid(row=4, column=0, columnspan=2, pady=10)
            
    def next_page(self):
        self.current_page += 1
        self.show_edit_flashcards_screen()
        
    def prev_page(self):
        self.current_page -= 1
        self.show_edit_flashcards_screen()
        
        
    def get_flashcards(self, user_id):
        con = get_db_connection()
        cursor = con.cursor()
        cursor.execute('SELECT id, front, back FROM flashcards WHERE user_id = ?', (user_id,))
        flashcards = cursor.fetchall()
        con.close()
        return flashcards
    
    
            
    def edit_flashcard(self, flashcard):
        self.clear_frame()
        ttk.Label(self.root, text="Edit Flashcard").pack()

        front_text = ttk.Entry(self.root)
        front_text.insert(0, flashcard[1])
        front_text.pack(pady=5)

        back_text = ttk.Entry(self.root)
        back_text.insert(0, flashcard[2])
        back_text.pack(pady=5)

        ttk.Button(self.root, text="Save", command=lambda: self.save_flashcard(flashcard[0], front_text.get(), back_text.get())).pack(pady=5)
        ttk.Button(self.root, text="Delete", command=lambda: self.delete_flashcard(flashcard[0])).pack(pady=5)
        ttk.Button(self.root, text="Back", command=self.show_edit_flashcards_screen).pack(pady=10)
        
    def save_flashcard(self, flashcard_id, front, back):
        con = get_db_connection()
        cursor = con.cursor()
        cursor.execute('UPDATE flashcards SET front = ?, back = ? WHERE id = ?', (front, back, flashcard_id))
        con.commit()
        con.close()
        messagebox.showinfo("Success", "Flashcard Changed")
        self.show_edit_flashcards_screen()


    def delete_flashcard(self, flashcard_id):
        con = get_db_connection()
        cursor = con.cursor()
        cursor.execute('DELETE FROM flashcards WHERE id = ?', (flashcard_id,))
        con.commit()
        con.close()
        messagebox.showinfo("Success", "Flashcard Deleted")
        self.show_edit_flashcards_screen()

    def show_badges_page(self):
        self.clear_frame()
        
        ttk.Label(self.root, text="Your Badges", font=("Arial", 10)).pack(pady=10)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT badges FROM users WHERE id = ?", (self.user_id,))
        result = cursor.fetchone()
        conn.close()
        
        badges = result[0] if result is not None else ""
        
        if badges: 
            ttk.Label(self.root, text="Earned Badges:", font=("Arial", 14)).pack(pady=5)
            badge_list = badges.split(";")
            
            for badge in badge_list:
                if badge.strip():
                    ttk.Label(self.root, text=f"- {badge.strip()}", font=("Arial",12)).pack()
        else: 
            ttk.Label(self.root, text="No badges earned yet.", font=("Arial", 12)).pack(pady=20)
        
        ttk.Button(self.root, text="Main Menu", command=self.show_main_menu).pack()
        
        
    
    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()    

        
if __name__ == "__main__":
    root = tk.Tk()
    app = FlashLearnApp(root)
    root.mainloop()
