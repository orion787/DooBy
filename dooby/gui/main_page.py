import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from dooby.core import get_session
from dooby.gui.edit_page import EditWindow
from dooby.gui.ui_layout_config import UILayoutConfig

class DooByApp:
    def __init__(self, root, model_class, title="DooBy App", 
                 logo_path=None, icon_path=None, 
                 ui_config: UILayoutConfig = None):
        self.root = root
        self.model_class = model_class
        self.session = get_session()
        self.logo_img = None
        self.ui_config = ui_config or UILayoutConfig(model_class)

        root.title(title)
        self.setup_ui(logo_path, icon_path)
        self.render()

    def setup_ui(self, logo_path, icon_path):
        if icon_path:
            self.root.iconbitmap(icon_path)
        if logo_path:
            logo = Image.open(logo_path).resize((100, 100))
            self.logo_img = ImageTk.PhotoImage(logo)
            tk.Label(self.root, image=self.logo_img).pack(pady=10)

        ttk.Button(self.root, text="➕ Добавить", command=self.add_record).pack(pady=(0, 10))

        self.canvas = tk.Canvas(self.root)
        self.scroll_y = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.frame = ttk.Frame(self.canvas)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scroll_y.pack(side="right", fill="y")

        self.frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scroll_y.set)

    def render(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        for record in self.session.query(self.model_class).all():
            self.render_card(record)

    def render_card(self, record):
        card_frame = ttk.Frame(self.frame, relief="solid", borderwidth=1, padding=10)
        card_frame.pack(fill="x", padx=10, pady=5, expand=True)
        card_frame.bind("<Button-1>", lambda e, r=record: self.edit_record(r))

        # Сортировка строк по номеру
        sorted_rows = sorted(self.ui_config.layout.items(), key=lambda x: x[0])
        
        for row_num, fields in sorted_rows:
            row_frame = ttk.Frame(card_frame)
            row_frame.pack(fill="x", pady=2)
            
            for field in fields:
                if not hasattr(record, field):
                    continue
                    
                value = getattr(record, field)
                if field in self.ui_config.special_widgets:
                    value = self.format_special_field(field, value)
                
                label_text = self.ui_config.field_labels.get(field, field)
                ttk.Label(row_frame, text=f"{label_text}: {value}").pack(side="left", padx=5)

    def format_special_field(self, field, value):
        widget_type, _ = self.ui_config.special_widgets.get(field, (None, None))
        
        if widget_type == 'phone':
            return self.format_phone(value)
        elif widget_type == 'currency':
            return f"{value:.2f} руб."
        return value

    def format_phone(self, phone):
        digits = ''.join(filter(str.isdigit, str(phone)))
        if digits.startswith("7"):
            digits = digits[1:]
        if len(digits) == 10:
            return f"+7 {digits[0:3]} {digits[3:6]} {digits[6:8]} {digits[8:10]}"
        return phone

    def add_record(self):
        EditWindow(self, self.model_class, self.session, self.ui_config)

    def edit_record(self, record):
        EditWindow(self, self.model_class, self.session, self.ui_config, record)

    def refresh(self):
        self.render()
