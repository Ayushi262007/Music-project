import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import sqlite3
from datetime import datetime, timedelta

# ---------- DATABASE FUNCTION ----------
def get_dashboard_data(username):
    conn = sqlite3.connect("music_tracker.db")
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(duration) FROM practice_sessions WHERE username=?", (username,))
    total_minutes = cursor.fetchone()[0] or 0

    today = datetime.today()
    week_start = today - timedelta(days=today.weekday())
    cursor.execute("SELECT COUNT(*) FROM practice_sessions WHERE username=? AND date>=?",
                   (username, week_start.strftime('%Y-%m-%d')))
    weekly_sessions = cursor.fetchone()[0]

    cursor.execute("SELECT DISTINCT instrument FROM practice_sessions WHERE username=?", (username,))
    instruments = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT goal_title, due_date FROM goals WHERE username=? AND completed=0 ORDER BY due_date ASC LIMIT 3", (username,))
    upcoming_goals = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM goals WHERE username=? AND completed=1", (username,))
    total_achievements = cursor.fetchone()[0]

    conn.close()

    return {
        "total_minutes": total_minutes,
        "weekly_sessions": weekly_sessions,
        "instruments": instruments,
        "upcoming_goals": upcoming_goals,
        "total_achievements": total_achievements
    }

# ---------- DASHBOARD UI ----------
def create_dashboard(parent, username="User"):
    # 🌤️ Matching Elegant Light Theme
    bg_color = "#F2F6FC"
    card_bg = "#FFFFFF"
    accent_color = "#A2679C"
    accent_alt = "#27AE60"
    text_main = "#1D3C5C"
    text_secondary = "#7B8FA1"

    parent.configure(bg=bg_color)
    for widget in parent.winfo_children():
        widget.destroy()

    data = get_dashboard_data(username)
    hours = data["total_minutes"] // 60
    minutes = data["total_minutes"] % 60

    tk.Label(parent, text=f"🎵 Welcome back, {username}!",
             font=("Helvetica", 20, "bold"), bg=bg_color, fg=text_main).pack(pady=20)

    # ---------- SUMMARY CARDS ----------
    summary_frame = tk.Frame(parent, bg=bg_color)
    summary_frame.pack(pady=10)

    card_data = [
        ("Total Practice Time", f"{hours} hrs {minutes} mins"),
        ("This Week's Sessions", str(data["weekly_sessions"])),
        ("Instruments Practiced", ", ".join(data["instruments"]) or "None"),
        ("Total Achievements", str(data["total_achievements"])),
    ]

    for title, value in card_data:
        card = tk.Frame(summary_frame, bg=card_bg, padx=20, pady=15, bd=1, relief="solid")
        card.pack(side="left", padx=15, pady=5)

        tk.Label(card, text=title, font=("Helvetica", 12, "bold"), bg=card_bg, fg=accent_color).pack(anchor="w")
        tk.Label(card, text=value, font=("Helvetica", 14, "bold"), bg=card_bg, fg=text_main).pack(anchor="w", pady=(5, 0))

    # ---------- GRAPH ----------
    graph_frame = tk.Frame(parent, bg=bg_color)
    graph_frame.pack(pady=20, fill="x")

    fig = plt.Figure(figsize=(6.5, 3.5), dpi=100)
    ax = fig.add_subplot(111)

    conn = sqlite3.connect("music_tracker.db")
    cursor = conn.cursor()

    days = []
    durations = []
    today = datetime.today()

    for i in range(7):
        day_date = (today - timedelta(days=(6 - i)))
        day_label = day_date.strftime("%a")
        days.append(day_label)

        cursor.execute("SELECT SUM(duration) FROM practice_sessions WHERE username=? AND date=?",
                       (username, day_date.strftime('%Y-%m-%d')))
        duration = cursor.fetchone()[0] or 0
        durations.append(duration)

    conn.close()

    bars = ax.bar(days, durations, color=accent_color)
    for i, bar in enumerate(bars):
        height = bar.get_height()
        if height > 0:
            ax.text(bar.get_x() + bar.get_width() / 2, height + 1, f"{int(height)}",
                    ha='center', va='bottom', color=text_main, fontsize=9)

    ax.set_title('Practice Time This Week (in Minutes)', color=text_main, fontsize=12)
    ax.set_facecolor(card_bg)
    fig.patch.set_facecolor(bg_color)
    ax.tick_params(axis='x', colors=text_main)
    ax.tick_params(axis='y', colors=text_main)
    ax.set_ylabel("Minutes Practiced", color=text_main)
    ax.grid(True, color="#CCCCCC", linestyle="--", linewidth=0.5, axis='y')

    for spine in ax.spines.values():
        spine.set_color(text_secondary)

    chart = FigureCanvasTkAgg(fig, master=graph_frame)
    chart.get_tk_widget().pack()

    # ---------- UPCOMING GOALS ----------
    goals_frame = tk.LabelFrame(parent, text="🎯 Upcoming Goals", bg=card_bg, fg="#05113D",
                                font=("Helvetica", 12, "bold"), padx=15, pady=10, bd=1, relief="solid")
    goals_frame.pack(pady=10, fill="x", padx=40)

    if data["upcoming_goals"]:
        for title, due in data["upcoming_goals"]:
            tk.Label(goals_frame,
                     text=f"• {title} (Due: {due})",
                     bg=card_bg,
                     fg="#0D0808",
                     font=("Helvetica", 12)
                     ).pack(anchor="w", pady=2)
    else:
        tk.Label(goals_frame, text="No upcoming goals.",
                 bg=card_bg, fg=text_secondary,
                 font=("Helvetica", 10)).pack(anchor="w")

    # ---------- PRACTICE SESSION FORM ----------
    def start_session():
        session_win = tk.Toplevel(parent)
        session_win.title("Start Practice Session")
        session_win.geometry("400x400")
        session_win.configure(bg=card_bg)

        tk.Label(session_win, text="🎵 Start Practice Session", font=("Helvetica", 16, "bold"),
                 bg=card_bg, fg=accent_color).pack(pady=20)

        tk.Label(session_win, text="Instrument:", bg=card_bg, fg=text_main).pack(anchor="w", padx=20)
        instrument_entry = tk.Entry(session_win, width=30)
        instrument_entry.pack(pady=5)

        tk.Label(session_win, text="Duration (mins):", bg=card_bg, fg=text_main).pack(anchor="w", padx=20)
        duration_entry = tk.Entry(session_win, width=30)
        duration_entry.pack(pady=5)

        tk.Label(session_win, text="Practice Notes (optional):", bg=card_bg, fg=text_main).pack(anchor="w", padx=20)
        notes_entry = tk.Text(session_win, height=4, width=30)
        notes_entry.pack(pady=5)

        def save_session():
            instrument = instrument_entry.get().strip()
            duration = duration_entry.get().strip()
            notes = notes_entry.get("1.0", "end").strip()

            if not instrument or not duration.isdigit():
                messagebox.showerror("Invalid Input", "Please enter a valid instrument and duration.")
                return

            conn = sqlite3.connect("music_tracker.db")
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS practice_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    date TEXT,
                    instrument TEXT,
                    duration INTEGER,
                    notes TEXT
                )
            """)

            cursor.execute(
                "INSERT INTO practice_sessions (username, date, instrument, duration, notes) VALUES (?, ?, ?, ?, ?)",
                (username, datetime.today().strftime('%Y-%m-%d'), instrument, int(duration), notes)
            )
            conn.commit()
            conn.close()

            messagebox.showinfo("Saved", "Practice session saved successfully!")
            session_win.destroy()
            create_dashboard(parent, username)

        tk.Button(session_win, text="Save Session", command=save_session,
                  bg=accent_color, fg="white", font=("Helvetica", 12, "bold"),
                  padx=10, pady=5, bd=0, cursor="hand2").pack(pady=20)

    # ---------- START PRACTICE BUTTON ----------
    tk.Button(parent, text="🎵 Start New Practice Session", font=("Helvetica", 12, "bold"),
              bg=accent_alt, fg="white", padx=20, pady=10, bd=0, cursor="hand2",
              command=start_session).pack(pady=30)






















