from collections import defaultdict
from tkinter import Tk
from dooby.core import init_db
from dooby.gui.main_page import DooByApp
from dooby.gui.ui_layout_config import UILayoutConfig
from models import Partner

#Инициализируем БД
engine = init_db("partners.db")


#Инициализация контекста модели
ui_config = UILayoutConfig(Partner)
ui_config.excluded_fields.append('fideninfo')


# Настраиваем лейаут
ui_config.layout = defaultdict(list, {
    1: ['name', 'type', 'discount'],
    2: ['phone'],
    3: ['director'],
    4: ['rating']
})


ui_config.set_field_label('name', 'Наименование')
ui_config.set_field_label('type', 'Тип организации')
ui_config.set_field_label('discount', 'Скидка')
ui_config.set_field_suffix('discount', '%') 
ui_config.set_field_label('phone', 'Телефон')
ui_config.set_special_widget('type', 'combobox', ['ООО', 'ИП', 'АО'])
ui_config.set_special_widget('phone', 'phone')


#Main()
root = Tk()
app = DooByApp(root, Partner, title="Учет партнёров", logo_path="resources//logo.png", ui_config=ui_config)
root.mainloop()
