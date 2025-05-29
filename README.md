# 🐹 DooBy 
*(FOR EDUCATIONAL PURPOSES)*  

**Database engine for automating work with domain (models in SqLite) and UI generation**

---

### 📋 Requirements
tk, pillow, sqlalchemy

---

📄 *Readme is written for my educational institution (you can translate it using a translator from Russian).*

---

### 📖 **Описание проекта**
Данный проект автоматизует работу с сущностью из какой-либо предметной области. Сущность (в данном проекте) представлят из себя описанный с помощью dooby.fields объект, хранящийся в БД SQLite. Библиотека автоматически генерирует GUI (tkinter) для работы с этой модeлью, но вы можете предоставить свои настройки для отображения GUI по вашему усмотрению, процесс настройки GUI будет описан ниже.<br>
Основная идея отрисовки заключается в том, что БД хранит список моделей, список котрых (с дополнительной настройкой) отображается в виде карточек, то есть каждая сущность представляет из себя отдельную карточку.

### 🛠️ Инструкция по использованию
Для разработки своего приложения с использованием dooby небходимо:
1. Разарботать свою модель/модели в файле models.py, для упрощения можно исспользовать декларации из dooby.fields
   <br>Например:
```Python
class Partner(Model):
    __tablename__ = "partners"
    id = KeyField()
    name = StringField()
    type = StringField()
    director = StringField()
    phone = StringField()
    rating = IntegerField()
```

2. В app файле настройте содинение с БД с помошью
```Python
engine = init_db("some/path") из dooby.core
```
   
---
Теперь опишу процесс настройки отображения:<br><br>
3. Инициализируейте контекст настроки UI моделью, контекст представлен в dooby.gui.ui_layout_config 
   <br>Например:
```Python
ui_config = UILayoutConfig(Partner)
```
4. Вы можете указать какие поля НЕ хотите отображать
   <br>Например:
```Python
ui_config.excluded_fields.append('hideninfo')
```

5. Опишите общие настроки отображения окна и карточек
   <br>Например:
```Python
ui_config.set_background_color(Colors.smoke)       #Цвет окна
ui_config.set_card_background(Colors.lightblue)    #Цвет карточки
ui_config.set_alignment('left_custom_spacing')     #Выравние в пределах картчоки (доступны: left, center, right, left_custom_spacing)
ui_config.set_inter_element_spacing(40)            #Отступ между полями для left_custom_spacing
ui_config.set_card_spacing(10)                     #Отступ между карточками
ui_config.set_font(('Arial', 12))                  #Выбор шрифта и кегеля
```


6. Построчно настройте отображения, то есть укажите какие поля на каких строках вы хотите видеть:
  <br>Например:
```Python
ui_config.layout = defaultdict(list, {
    1: ['name', 'type', 'discount'],
    2: ['phone'],
    3: ['director'],
    4: ['rating']
})
```
7. Настройте особенности отображения подписей до и после полей
   <br>Например:
```Python
ui_config.set_field_label('name', 'Наименование :')                             #Перед полем 
ui_config.set_field_label('type', 'Тип организации :')                          
ui_config.set_field_label('discount', 'Скидка :')                               
ui_config.set_field_suffix('discount', '%')                                     #После поля
ui_config.set_field_label('phone', 'Телефон :')
ui_config.set_special_widget('type', 'combobox', ['ООО', 'ИП', 'АО'])           #Выбор для режима добавления
ui_config.set_special_widget('phone', 'phone')
ui_config.set_field_label('director', 'Директор :')
ui_config.set_field_label('rating', 'Рейтинг :')
```
8. Для запуска процесса приложения сконструируйте экзампляр класса DooByApp, представленный в dooby.gui.main_page
   <br>Например:
```Python
root = Tk()
DooByApp(root, Partner, title="Учет партнёров", logo_path="resources//logo.png", ui_config=ui_config)
```
9. Запустите процесс отрисовки tkiner:
```Python
root.mainloop()
```


### 📜 Лицензия
Проект залицензирован под MIT License. Свободно используйте, модифицируйте и распространяйте.
