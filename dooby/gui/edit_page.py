import tkinter as tk
from tkinter import ttk, messagebox

class EditWindow(tk.Toplevel):
    def __init__(self, parent_app, model_class, session, ui_config, record=None):
        super().__init__(parent_app.root)
        self.parent_app = parent_app
        self.model_class = model_class
        self.session = session
        self.record = record
        self.ui_config = ui_config
        self.widgets = {}

        self.title("Редактирование" if record else "Добавление")
        self.build_form()

    def build_form(self):
        main_frame = ttk.Frame(self)
        main_frame.pack(padx=10, pady=10, fill="both", expand=True)

        sorted_rows = sorted(self.ui_config.layout.items(), key=lambda x: x[0])

        for row_num, fields in sorted_rows:
            row_frame = ttk.Frame(main_frame)
            row_frame.pack(fill="x", pady=5)

            for field in fields:
                if not self.is_read_only_property(field):
                    self.create_field_widget(row_frame, field)

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="💾 Сохранить", command=self.save).pack(side="left", padx=5)
        ttk.Button(button_frame, text="⬅️ Отмена", command=self.destroy).pack(side="left", padx=5)

        if self.record:
            self.load_data()

    def create_field_widget(self, parent, field):
        frame = ttk.Frame(parent)
        frame.pack(side="left", padx=5, expand=True)

        label_text = self.ui_config.field_labels.get(field, field)
        ttk.Label(frame, text=label_text).pack(anchor="w")

        widget_type, options = self.ui_config.special_widgets.get(field, (None, None))

        if widget_type == 'combobox':
            widget = ttk.Combobox(frame, values=options)
        elif widget_type == 'phone':
            widget = ttk.Entry(frame, validate="key")
            widget.configure(validatecommand=(widget.register(self.validate_phone), '%P'))
        elif widget_type == 'currency':
            widget = ttk.Entry(frame, validate="key")
            widget.configure(validatecommand=(widget.register(self.validate_currency), '%P'))
        else:
            widget = ttk.Entry(frame)

        widget.pack(fill="x")
        self.widgets[field] = widget

    def validate_phone(self, value):
        return all(c in '+0123456789 ()-' for c in value)

    def validate_currency(self, value):
        if value.replace('.', '', 1).isdigit():
            return True
        return False

    def load_data(self):
        for field, widget in self.widgets.items():
            value = getattr(self.record, field, "")
            if isinstance(widget, ttk.Combobox):
                widget.set(str(value))
            else:
                widget.delete(0, tk.END)
                widget.insert(0, str(value))

    def save(self):
        try:
            data = {}
            for field, widget in self.widgets.items():
                value = widget.get()
                if value == "":
                    raise ValueError(f"Поле '{field}' не может быть пустым")
                if field in self.ui_config.special_widgets:
                    value = self.process_special_field(field, value)
                data[field] = value

            self.validate_data(data)

            if self.record:
                record = self.record
            else:
                record = self.model_class()

            for field, value in data.items():
                if not self.is_read_only_property(field):
                    setattr(record, field, value)

            self.session.add(record)
            self.session.commit()

            messagebox.showinfo("Успешно", "Данные сохранены")
            self.parent_app.refresh()
            self.destroy()

        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def process_special_field(self, field, value):
        widget_type, _ = self.ui_config.special_widgets.get(field)

        if widget_type == 'currency':
            return float(value)
        elif widget_type == 'phone':
            return ''.join(filter(str.isdigit, value))
        return value

    def validate_data(self, data):
        required_fields = [
            field for field, (wt, _) in self.ui_config.special_widgets.items()
            if wt == 'required'
        ]
        for field in required_fields:
            if not data.get(field):
                raise ValueError(f"Поле '{field}' обязательно для заполнения")

    def is_read_only_property(self, field):
        """
        Проверяет, является ли поле свойством только для чтения.
        """
        attr = getattr(self.model_class, field, None)
        if isinstance(attr, property):
            return attr.fset is None
        return False
