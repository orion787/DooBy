from collections import defaultdict
from tkinter import Tk
from dooby.core import init_db
from dooby.gui.main_page import DooByApp
from dooby.gui.ui_layout_config import *
from models import Partner


#Инициализируем БД
engine = init_db("partners.db")

#Иницилиазция лейаута для UI
ui_config = UILayoutConfig(Partner)

#Отказываемся от отображения поля hideninfo
ui_config.excluded_fields.append('hideninfo')

# Настраиваем лейаут
ui_config.set_background_color(Colors.smoke)       #Цвет окна
ui_config.set_card_background(Colors.lightblue)    #Цвет карточки
ui_config.set_alignment('left_custom_spacing')     #Выравние в пределах картчоки (доступны: left, center, right, left_custom_spacing)
ui_config.set_inter_element_spacing(40)            #Отступ между полями для left_custom_spacing
ui_config.set_card_spacing(10)                     #Отступ между карточками
ui_config.set_font(('Arial', 12))                  #Выбор шрифта и кегеля


#Настройка построчного отображения полей
ui_config.layout = defaultdict(list, {
    1: ['type', 'name', 'discount'],
    2: ['phone'],
    3: ['director'],
    4: ['rating']
})


#Настройка отображенияя текста до и после поля, а также в режиме добавления
ui_config.set_field_label('name', 'Наименование :')                             #Перед полем 
ui_config.set_field_label('type', 'Тип организации :')                          
ui_config.set_field_label('discount', 'Скидка :')                               
ui_config.set_field_suffix('discount', '%')                                     #После поля
ui_config.set_field_label('phone', 'Телефон :')
ui_config.set_special_widget('type', 'combobox', ['ООО', 'ИП', 'АО'])           #Выбор для режима добавления
ui_config.set_special_widget('phone', 'phone')
ui_config.set_field_label('director', 'Директор :')
ui_config.set_field_label('rating', 'Рейтинг :')


#Main()
root = Tk()
app = DooByApp(root, Partner, title="Учет партнёров", logo_path="resources//logo.png", ui_config=ui_config)
root.mainloop()
