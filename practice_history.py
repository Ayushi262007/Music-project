# practice_history.py
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

def create_practice_history_frame(parent, username):
    # Main Frame
    frame = tk.Frame(parent, bg="#F2F6FC")  # Background color
    frame.pack(fill="both", expand=True)

    # Title
    title = tk.Label(
        frame,
        text="🎵 Practice History",
        font=("Helvetica", 18, "bold"),
        bg="#FFFFFF",
        fg="#2B2B2B"  # Text color
    )
    title.pack(pady=10)

    # Treeview Frame with Scrollbar
    tree_frame = tk.Frame(frame, bg="#F2F6FC")
    tree_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))

    tree_scroll = tk.Scrollbar(tree_frame)
    tree_scroll.pack(side="right", fill="y")

    # Columns
    columns = ("Date", "Instrument", "Duration (min)", "Practice")
    tree = ttk.Treeview(
        tree_frame,
        columns=columns,
        show="headings",
        yscrollcommand=tree_scroll.set,
        height=15
    )
    tree_scroll.config(command=tree.yview)

    # Style
    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "Treeview",
        background="#FFFFFF",        # Table background
        foreground="#2B2B2B",        # Text color
        rowheight=30,
        fieldbackground="#FFFFFF",
        bordercolor="#FFFFFF",
        font=("Helvetica", 10)
    )
    style.configure(
        "Treeview.Heading",
        background="#A084E8",        # Accent color for heading
        foreground="#FFFFFF",
        font=("Helvetica", 10, "bold")
    )
    style.map("Treeview", background=[("selected", "#F8C8DC")])  # Selection color

    # Configure headings & columns
    for col in columns:
        tree.heading(col, text=col)
        if col == "Notes":
            tree.column(col, anchor="w", width=350)
        else:
            tree.column(col, anchor="center", width=160)

    tree.pack(fill="both", expand=True)

    # Load Data from DB
    def load_data():
        conn = sqlite3.connect("music_tracker.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT date, instrument, duration, notes
            FROM practice_sessions
            WHERE username = ?
            ORDER BY date DESC
        """, (username,))
        rows = cursor.fetchall()
        tree.delete(*tree.get_children())
        for row in rows:
            tree.insert("", "end", values=row)
        conn.close()

    load_data()

    # Delete Record
    def delete_entry():
        selected = tree.focus()
        if not selected:
            messagebox.showwarning("Select Entry", "Please select a record to delete.")
            return
        values = tree.item(selected, "values")
        confirm = messagebox.askyesno("Confirm Delete", f"Delete session from {values[0]}?")
        if confirm:
            conn = sqlite3.connect("music_tracker.db")
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM practice_sessions
                WHERE username = ? AND date = ? AND instrument = ? AND duration = ? AND notes = ?
            """, (username, values[0], values[1], values[2], values[3]))
            conn.commit()
            conn.close()
            load_data()

    # Delete Button
    delete_btn = tk.Button(
        frame,
        text="🗑️ Delete Selected",
        command=delete_entry,
        bg="#F8C8DC",         # Button color
        fg="#2B2B2B",         # Text color
        font=("Helvetica", 10, "bold"),
        activebackground="#A084E8",
        activeforeground="#FFFFFF",
        cursor="hand2"
    )
    delete_btn.pack(pady=10)

    return frame



