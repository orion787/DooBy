import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from dooby.core import get_session
from dooby.gui.edit_page import EditWindow

class DooByApp:
    def __init__(self, root, model_class, title="DooBy App", logo_path=None, icon_path=None):
        self.root = root
        self.model_class = model_class
        self.session = get_session()
        self.logo_img = None

        root.title(title)
        if icon_path:
            root.iconbitmap(icon_path)
        if logo_path:
            logo = Image.open(logo_path).resize((100, 100))
            self.logo_img = ImageTk.PhotoImage(logo)
            tk.Label(root, image=self.logo_img).pack(pady=10)

        # Кнопка "Добавить партнёра"
        ttk.Button(root, text="➕ Добавить партнёра", command=self.add_partner).pack(pady=(0, 10))

        self.canvas = tk.Canvas(root)
        self.scroll_y = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.frame = ttk.Frame(self.canvas)

        self.frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scroll_y.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scroll_y.pack(side="right", fill="y")

        self.render()

    def render(self):
        # Очистка предыдущих карточек
        for widget in self.frame.winfo_children():
            widget.destroy()

        records = self.session.query(self.model_class).all()
        for r in records:
            self.render_card(r)

    def render_card(self, record):
        box = ttk.Frame(self.frame, relief="solid", borderwidth=1, padding=10)
        box.pack(fill="x", padx=10, pady=5)
        box.bind("<Button-1>", lambda e: self.edit_partner(record))  # Клик для редактирования

        top = ttk.Frame(box)
        top.pack(fill="x")
        ttk.Label(top, text=f"{record.type} | {record.name}", font=("Arial", 12, "bold")).pack(side="left")
        ttk.Label(top, text=f"{record.discount:.0f}%", font=("Arial", 12)).pack(side="right")

        ttk.Label(box, text=record.director).pack(anchor="w")
        ttk.Label(box, text=self.format_phone(record.phone)).pack(anchor="w")
        ttk.Label(box, text=f"Рейтинг: {record.rating}").pack(anchor="w")
        ttk.Label(box, text=f"Продаж на сумму: {record.total_sales:.2f} руб.").pack(anchor="w")

    def format_phone(self, phone):
        digits = ''.join(filter(str.isdigit, phone))
        if digits.startswith("7"):
            digits = digits[1:]
        if len(digits) == 10:
            return f"+7 {digits[0:3]} {digits[3:6]} {digits[6:8]} {digits[8:10]}"
        return phone

    def add_partner(self):
        EditWindow(self, self.model_class, self.session)

    def edit_partner(self, record):
        EditWindow(self, self.model_class, self.session, partner=record)

    def refresh(self):
        """Обновление карточек после редактирования"""
        self.render()
