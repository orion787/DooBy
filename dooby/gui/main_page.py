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
        root.configure(bg=self.ui_config.background_color)
        self._build_ui(logo_path, icon_path)
        self._populate()

    def _build_ui(self, logo_path, icon_path):
        if icon_path:
            self.root.iconbitmap(icon_path)
        if logo_path:
            logo = Image.open(logo_path).resize((100, 100))
            self.logo_img = ImageTk.PhotoImage(logo)
            tk.Label(self.root, image=self.logo_img, 
                    bg=self.ui_config.background_color).pack(pady=10)

        btn_style = ttk.Style()
        btn_style.configure('Accent.TButton', background=self.ui_config.accent_color)
        
        ttk.Button(self.root, text="➕ Добавить", 
                 command=self.add_record, style='Accent.TButton').pack(pady=(0,10))

        container = tk.Frame(self.root, bg=self.ui_config.background_color)
        container.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(container, bg=self.ui_config.background_color, 
                               highlightthickness=0)
        self.v_scroll = ttk.Scrollbar(container, orient="vertical", 
                                    command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.v_scroll.set)

        self.scrollable_frame = tk.Frame(self.canvas, 
                                        bg=self.ui_config.background_color)
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
        card = tk.Frame(self.scrollable_frame, 
                    bg=self.ui_config.card_background,
                    bd=1, 
                    relief='solid',
                    padx=10,
                    pady=5)
        card.pack(fill="x", padx=10, pady=self.ui_config.card_spacing)
        card.bind("<Button-1>", lambda e, r=record: self.edit_record(r))

        rows = sorted(self.ui_config.layout.items(), key=lambda x: x[0])
        for _, fields in rows:
            row = tk.Frame(card, bg=self.ui_config.card_background)
            row.pack(fill="x", pady=2)

            # Конфигурация колонок
            for col_idx in range(len(fields)):
                if self.ui_config.alignment == 'first_left':
                    weight = 1 if col_idx > 0 else 0
                    row.columnconfigure(col_idx, weight=weight, uniform='group1')
                else:
                    row.columnconfigure(col_idx, weight=1)

            if self.ui_config.alignment == 'left_custom_spacing':
                for col_idx in range(len(fields)):
                    row.columnconfigure(col_idx, weight=0)  # Отключаем растягивание


            for idx, field in enumerate(fields):
                if not hasattr(record, field):
                    continue

                raw = getattr(record, field)
                if field in self.ui_config.special_widgets:
                    raw = self._format_special(field, raw)

                label = self.ui_config.field_labels.get(field, "")
                suffix = self.ui_config.field_suffix.get(field, "")

                text = f"{label} {raw}{suffix}"
                
                # Определение параметров отображения
                if self.ui_config.alignment == 'left_custom_spacing':
                    anchor = 'w'
                    sticky = 'w'
                    # Отступ только справа для всех кроме последнего элемента
                    padx = (0, self.ui_config.inter_element_spacing) if idx < len(fields)-1 else (0, 0)
                elif self.ui_config.alignment == 'first_left':
                    anchor = 'w' if idx == 0 else 'center'
                    sticky = 'w' if idx == 0 else 'ew'
                    padx = (self.ui_config.element_spacing, self.ui_config.element_spacing)
                else:
                    anchor = {
                        'left': 'w',
                        'center': 'center',
                        'right': 'e'
                    }[self.ui_config.alignment]
                    sticky = 'ew'
                    padx = (self.ui_config.element_spacing, self.ui_config.element_spacing)

                lbl = tk.Label(row, 
                            text=text, 
                            bg=self.ui_config.card_background,
                            font=self.ui_config.font_body,
                            anchor=anchor)
                lbl.grid(row=0, column=idx, 
                        sticky=sticky, 
                        padx=padx,
                        pady=0)

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
