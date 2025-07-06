import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import time

def create_start_practice_frame(parent, username):
    frame = tk.Frame(parent, bg="#F2F6FC")
    frame.pack(fill="both", expand=True)

    # ---------- COLORS & FONTS ----------
    text_color = "#2B2B2B"
    accent_color = "#A084E8"
    button_color = "#CAA9B7"
    font_main = ("Helvetica", 13)
    font_title = ("Helvetica", 24, "bold")
    font_button = ("Helvetica", 12, "bold")
    font_timer = ("Courier", 28, "bold")

    # ---------- TIMER STATE ----------
    start_time = [None]
    timer_id = [None]

    def update_timer():
        if start_time[0]:
            elapsed = int(time.time() - start_time[0])
            hrs = elapsed // 3600
            mins = (elapsed % 3600) // 60
            secs = elapsed % 60
            timer_label.config(text=f"⏱ {hrs:02}:{mins:02}:{secs:02}")
            timer_id[0] = timer_label.after(1000, update_timer)

    def start_practice_timer():
        start_time[0] = time.time()
        start_entry.delete(0, 'end')
        start_entry.insert(0, datetime.now().strftime("%H:%M:%S"))
        update_timer()

    def end_practice_timer():
        end_entry.delete(0, 'end')
        end_entry.insert(0, datetime.now().strftime("%H:%M:%S"))
        if timer_id[0]:
            timer_label.after_cancel(timer_id[0])
            timer_id[0] = None

    # ---------- TITLE ----------
    tk.Label(frame, text="🎵 Start Practice", font=font_title, bg="#FFFFFF", fg=text_color).pack(pady=(30, 10))

    # ---------- TIMER DISPLAY ----------
    timer_frame = tk.Frame(frame, bg="#FFFFFF", bd=1, relief="solid", padx=30, pady=15)
    timer_label = tk.Label(timer_frame, text="⏱ 00:00:00", font=font_timer, bg="#FFFFFF", fg=accent_color)
    timer_label.pack()
    timer_frame.pack(pady=20)

    # ---------- FORM SECTION ----------
    form_frame = tk.Frame(frame, bg="#FFFFFF")
    form_frame.pack(fill="x", padx=100, pady=10)
    form_frame.columnconfigure(1, weight=1)

    def create_label(text, row):
        label = tk.Label(form_frame, text=text, bg="#FFFFFF", fg=text_color, font=font_main)
        label.grid(row=row, column=0, sticky="e", pady=8, padx=(0, 20))

    # ---------- Row 0: Instrument ----------
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Custom.TCombobox",
                    font=font_main,
                    fieldbackground="#FFFFFF",
                    background="#F2F6FC",
                    bordercolor="#040000",
                    borderwidth=1,
                    relief="solid")

    create_label("Select Instrument:", 0)
    instrument_var = tk.StringVar()
    instrument_dropdown = ttk.Combobox(form_frame, textvariable=instrument_var,
                                       values=["Piano", "Violin", "Guitar", "Flute"],
                                       font=font_main, width=35, style="Custom.TCombobox", state="readonly")
    instrument_dropdown.grid(row=0, column=1, sticky="ew", pady=8)

    # ---------- Row 1: Practice Goal ----------
    create_label("Practice Goals:", 1)
    focus_entry = tk.Entry(form_frame, font=font_main,
                           relief="solid", bd=1, highlightthickness=1, highlightbackground="#A084E8")
    focus_entry.grid(row=1, column=1, sticky="ew", pady=8, ipady=3)

    # ---------- Row 2: Start Time ----------
    create_label("Start Time:", 2)
    start_entry = tk.Entry(form_frame, font=font_main,
                           relief="solid", bd=1, highlightthickness=1, highlightbackground="#A084E8")
    start_entry.grid(row=2, column=1, sticky="ew", pady=8, ipady=3)

    # ---------- Row 3: End Time ----------
    create_label("End Time:", 3)
    end_entry = tk.Entry(form_frame, font=font_main,
                         relief="solid", bd=1, highlightthickness=1, highlightbackground="#A084E8")
    end_entry.grid(row=3, column=1, sticky="ew", pady=8, ipady=3)

    # ---------- Row 4: Notes ----------
    create_label("Practice Notes / Reflections:", 4)
    notes_text = tk.Text(form_frame, height=6, font=font_main, wrap="word",
                         relief="solid", bd=1, highlightthickness=1, highlightbackground="#A084E8")
    notes_text.grid(row=4, column=1, sticky="ew", pady=8)

    # ---------- SAVE SESSION ----------
    def save_practice():
        instrument = instrument_var.get()
        focus = focus_entry.get()
        notes = notes_text.get("1.0", "end").strip()
        start_time_val = start_entry.get()
        end_time_val = end_entry.get()

        if not all([instrument, focus, start_time_val, end_time_val]):
            messagebox.showwarning("Missing Info", "Please fill all required fields.")
            return

        try:
            start_dt = datetime.strptime(start_time_val, "%H:%M:%S")
            end_dt = datetime.strptime(end_time_val, "%H:%M:%S")
            duration = int((end_dt - start_dt).total_seconds() / 60)
        except ValueError:
            messagebox.showerror("Time Error", "Start or End Time format should be HH:MM:SS.")
            return

        try:
            conn = sqlite3.connect("practice_tracker.db")  # Change DB name if needed
            cursor = conn.cursor()

            # Ensure table exists with the correct schema
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS practice_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    start_time TEXT,
                    end_time TEXT,
                    duration TEXT,
                    focus TEXT,
                    notes TEXT
                )
            """)

            # Insert practice session
            cursor.execute("""
                INSERT INTO practice_sessions (username, start_time, end_time, duration, focus, notes)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (username, start_time_val, end_time_val, str(duration), focus, notes))

            conn.commit()
            conn.close()

            messagebox.showinfo("Saved", "Practice session saved successfully!")

            # Reset fields
            focus_entry.delete(0, 'end')
            notes_text.delete("1.0", 'end')
            start_entry.delete(0, 'end')
            end_entry.delete(0, 'end')
            instrument_dropdown.set("")
            timer_label.config(text="⏱ 00:00:00")
            start_time[0] = None
            if timer_id[0]:
                timer_label.after_cancel(timer_id[0])
                timer_id[0] = None

        except Exception as e:
            print("Database Error:", e)
            messagebox.showerror("Database Error", str(e))

    # ---------- BUTTONS ----------
    button_frame = tk.Frame(frame, bg=  "#F2F6FC")
    button_frame.pack(pady=20)

    start_btn = tk.Button(button_frame, text="▶ Start Timer", command=start_practice_timer,
                          bg=accent_color, fg="white", font=font_button, width=18,
                          relief="flat", bd=2, activebackground="#7B66FF", activeforeground="white")
    start_btn.pack(side="left", padx=20, ipadx=4, ipady=6)

    end_btn = tk.Button(button_frame, text="⏹ End Timer", command=end_practice_timer,
                        bg=accent_color, fg="white", font=font_button, width=18,
                        relief="flat", bd=2, activebackground="#7B66FF", activeforeground="white")
    end_btn.pack(side="left", padx=20, ipadx=4, ipady=6)

    # ---------- SAVE BUTTON ----------
    tk.Button(frame, text="💾 Save Session", command=save_practice,
              bg=button_color, fg=text_color, font=font_button, width=25).pack(pady=30)

    return frame









