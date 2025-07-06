import tkinter as tk
from tkinter import messagebox
import sqlite3
import calendar
from datetime import datetime
from functools import partial

def fetch_practice_data(username):
    conn = sqlite3.connect("music_tracker.db")
    cursor = conn.cursor()
    cursor.execute("SELECT date, instrument, duration, notes FROM practice_sessions WHERE username=?", (username,))
    rows = cursor.fetchall()
    conn.close()

    data = {}
    for date, instrument, duration, notes in rows:
        if date not in data:
            data[date] = []
        data[date].append({
            "instrument": instrument,
            "duration": duration,
            "notes": notes
        })
    return data

def create_calendar_frame(parent, username):
    for widget in parent.winfo_children():
        widget.destroy()

    frame = tk.Frame(parent, bg="#F2F6FC")
    frame.pack(fill="both", expand=True)

    current_date = datetime.today()
    month_var = tk.IntVar(value=current_date.month)
    year_var = tk.IntVar(value=current_date.year)

    def draw_calendar():
        for widget in calendar_frame.winfo_children():
            widget.destroy()

        practice_data = fetch_practice_data(username)
        year = year_var.get()
        month = month_var.get()
        cal = calendar.Calendar()

        # Month Title
        tk.Label(calendar_frame, text=f"{calendar.month_name[month]} {year}",
                 font=("Helvetica", 20, "bold"), bg="#FAFAFC", fg="#2B2B2B").grid(row=0, column=0, columnspan=7, pady=20)

        # Day Headers
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, day in enumerate(days):
            tk.Label(calendar_frame, text=day, font=("Helvetica", 11, "bold"),
                     bg="#3E8EDE", fg="#FFFFFF", width=14, pady=10).grid(row=1, column=i)

        row = 2
        for date in cal.itermonthdates(year, month):
            date_str = date.strftime("%Y-%m-%d")
            is_today = date == datetime.today().date()
            is_current_month = date.month == month

            bg_color = "#FFFFFF"
            if date_str in practice_data:
                bg_color = "#F8C8DC"
            elif not is_current_month:
                bg_color = "#EEEEEE"

            box = tk.Frame(calendar_frame, bg=bg_color, relief="raised", bd=1, width=120, height=80)
            box.grid_propagate(False)
            box.grid(row=row, column=date.weekday(), padx=3, pady=3)

            # Date Number
            date_label = tk.Label(box, text=str(date.day),
                                  font=("Helvetica", 10, "bold"),
                                  bg=bg_color, fg="#2B2B2B")
            date_label.pack(anchor="nw", padx=5, pady=2)

            if is_today and is_current_month:
                today_mark = tk.Label(box, text="Today", font=("Helvetica", 8), bg=bg_color, fg="#3E8EDE")
                today_mark.pack(anchor="ne", padx=5)

            # Show total practice
            if date_str in practice_data:
                total = sum(s["duration"] for s in practice_data[date_str])
                detail_label = tk.Label(box, text=f"{total} min", font=("Helvetica", 9),
                                        bg=bg_color, fg="#2B2B2B")
                detail_label.pack(anchor="center")

                box.bind("<Button-1>", partial(show_details_popup, date_str, practice_data[date_str]))

            if date.weekday() == 6:
                row += 1

        # Legend
        legend_frame = tk.Frame(calendar_frame, bg="#FAFAFC")
        legend_frame.grid(row=row+1, column=0, columnspan=7, pady=10)
        create_legend(legend_frame)

    def show_details_popup(date_str, sessions, event=None):
        info = f"🎯 Practice Details for {date_str}\n"
        for s in sessions:
            info += f"\n🎵 Instrument: {s['instrument']}\n⏱ Duration: {s['duration']} min\n📝 Notes: {s['notes']}\n"
        messagebox.showinfo("Practice Info", info)

    def create_legend(frame):
        items = [
            ("Practiced Day", "#F8C8DC"),
            ("Today", "#3E8EDE"),
            ("Other Month", "#EEEEEE"),
        ]
        for label, color in items:
            b = tk.Frame(frame, bg=color, width=20, height=20)
            b.pack(side="left", padx=5)
            l = tk.Label(frame, text=label, bg="#FAFAFC", font=("Helvetica", 9))
            l.pack(side="left", padx=(0, 15))

    # Navigation Buttons
    nav_frame = tk.Frame(frame, bg="#FAFAFC")
    nav_frame.pack(pady=10)

    def prev_month():
        m, y = month_var.get(), year_var.get()
        if m == 1:
            month_var.set(12)
            year_var.set(y - 1)
        else:
            month_var.set(m - 1)
        draw_calendar()

    def next_month():
        m, y = month_var.get(), year_var.get()
        if m == 12:
            month_var.set(1)
            year_var.set(y + 1)
        else:
            month_var.set(m + 1)
        draw_calendar()

    tk.Button(nav_frame, text="← Previous", command=prev_month,
              bg="#5F5FFF", fg="white", font=("Helvetica", 10, "bold"), width=12).pack(side="left", padx=15)

    tk.Button(nav_frame, text="Next →", command=next_month,
              bg="#5F5FFF", fg="white", font=("Helvetica", 10, "bold"), width=12).pack(side="left", padx=15)

    calendar_frame = tk.Frame(frame, bg="#FAFAFC")
    calendar_frame.pack()

    draw_calendar()

    return frame




