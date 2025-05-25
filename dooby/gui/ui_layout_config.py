from sqlalchemy import inspect
from collections import defaultdict
from typing import List

class UILayoutConfig:
    def __init__(self, model_class):
        self.model_class = model_class
        self.excluded_fields = ['id', 'hideninfo']
        self.field_labels = {}     # подписи до значения
        self.field_suffix = {}     # **новое**: текст после значения
        self.special_widgets = {}
        self.layout = defaultdict(list)
        
        inspector = inspect(model_class)
        fields = [c.name for c in inspector.mapper.columns if c.name not in self.excluded_fields]
        for i, field in enumerate(fields, 1):
            self.layout[i].append(field)

    def add_row(self, row_number: int, fields: List[str]):
        self.layout[row_number].extend(fields)
        
    def set_field_label(self, field: str, label: str):
        """Текст перед значением"""
        self.field_labels[field] = label
        
    def set_field_suffix(self, field: str, suffix: str):
        """Текст после значения"""
        self.field_suffix[field] = suffix
        
    def set_special_widget(self, field: str, widget_type: str, options: list = None):
        self.special_widgets[field] = (widget_type, options)
