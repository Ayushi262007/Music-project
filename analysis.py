import tkinter as tk
from tkinter import ttk
import sqlite3
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import defaultdict

def fetch_practice_data(username, start_date=None, end_date=None):
    conn = sqlite3.connect("music_tracker.db")
    c = conn.cursor()

    if start_date and end_date:
        c.execute("""
            SELECT date, duration, instrument FROM practice_sessions 
            WHERE username = ? AND date BETWEEN ? AND ?
        """, (username, start_date, end_date))
    else:
        c.execute("SELECT date, duration, instrument FROM practice_sessions WHERE username = ?", (username,))
        
    rows = c.fetchall()
    conn.close()
    return rows

def create_analysis_frame(parent, username):
    for widget in parent.winfo_children():
        widget.destroy()

    frame = tk.Frame(parent, bg="#F2F6FC")
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="📈 Practice Analysis", font=("Helvetica", 20, "bold"),
             bg="#FFFFFF", fg="#2B2B2B").pack(pady=10)

    # ---------- Date Filter UI ----------
    filter_frame = tk.Frame(frame, bg="#FFFFFF")
    filter_frame.pack(pady=5)

    tk.Label(filter_frame, text="From (YYYY-MM-DD):", font=("Helvetica", 10), bg="#FFFFFF").grid(row=0, column=0, padx=5)
    start_entry = tk.Entry(filter_frame, font=("Helvetica", 10), width=12)
    start_entry.grid(row=0, column=1)

    tk.Label(filter_frame, text="To (YYYY-MM-DD):", font=("Helvetica", 10), bg="#FFFFFF").grid(row=0, column=2, padx=5)
    end_entry = tk.Entry(filter_frame, font=("Helvetica", 10), width=12)
    end_entry.grid(row=0, column=3)

    def render_graphs(start=None, end=None):
        nonlocal frame  # use existing frame
        for widget in frame.winfo_children():
            if isinstance(widget, tk.Frame) and widget not in [filter_frame]:
                widget.destroy()

        # ---------- Data ----------
        data = fetch_practice_data(username, start, end)
        instruments = set()
        day_instrument_duration = defaultdict(lambda: defaultdict(int))
        instrument_data = defaultdict(int)

        for date_str, duration, instrument in data:
            try:
                day = datetime.strptime(date_str, "%Y-%m-%d").strftime("%A")
                instruments.add(instrument)
                day_instrument_duration[day][instrument] += duration
                instrument_data[instrument] += duration
            except Exception as e:
                print("Date format error:", e)

        instruments = sorted(list(instruments))
        days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

        # ---------- Chart Frame ----------
        chart_frame = tk.Frame(frame, bg="#FFFFFF")
        chart_frame.pack(fill="both", expand=True, padx=20, pady=10)
        chart_frame.columnconfigure(0, weight=1)
        chart_frame.columnconfigure(1, weight=1)
        chart_frame.rowconfigure(0, weight=1)

        # ---------- Bar Chart ----------
        bar_fig, bar_ax = plt.subplots(figsize=(8, 4), dpi=100)
        x = range(len(days_order))
        bar_width = 0.8 / len(instruments) if instruments else 0.8
        colors = plt.cm.tab10.colors

        for i, instrument in enumerate(instruments):
            y_vals = [day_instrument_duration[day].get(instrument, 0) for day in days_order]
            offset = [xi + i * bar_width for xi in x]
            bar_ax.bar(offset, y_vals, width=bar_width, label=instrument, color=colors[i % len(colors)])

        bar_ax.set_xticks([xi + bar_width * (len(instruments) / 2 - 0.5) for xi in x])
        bar_ax.set_xticklabels(days_order, rotation=45, ha="right")
        bar_ax.set_ylabel("Minutes")
        bar_ax.set_title("Daily Practice Duration per Instrument")
        bar_ax.legend(title="Instrument")
        bar_fig.tight_layout()

        bar_canvas = FigureCanvasTkAgg(bar_fig, master=chart_frame)
        bar_canvas.draw()
        bar_widget = bar_canvas.get_tk_widget()
        bar_widget.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # ---------- Pie Chart ----------
        if instrument_data:
            pie_fig, pie_ax = plt.subplots(figsize=(5, 4), dpi=100)
            labels = list(instrument_data.keys())
            sizes = list(instrument_data.values())
            pie_ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
            pie_ax.set_title("Total Practice Time per Instrument")
            pie_fig.tight_layout()

            pie_canvas = FigureCanvasTkAgg(pie_fig, master=chart_frame)
            pie_canvas.draw()
            pie_widget = pie_canvas.get_tk_widget()
            pie_widget.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        else:
            tk.Label(chart_frame, text="No instrument data available.",
                     font=("Helvetica", 12), fg="#888888", bg="#FFFFFF").grid(row=0, column=1, padx=10, pady=10)

    # ---------- Filter Button ----------
    def on_filter():
        start = start_entry.get().strip()
        end = end_entry.get().strip()
        try:
            # validate format
            if start: datetime.strptime(start, "%Y-%m-%d")
            if end: datetime.strptime(end, "%Y-%m-%d")
            render_graphs(start, end)
        except ValueError:
            tk.messagebox.showerror("Invalid Date", "Please enter valid dates in YYYY-MM-DD format.")

    filter_btn = tk.Button(filter_frame, text="Filter", font=("Helvetica", 10, "bold"),
                           command=on_filter, bg="#A084E8", fg="white")
    filter_btn.grid(row=0, column=4, padx=10)

    # ---------- Default View (last 7 days) ----------
    today = datetime.today().date()
    last_week = today - timedelta(days=6)
    start_entry.insert(0, str(last_week))
    end_entry.insert(0, str(today))
    render_graphs(str(last_week), str(today))




