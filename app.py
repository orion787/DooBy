from collections import defaultdict
from tkinter import Tk
from dooby.core import init_db
from dooby.gui.main_page import DooByApp
from dooby.gui.ui_layout_config import *
from models import Partner


#Инициализируем БД
engine = init_db("partners.db")
ui_config = UILayoutConfig(Partner)
ui_config.excluded_fields.append('fideninfo')

# Настраиваем лейаут
ui_config.set_background_color("#F0F0F0")
ui_config.set_card_background(Colors.lightblue)
ui_config.set_alignment('left_custom_spacing')
ui_config.set_inter_element_spacing(40)
ui_config.set_card_spacing(10)
ui_config.set_font(('Arial', 14))


ui_config.layout = defaultdict(list, {
    1: ['type', 'name', 'discount'],
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
