import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import sqlite3
import os

# ---------- DATABASE SETUP ----------
conn = sqlite3.connect('music_tracker.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
''')




# Ensure columns exist
try:
    cursor.execute("ALTER TABLE users ADD COLUMN instrument TEXT")
except sqlite3.OperationalError:
    pass
try:
    cursor.execute("ALTER TABLE users ADD COLUMN exam_year TEXT")
except sqlite3.OperationalError:
    pass
conn.commit()

# ---------- MAIN APP ----------
class MusicLoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Practice Tracker - Login")

        # ✅ Fixed window settings to show title bar with buttons
        self.root.overrideredirect(False)  # Enable OS window border (title bar)
        try:
            self.root.state('zoomed')  # Maximize window with title bar (Windows)
        except:
            self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}+0+0")  # Cross-platform fallback

        self.root.configure(bg="#F0EBE3")

        # ---------- TOP TITLE ----------
        top_title = tk.Label(self.root, text="🎵 Music Practice Tracker", font=("Helvetica", 32, "bold"),
                             bg="#F0EBE3", fg="#1E1E1E")
        top_title.pack(pady=30)

        # ---------- CENTER FRAME ----------
        main_frame = tk.Frame(self.root, bg="#FFFFFF", bd=2, relief="groove")
        main_frame.place(relx=0.5, rely=0.5, anchor="center", width=520)

        # ---------- Logo Image ----------
        try:
            logo_img = Image.open("logo.png").resize((100, 100))
            logo_photo = ImageTk.PhotoImage(logo_img)
            logo_label = tk.Label(main_frame, image=logo_photo, bg="#FFFFFF")
            logo_label.image = logo_photo
            logo_label.pack(pady=(20, 10))
        except:
            tk.Label(main_frame, text="🎼", font=("Arial", 42), bg="#FFFFFF").pack(pady=(20, 10))

        # ---------- Login/Register Title ----------
        tk.Label(main_frame, text="Login / Register", font=("Helvetica", 22, "bold"),
                 bg="#FFFFFF", fg="#2C3E50").pack(pady=(0, 20))

        # ---------- Form Variables ----------
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.instrument_var = tk.StringVar()
        self.exam_year_var = tk.StringVar()

        # ---------- Input Fields ----------
        self.add_field(main_frame, "Username", self.username_var)
        self.add_field(main_frame, "Password", self.password_var, show="*")

        # ---------- Instrument Dropdown ----------
        self.add_dropdown(main_frame, "Instrument", self.instrument_var,
                          ["Piano", "Violin", "Guitar", "Flute", "Tabla", "Vocal", "Sitar", "Drums"])

        # ---------- Exam Year Dropdown ----------
        self.add_dropdown(main_frame, "Examination Level", self.exam_year_var,
                          ["Prarambhik", "Praveshika", "Madhyama", "Visharad", "Alankar"])

        # ---------- Buttons ----------
        self.add_button(main_frame, "Login", self.login, "#2F80ED")
        self.add_button(main_frame, "Register", self.register, "#27ae60")

        # ---------- Exit Button ----------
        tk.Button(self.root, text="Exit", command=self.root.quit,
                  font=("Arial", 11, "bold"), bg="#C0392B", fg="white",
                  relief="flat", padx=10, pady=4).place(relx=0.98, rely=0.02, anchor="ne")

    # ---------- FIELD CREATION ----------
    def add_field(self, frame, label_text, variable, show=None):
        tk.Label(frame, text=label_text, bg="#FFFFFF", anchor="w", fg="#2C3E50", font=("Arial", 12, "bold")).pack(fill="x", padx=30, pady=(5, 2))
        entry = tk.Entry(frame, textvariable=variable, font=("Arial", 12), fg="#34495E", bg="#F8F8F8",
                         show=show, relief="solid", bd=1, highlightthickness=1, highlightbackground="#BDC3C7")
        entry.pack(fill="x", padx=30, pady=(0, 12))

    def add_dropdown(self, frame, label, variable, values):
        tk.Label(frame, text=label, bg="#FFFFFF", anchor="w", fg="#2C3E50", font=("Arial", 12, "bold")).pack(fill="x", padx=30)
        dropdown = ttk.Combobox(frame, textvariable=variable, values=values,
                                font=("Arial", 12), state="readonly")
        dropdown.pack(fill="x", padx=30, pady=(0, 12))
        dropdown.set(f"Select {label}")

    def add_button(self, frame, text, command, color):
        btn = tk.Button(frame, text=text, command=command,
                        font=("Arial", 12, "bold"), bg=color, fg="white",
                        activebackground="#2980B9", relief="flat", width=20, pady=6)
        btn.pack(pady=(5, 10))

    # ---------- LOGIN FUNCTION ----------
    def login(self):
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        instrument = self.instrument_var.get().strip()
        exam_year = self.exam_year_var.get().strip()

        if not username or not password:
            messagebox.showwarning("Input Error", "Please enter username and password.")
            return

        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()

        if user:
            if user[2] == password:
                messagebox.showinfo("Login Successful", f"Welcome, {username}!")
                self.open_main_app(username)
            else:
                messagebox.showerror("Login Failed", "Invalid password.")
        else:
            try:
                cursor.execute("INSERT INTO users (username, password, instrument, exam_year) VALUES (?, ?, ?, ?)",
                               (username, password, instrument, exam_year))
                conn.commit()
                messagebox.showinfo("Registration Successful", f"Account created for {username}. Logging in...")
                self.open_main_app(username)
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Username already exists.")

    # ---------- REGISTER FUNCTION ----------
    def register(self):
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        instrument = self.instrument_var.get().strip()
        exam_year = self.exam_year_var.get().strip()

        if not username or not password:
            messagebox.showwarning("Input Error", "Username and password are required.")
            return

        try:
            cursor.execute("INSERT INTO users (username, password, instrument, exam_year) VALUES (?, ?, ?, ?)",
                           (username, password, instrument, exam_year))
            conn.commit()
            messagebox.showinfo("Registration Successful", "Now you can log in.")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists.")

    # ---------- OPEN MAIN APP ----------
    def open_main_app(self, username):
        self.root.destroy()
        if os.path.exists("main.py"):
            os.system("python main.py")
        else:
            messagebox.showinfo("Next Page", f"(main.py not found) Logged in as {username}")

# ---------- RUN ----------
if __name__ == "__main__":
    root = tk.Tk()
    app = MusicLoginApp(root)
    root.mainloop()
















