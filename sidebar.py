import tkinter as tk

def create_sidebar(parent, on_nav_click=None):
    # Color palette
    bg_color = "#F2F6FC"
    card_bg = "#FFFFFF"
    accent_color = "#A2679C"
    accent_alt = "#27AE60"
    text_main = "#FFFFFF"
    text_secondary = "#000000"

    sidebar_bg = "#C4DEDE"
    content_bg = accent_color
    button_default_bg = "#A373A6"       # This is your main button color
    button_hover_bg = "#9D6CA3"         # On hover
    button_fg = text_main

    sidebar = tk.Frame(parent, bg="#6F99AE", width=200)
    sidebar.pack(side="left", fill="y")

    menu_items = [
        ("Dashboard", "📊"),
        ("Start Practice", "🎵"),
        ("Practice History", "📅"),
        ("Goals", "🎯"),
        ("Practice Notes", "📝"),
        ("Analysis by Graph", "📈"),
        ("Achievements", "🏆"),
        ("Practice Calendar", "📆"),
        ("Logout", "🚪")
    ]

    content_wrapper = tk.Frame(sidebar, bg="#CAA8C7")
    content_wrapper.pack(fill="both", expand=True)

    def on_enter(event):
        event.widget.config(bg=button_hover_bg)

    def on_leave(event):
        event.widget.config(bg=button_default_bg)

    for label, icon in menu_items:
        btn_frame = tk.Frame(content_wrapper, bg=content_bg,
                             highlightbackground=content_bg, highlightthickness=1, bd=0)
        btn_frame.pack(fill="x", padx=10, pady=5, expand=True)

        btn = tk.Button(
            btn_frame,
            text=f"{icon}  {label}",
            font=("Helvetica", 14),
            fg=button_fg,
            bg=button_default_bg,
            activebackground=button_hover_bg,
            activeforeground=button_fg,
            relief="flat",
            anchor="w",
            padx=20,
            pady=12,
            command=lambda l=label: on_nav_click(l) if on_nav_click else None
        )
        btn.pack(fill="x")

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

    return sidebar
