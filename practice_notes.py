import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

def create_practice_notes_table():
    conn = sqlite3.connect("music_practice.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS practice_notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            note TEXT,
            category TEXT,
            date TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_practice_note(username, note, category):
    if not note.strip():
        messagebox.showwarning("Empty Note", "Please enter some practice notes.")
        return
    conn = sqlite3.connect("music_practice.db")
    c = conn.cursor()
    c.execute("INSERT INTO practice_notes (username, note, category, date) VALUES (?, ?, ?, ?)",
              (username, note.strip(), category, datetime.now().strftime("%Y-%m-%d %H:%M")))
    conn.commit()
    conn.close()
    messagebox.showinfo("Saved", "Practice note saved successfully.")

def load_notes(username, tree):
    for item in tree.get_children():
        tree.delete(item)
    conn = sqlite3.connect("music_practice.db")
    c = conn.cursor()
    c.execute("SELECT note, category, date FROM practice_notes WHERE username=? ORDER BY date DESC", (username,))
    for row in c.fetchall():
        tree.insert("", "end", values=row)
    conn.close()

def create_practice_notes_frame(parent, username):
    create_practice_notes_table()

    frame = tk.Frame(parent, bg= "#F2F6FC")
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="📝 Practice Notes", font=("Helvetica", 18, "bold"),
             bg="#FFFFFF", fg="#2B2B2B").pack(pady=10)

    form_frame = tk.Frame(frame, bg="#FFFFFF")
    form_frame.pack(pady=10)

    # Category dropdown
    tk.Label(form_frame, text="Category:", bg="#FFFFFF", fg="#2B2B2B",
             font=("Helvetica", 12)).grid(row=0, column=0, sticky="e", padx=5, pady=5)
    category_var = tk.StringVar(value="General")
    categories = ["General", "Tone", "Speed", "Rhythm", "Memory", "Expression"]
    category_menu = ttk.Combobox(form_frame, textvariable=category_var, values=categories, state="readonly", width=20)
    category_menu.grid(row=0, column=1, sticky="w", pady=5)

    # Notes field
    tk.Label(form_frame, text="Notes:", bg="#FFFFFF", fg="#2B2B2B",
             font=("Helvetica", 12)).grid(row=1, column=0, sticky="ne", padx=5)
    notes_text = tk.Text(form_frame, height=6, width=60, font=("Helvetica", 11), wrap="word",
                         relief="solid", bd=1)
    notes_text.grid(row=1, column=1, padx=5, pady=5)

    def handle_save():
        note = notes_text.get("1.0", tk.END)
        category = category_var.get()
        save_practice_note(username, note, category)
        notes_text.delete("1.0", tk.END)
        load_notes(username, notes_tree)

    tk.Button(form_frame, text="💾 Save Note", font=("Helvetica", 11), bg="#A084E8", fg="#FFFFFF",
              activebackground="#7A5CE3", relief="flat", padx=10, pady=5, command=handle_save).grid(row=2, column=1, sticky="e", pady=10)

    # Notes history
    separator = ttk.Separator(frame, orient="horizontal")
    separator.pack(fill="x", pady=10)

    tk.Label(frame, text="📂 Saved Notes", font=("Helvetica", 14, "bold"),
             bg="#FFFFFF", fg="#2B2B2B").pack()

    columns = ("Note", "Category", "Date")
    notes_tree = ttk.Treeview(frame, columns=columns, show="headings", height=8)
    for col in columns:
        notes_tree.heading(col, text=col)
        notes_tree.column(col, width=150, anchor="center")
    notes_tree.pack(pady=10, padx=20, fill="both", expand=True)

    load_notes(username, notes_tree)
