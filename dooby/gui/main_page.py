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
        root.configure(bg='white')
        self._build_ui(logo_path, icon_path)
        self._populate()

    def _build_ui(self, logo_path, icon_path):
        if icon_path:
            self.root.iconbitmap(icon_path)
        if logo_path:
            logo = Image.open(logo_path).resize((100, 100))
            self.logo_img = ImageTk.PhotoImage(logo)
            tk.Label(self.root, image=self.logo_img, bg='white').pack(pady=10)

        ttk.Button(self.root, text="➕ Добавить", command=self.add_record).pack(pady=(0,10))

        container = tk.Frame(self.root, bg='white')
        container.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(container, bg='white', highlightthickness=0)
        self.v_scroll = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.v_scroll.set)

        self.scrollable_frame = tk.Frame(self.canvas, bg='white')
        self.scrollable_window = self.canvas.create_window((0,0),
                                                           window=self.scrollable_frame,
                                                           anchor="nw")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.pack(side="left", fill="both", expand=True)
        self.v_scroll.pack(side="right", fill="y")

        self.canvas.bind("<Configure>", self._on_canvas_resize)

    def _on_canvas_resize(self, event):
        self.canvas.itemconfig(self.scrollable_window, width=event.width)
        self._populate()

    def _populate(self):
        for w in self.scrollable_frame.winfo_children():
            w.destroy()
        for record in self.session.query(self.model_class).all():
            self._render_card(record)

    def _render_card(self, record):
        card = tk.Frame(self.scrollable_frame, bg='white', bd=1, relief='solid')
        card.pack(fill="x", padx=10, pady=5)
        card.bind("<Button-1>", lambda e, r=record: self.edit_record(r))

        FONT_BODY = ("Arial", 10)
        rows = sorted(self.ui_config.layout.items(), key=lambda x: x[0])
        for _, fields in rows:
            row = tk.Frame(card, bg='white')
            row.pack(fill="x", pady=2, padx=5)

            cols = len(fields)
            for idx, field in enumerate(fields):
                row.columnconfigure(idx, weight=1)
                if not hasattr(record, field):
                    continue

                raw = getattr(record, field)
                if field in self.ui_config.special_widgets:
                    raw = self._format_special(field, raw)

                label = self.ui_config.field_labels.get(field, field)
                suffix = self.ui_config.field_suffix.get(field, "")

                text = f"{label}: {raw}{suffix}"

                lbl = tk.Label(row, text=text, bg='white', font=FONT_BODY, anchor="w")
                lbl.grid(row=0, column=idx, sticky="ew", padx=5)

    def _format_special(self, field, value):
        wtype, _ = self.ui_config.special_widgets[field]
        if wtype == 'phone':
            return self.format_phone(value)
        if wtype == 'currency':
            return f"{value:.2f}"
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
        self._populate()
