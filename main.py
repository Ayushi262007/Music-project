import tkinter as tk
import sqlite3
from topbar import create_topbar
from sidebar import create_sidebar
from dashboard import create_dashboard
from start_practice import create_start_practice_frame
from practice_history import create_practice_history_frame
from goals import create_goals_frame
from practice_notes import create_practice_notes_frame
from analysis import create_analysis_frame
from achievements import create_achievements_frame
from calendar_view import create_calendar_frame
from music_login import MusicLoginApp
from tkinter import messagebox


def create_tables():
    conn = sqlite3.connect("music_tracker.db")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS practice_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            date TEXT,
            instrument TEXT,
            duration INTEGER,
            notes TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            goal_title TEXT,
            description TEXT,
            target_minutes INTEGER,
            due_date TEXT,
            completed INTEGER DEFAULT 0
        )
    ''')

    conn.commit()
    conn.close()


def main(username):
    root = tk.Tk()
    root.title("Music Practice Tracker - Dashboard")
    root.attributes('-fullscreen', True)
    create_tables()

    # 🌟 Light pleasant background (non-white)
    app_bg_color = "#506F9E"       # Soft pastel blue
    content_bg_color = "#2C3646"

    root.configure(bg=app_bg_color)

    def on_minimize():
        root.iconify()

    def on_close():
        root.destroy()

    def logout_user():
        if messagebox.askyesno("Logout", "Are you sure you want to log out?"):
            root.destroy()
            login_win = tk.Tk()
            login_win.title("Login Again")
            MusicLoginApp(login_win)
            login_win.mainloop()

    # Top Bar
    create_topbar(root, on_minimize, on_close)

    # Wrapper for sidebar and main content
    content_frame = tk.Frame(root, bg=content_bg_color)
    content_frame.pack(fill="both", expand=True)

    # Sidebar
    sidebar = create_sidebar(content_frame, on_nav_click=lambda s: handle_navigation(s))
    sidebar.pack(side="left", fill="y")

    # Main content area
    global main_content
    main_content = tk.Frame(content_frame, bg=content_bg_color)
    main_content.pack(side="left", fill="both", expand=True)

    def handle_navigation(selection):
        for widget in main_content.winfo_children():
            widget.destroy()

        if selection == "Dashboard":
            create_dashboard(main_content, username)
        elif selection == "Start Practice":
            create_start_practice_frame(main_content, username)
        elif selection == "Practice History":
            create_practice_history_frame(main_content, username)
        elif selection == "Goals":
            create_goals_frame(main_content, username)
        elif selection == "Practice Notes":
            create_practice_notes_frame(main_content, username)
        elif selection == "Analysis by Graph":
            create_analysis_frame(main_content, username)
        elif selection == "Achievements":
            create_achievements_frame(main_content, username)
        elif selection == "Practice Calendar":
            create_calendar_frame(main_content, username)
        elif selection == "Logout":
            logout_user()
        else:
            tk.Label(main_content, text=f"{selection} Coming Soon...",
                     font=("Helvetica", 16, "bold"), bg=content_bg_color, fg="#333").pack(pady=50)

    # Load dashboard initially
    create_dashboard(main_content, username)

    root.mainloop()


if __name__ == "__main__":
    main("Ayushi")














