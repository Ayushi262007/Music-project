# topbar.py
import tkinter as tk

def create_topbar(parent, on_minimize, on_close):
    sidebar_bg = "#A2679C"     # Matches sidebar background
    button_fg = "#FFFFFF"
      

    topbar = tk.Frame(parent, bg=sidebar_bg, height=40)
    topbar.pack(fill="x", side="top")

    # Title
    title = tk.Label(topbar, text="🎵 Music Practice Tracker", font=("Helvetica", 18, "bold"),
                     bg=sidebar_bg, fg=button_fg, padx=10)
    title.pack(side="left")

    # Close Button (X)
    close_btn = tk.Button(topbar, text="✕", command=on_close, font=("Arial", 12),
                          bg=sidebar_bg, fg=button_fg, activebackground="#D9534F",
                          relief="flat", padx=8, pady=2)
    close_btn.pack(side="right", padx=5)

    # Minimize Button (–)
    minimize_btn = tk.Button(topbar, text="–", command=on_minimize, font=("Arial", 12),
                             bg=sidebar_bg, fg=button_fg, activebackground="#CCCCCC",
                             relief="flat", padx=8, pady=2)
    minimize_btn.pack(side="right")

    return topbar



