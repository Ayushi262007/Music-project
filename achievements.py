import tkinter as tk
import sqlite3
from datetime import datetime, timedelta
from collections import defaultdict

def calculate_achievements(username):
    conn = sqlite3.connect("music_tracker.db")
    c = conn.cursor()
    c.execute("SELECT date, duration, instrument FROM practice_sessions WHERE username = ?", (username,))
    data = c.fetchall()

    c.execute("SELECT COUNT(*) FROM goals WHERE username = ? AND completed = 1", (username,))
    goals_completed = c.fetchone()[0]
    conn.close()

    total_minutes = 0
    instrument_minutes = defaultdict(int)
    date_set = set()

    for date_str, duration, instrument in data:
        total_minutes += duration
        instrument_minutes[instrument] += duration
        date_set.add(date_str)

    # Calculate streak
    dates = sorted([datetime.strptime(d, "%Y-%m-%d").date() for d in date_set])
    streak = 1
    max_streak = 1
    for i in range(1, len(dates)):
        if (dates[i] - dates[i - 1]).days == 1:
            streak += 1
            max_streak = max(max_streak, streak)
        else:
            streak = 1

    # Achievement badges
    achievements = []

    if total_minutes >= 60:
        achievements.append(f"🕒 Practiced Over 1000 Minutes! ({total_minutes})")

    if max_streak >= 5:
        achievements.append(f"🔥 {max_streak}-Day Practice Streak!")

    for inst, mins in instrument_minutes.items():
        if mins >= 100:
            achievements.append(f"🎵 {inst} Mastery — {mins} minutes!")

    if goals_completed >= 5:
        achievements.append(f"✅ Completed {goals_completed} Goals!")

    if not achievements:
        achievements.append("⏳ Keep practicing to unlock achievements!")

    return achievements

def create_achievements_frame(parent, username):
    for widget in parent.winfo_children():
        widget.destroy()

    frame = tk.Frame(parent, bg="#F2F6FC")
    frame.pack(fill="both", expand=True, padx=30, pady=30)

    tk.Label(frame, text="🏆 Achievements", font=("Helvetica", 20, "bold"),
             bg="#FFFFFF", fg="#2B2B2B").pack(pady=10)

    achievements = calculate_achievements(username)

    for achievement in achievements:
        badge = tk.Label(frame, text=achievement, font=("Helvetica", 14),
                         bg="#F8F8FF", fg="#2B2B2B", padx=10, pady=8,
                         anchor="w", relief="solid", bd=1)
        badge.pack(fill="x", pady=5)
