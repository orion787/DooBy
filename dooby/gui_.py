"""

import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from dooby.core import get_session

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
        self.render()




class EditWindow(tk.Toplevel):
    def __init__(self, parent_app, model_class, session, partner=None):
        super().__init__(parent_app.root)
        self.parent_app = parent_app
        self.model_class = model_class
        self.session = session
        self.partner = partner

        self.title("Редактирование партнёра" if partner else "Добавление партнёра")

        self.fields = {}
        self.build_form()

    def build_form(self):
        labels = [
            ("Наименование", "name"),
            ("Тип партнёра", "type"),
            ("Рейтинг", "rating"),
            ("Адрес", "address"),
            ("ФИО директора", "director"),
            ("Телефон", "phone"),
            ("Email", "email")
        ]

        for i, (label_text, field_name) in enumerate(labels):
            ttk.Label(self, text=label_text).grid(row=i, column=0, sticky="w", padx=10, pady=5)
            entry = ttk.Entry(self, width=40)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.fields[field_name] = entry

        # Выпадающий список для типа
        self.fields["type"].destroy()
        cb = ttk.Combobox(self, values=["ООО", "ОАО", "ЗАО", "Оптовик", "Розничный", "Дистрибьютор"])
        cb.grid(row=1, column=1, padx=10, pady=5)
        self.fields["type"] = cb

        # Кнопки
        ttk.Button(self, text="💾 Сохранить", command=self.save).grid(row=10, column=0, columnspan=2, pady=15)
        ttk.Button(self, text="⬅️ Назад", command=self.destroy).grid(row=11, column=0, columnspan=2)

        if self.partner:
            self.load_data()

    def load_data(self):
        for field, widget in self.fields.items():
            widget.delete(0, tk.END)
            widget.insert(0, getattr(self.partner, field))

    def save(self):
        try:
            name = self.fields["name"].get().strip()
            type_ = self.fields["type"].get().strip()
            rating = int(self.fields["rating"].get().strip())
            address = self.fields["address"].get().strip()
            director = self.fields["director"].get().strip()
            phone = self.fields["phone"].get().strip()
            email = self.fields["email"].get().strip()

            if not name or rating < 0:
                raise ValueError("Имя обязательно, рейтинг должен быть неотрицательным числом")

            if self.partner:
                partner = self.partner
            else:
                partner = self.model_class()

            partner.name = name
            partner.type = type_
            partner.rating = rating
            partner.address = address
            partner.director = director
            partner.phone = phone
            partner.email = email

            self.session.add(partner)
            self.session.commit()

            messagebox.showinfo("Успешно", "Данные партнёра сохранены.")
            self.parent_app.refresh()
            self.destroy()

        except ValueError as ve:
            messagebox.showerror("Ошибка ввода", str(ve))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка:\n{e}")
"""