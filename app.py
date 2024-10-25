import tkinter as tk
from tkinter import messagebox
from auth import register_user, login_user
from database import init_db
from flashcards import add_flashcard, get_flashcard
class FlashLearnApp: 
    def __init__(self, root):
        self.root = root
        self.root.title("FlashLearnSUNY")
        self.root.geometry("400x300")
        
        init_db()
        
        self.show_login_screen()
        
    def show_login_screen(self):
        self.clear_frame()
    
        tk.Label(self.root, text="Username:").pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()
    
        tk.Label(self.root, text="Password").pack()
        self.password_entry = tk.Entry(self.root, show='*')
        self.password_entry.pack()
    
        tk.Button(self.root, text='Login', command=self.login).pack()
        tk.Button(self.root, text='Register', command=self.register).pack()
    
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user = login_user(username, password)
    
        if user: 
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
        self.clear_frame()
        tk.Label(self.root, text="Welcome to FlashLearnSUNY").pack()
    
        tk.Button(self.root, text="Create Mode", command=self.show_create_flashcards).pack()
        tk.Button(self.root, text="Study Mode", command=self.show_study_mode).pack()
    
    def show_create_flashcards(self):
        self.clear_frame()
        tk.Label(self.root, text="Flashcard Create Mode").pack()
    
        self.front_entry = tk.Entry(self.root)
        self.front_entry.pack()
        self.front_entry.insert(0,"Enter Front Text")
    
        self.back_entry = tk.Entry(self.root)
        self.back_entry.pack()
        self.back_entry.insert(0, "Enter Back Text")
    
        tk.Button(self.root, text="Add Flashcard", command=self.add_flashcard).pack()
        tk.Button(self.root, text="Back to Main Menu", command=self.show_main_menu).pack()
    
    def add_flashcard(self):
        front_text = self.front_entry.get()
        back_text = self.back_entry.get()
        
        if hasattr(self, 'user_id'):
            add_flashcard(self.user_id, front_text, back_text)
            messagebox.showinfo("Success", "Flashcard Added")
        else: 
            messagebox.showerror("Error", "User is not Logged in!")
      
    def show_study_mode(self):
        self.clear_frame()
        tk.Label(self.root, text="Study Mode").pack()
    
        user_id = self.user_id
        flashcards = get_flashcard(user_id)
    
        if flashcards: 
            self.current_flashcard = 0
            self.flashcards = flashcards
            self.display_flashcard()
        else:
            tk.Label(self.root, text="No Flashcards Found").pack()
            
        tk.Button(self.root, text="Back to Main Menu", command=self.show_main_menu).pack()

    def display_flashcard(self):
        front, back = self.flashcards[self.current_flashcard]
        tk.Label(self.root, text=f"Front: {front}").pack()
    
        def flip_card():
            tk.Label(self.root, text=f"Back: {back}").pack()
        
        tk.Button(self.root, text="Flip", command=flip_card).pack()
    
    
    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()    

        
if __name__ == "__main__":
    root = tk.Tk()
    app = FlashLearnApp(root)
    root.mainloop()