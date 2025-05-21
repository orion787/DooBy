import tkinter as tk
from tkinter import ttk, messagebox

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
        cb = ttk.Combobox(self, values=["Оптовик", "Розничный", "Дистрибьютор", "ООО", "ОАО", "ЗАО"])
        cb.grid(row=1, column=1, padx=10, pady=5)
        self.fields["type"] = cb

        # Кнопки
        ttk.Button(self, text="💾 Сохранить", command=self.save).grid(row=10, column=0, columnspan=2, pady=15)
        ttk.Button(self, text="⬅️ Назад", command=self.destroy).grid(row=11, column=0, columnspan=2)

        if self.partner:
            self.load_data()

    def load_data(self):
        """Заполнить форму существующими данными"""
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
