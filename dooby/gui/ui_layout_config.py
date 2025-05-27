from sqlalchemy import inspect
from collections import defaultdict
from typing import List


class UILayoutConfig:
    def __init__(self, model_class):
        self.model_class = model_class
        self.excluded_fields = ['id', 'hideninfo']
        self.field_labels = {}
        self.field_suffix = {}
        self.special_widgets = {}
        self.layout = defaultdict(list)
        
        self.background_color = 'white'          # Основной цвет фона
        self.card_background = 'white'           # Цвет фона карточек
        self.alignment = 'left'                  # Выравнивание: left/center/right
        self.element_spacing = 5                 # Отступ между элементами в ряду
        self.card_spacing = 5                    # Отступ между карточками
        self.font_body = ('Arial', 10)           # Шрифт текста
        self.accent_color = '#E1E1E1'          # Цвет акцентов
        self.inter_element_spacing = 5           # Отступ между элементами для left_custom_spacing

        inspector = inspect(model_class)
        fields = [c.name for c in inspector.mapper.columns if c.name not in self.excluded_fields]
        for i, field in enumerate(fields, 1):
            self.layout[i].append(field)

    @staticmethod
    def add_row(self, row_number: int, fields: List[str]):
        self.layout[row_number].extend(fields)
        
    def set_field_label(self, field: str, label: str):
        self.field_labels[field] = label
        
    def set_field_suffix(self, field: str, suffix: str):
        self.field_suffix[field] = suffix
        
    def set_special_widget(self, field: str, widget_type: str, options: list = None):
        self.special_widgets[field] = (widget_type, options)
        
    # Методы для настройки стилей
    def set_background_color(self, color: str):
        """Доступные цвета: white, lightgrey, lightblue, #hex-код"""
        self.background_color = color
        
    def set_card_background(self, color: str):
        self.card_background = color
        
    def set_alignment(self, align: str):
        """Варианты: left, center, right, first_left, left_custom_spacing"""
        valid_alignments = ['left', 'center', 'right', 'first_left', 'left_custom_spacing']
        if align not in valid_alignments:
            raise ValueError(f"Недопустимое выравнивание. Допустимые значения: {', '.join(valid_alignments)}")
        self.alignment = align
        
    def set_inter_element_spacing(self, pixels: int):
        """Устанавливает отступ между элементами для left_custom_spacing"""
        self.inter_element_spacing = pixels
        
    def set_element_spacing(self, pixels: int):
        self.element_spacing = pixels
        
    def set_card_spacing(self, pixels: int):
        self.card_spacing = pixels
        
    def set_font(self, font_tuple: tuple):
        self.font_body = font_tuple


class Colors():
    default = None
    white = '#FFFFFF'   
    lightgrey = '#F0F0F0'
    lightblue = "#B9D7F1"
    seashell = '#FFF5EE'
    peach = '#fdd9b5'
    smoke = '#F0F0F0'
    gray = '#b5b8b1'
