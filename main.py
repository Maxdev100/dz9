import tkinter as tk
from tkinter import ttk
import sqlite3

# Класс базы данных
class DB:
    # Инициализация (подключение к БД и создание таблицы, если она отсутствует)
    def __init__(self):
        self.conn = sqlite3.connect("db.db")
        self.c = self.conn.cursor()

        self.c.execute('''
        CREATE TABLE IF NOT EXISTS db(id integer primary key, name text, tel text, email text)
        ''')
        self.conn.commit()

    # Функция добавления данных в БД
    def insert_data(self, name, tel, email):
        self.c.execute('''
        INSERT INTO db (name, tel, email) VALUES (?, ?, ?)
        ''', (name, tel, email))

        self.conn.commit()

# Класс главного окна
class Main(tk.Frame):
    # Конструктор класса (инициализация главного окна, 
    # подключение к БД и вывод записей)
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = DB()
        self.view_records()

    # Инициализация главного окна
    def init_main(self):
        # Добавление тулбара с кнопками
        toolbar = tk.Frame(bg="#d7d8e0", bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Добавление таблицы с записями
        self.tree = ttk.Treeview(self, columns=['ID', 'name', 'tel', 'email'],
                                 height=45, show='headings')
       
        # Настройка таблицы с записями
        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('name', width=300, anchor=tk.CENTER)
        self.tree.column('tel', width=150, anchor=tk.CENTER)
        self.tree.column('email', width=150, anchor=tk.CENTER)

        self.tree.heading('ID', text='ID')
        self.tree.heading('name', text='ФИО')
        self.tree.heading('tel', text='Телефон')
        self.tree.heading('email', text='E-mail')
        self.tree.pack(side=tk.LEFT)

        # Кнопка добавления записи
        self.add_img = tk.PhotoImage(file='./img/add.png')        
        btn_open_dialog = tk.Button(toolbar, bg='#d7d8e0', bd=0,
                                    image=self.add_img, command=self.open_dialog)
        btn_open_dialog.pack(side=tk.LEFT)
        
        # Кнопка редактирования
        self.update_img = tk.PhotoImage(file="./img/update.png")
        btn_edit_dialog = tk.Button(toolbar, bg="#d7d8e0",
                                    bd=0, image=self.update_img,
                                    command=self.open_update_dialog)
        btn_edit_dialog.pack(side=tk.LEFT)

        # Кнопка удаления
        self.delete_image = tk.PhotoImage(file='./img/delete.png')
        btn_delete = tk.Button(toolbar, bg="#d7d8e0",
                               bd = 0, image=self.delete_image,
                               command=self.delete_records)
        btn_delete.pack(side=tk.LEFT)

        # Кнопка поиска
        self.search_image = tk.PhotoImage(file='./img/search.png')
        btn_search = tk.Button(toolbar, bg="#d7d8e0",
                               bd = 0, image=self.search_image,
                               command=self.open_search_dialog)
        btn_search.pack(side=tk.LEFT)

        # Кнопка обновления списка
        self.refresh_image = tk.PhotoImage(file='./img/refresh.png')
        btn_refresh = tk.Button(toolbar, bg="#d7d8e0",
                               bd = 0, image=self.refresh_image,
                               command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)

        # Добавление скроллбара
        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)


    # При нажатии кнопки поиска - открытие окна поиска, используя класс Search
    def open_search_dialog(self):
        Search()

    # Поиск по имени пользователя в БД и запись результатов в таблицу
    # с последующем обновлением ее содержимого
    def search_records(self, name):
        name = ('%' + name + '%')
        self.db.c.execute('''
            SELECT * FROM db WHERE name LIKE ?''', (name,))
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    
    # Удаление выбранный записей в таблице из БД при нажатии кнопки
    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.c.execute('''
                DELETE FROM db WHERE id = ?
            ''', (self.tree.set(selection_item, "#1"),))
        self.db.conn.commit()
        self.view_records()

    # Обновление записей в БД в окне редактирования по нажатию кнопки
    # и вывод обновленной таблицы
    def update_record(self, name, tel, email):
        self.db.conn.execute('''
            UPDATE db SET name=?, tel=?, email=? WHERE id = ?
        ''', (name, tel, email, self.tree.set(self.tree.selection()[0], "#1")))
        self.db.conn.commit()
        self.view_records()
    
    # Открытие окна редакторования при нажатии кнопки через класс Update
    def open_update_dialog(self):
        Update()
    
    # Открытие окна добавления пользователя по нажатию кнопки
    def open_dialog(self):
        Child()

    # Функия получения данных из БД с последующем обновлением таблицы с записями
    # в главном окне
    def view_records(self):
        self.db.c.execute('''
        SELECT * FROM db
        ''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    # Добавление записи в БД и обновление таблицы на главном окне
    def records(self, name, tel, email):
        self.db.insert_data(name, tel, email)
        self.view_records()

# Класс окна добавления пользователя
class Child(tk.Toplevel):
    # Инициализация и вызов функции создания окна
    def __init__(self):
        super().__init__()
        self.init_child()
        self.view = app

    # Создание окна и настройка виджетов
    def init_child(self):
        self.title("Добавить")
        self.geometry("400x220")
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()

        # Текст "ФИО"
        label_name = tk.Label(self, text="ФИО")
        label_name.place(x=50, y=50)

        # Текст "Телефон"
        label_select = tk.Label(self, text="Телефон")
        label_select.place(x=50, y=80)

        # Текст "E-mail"
        label_email = tk.Label(self, text="E-mail")
        label_email.place(x=50, y=110)

        # Ввод имени
        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=50)

        # Ввод телефона
        self.entry_tel = ttk.Entry(self)
        self.entry_tel.place(x=200, y=80)

        # Ввод почты
        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200, y=110)

        # Кнопка отмены. При нажатии - закрытие окна
        self.button_cancel = tk.Button(self, text="Отмена", command=self.destroy)
        self.button_cancel.place(x=275, y=170)

        # Кнопка добавления записи. При нажатии - получение данных полей ввода
        # и добавление этих данных в БД
        self.button_add = tk.Button(self, text="Добавить")
        self.button_add.place(x=195, y=170)
        self.button_add.bind("<Button-1>",
                             lambda event: self.view.records(self.entry_name.get(),
                                                             self.entry_tel.get(),
                                                             self.entry_email.get()))
                                                             
# Окно редактирования данных
class Update(Child):
    # Инициализация необходимых переменных и вызов функций
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.default_data()

    # Создание окна редактирования и добавление виджетов
    def init_edit(self):
        self.title("Редактировать позицию")
        
        # Кнопка применения изменений. При нажатии - обновление данных в БД на новые
        btn_edit = ttk.Button(self, text="Применить")
        btn_edit.bind("<Button-1>", lambda event:
                      self.view.update_record(self.entry_name.get(),
                                              self.entry_tel.get(),
                                              self.entry_email.get()))
        
        # Кнопка отмены. При нажатии - закрытие окна
        btn_edit.bind("<Button-1>", lambda event:
                      self.destroy(), add="+")
        
        btn_edit.place(x=180, y=170)
        self.button_add.destroy()

    
    # Получение данных выбраного человека и заполнение полей ввода для удобства
    def default_data(self):
        self.db.c.execute('''
            SELECT * FROM db WHERE id=?
        ''', (self.view.tree.set(self.view.tree.selection()[0], "#1"),))
        row = self.db.c.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_tel.insert(0, row[2])
        self.entry_email.insert(0, row[3])
    
# Класс окна поиска по имени
class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    # Создание окна и заполнение виджетами
    def init_search(self):
        self.title("Поиск")
        self.geometry("300x100")
        self.resizable(False, False)

        # Создание надписи "Поиск"
        label_search = tk.Label(self, text="Поиск")
        label_search.place(x=50, y=20) 

        # Поле ввода
        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=105, y=20, width=150)

        # Кнопка отмены. При нажатии - закрытие окна
        btn_cancel = ttk.Button(self, text="Закрыть", command=self.destroy)
        btn_cancel.place(x=185, y=50)

        # Кнопка поиска
        btn_search = ttk.Button(self, text="Поиск") 
        btn_search.bind("<Button-1>", lambda event: 
                        self.view.search_records(self.entry_search.get()))
        btn_search.bind("<Button-1>", lambda event:
                        self.destroy(), add="+")
        btn_search.place(x=105, y=50)


# Создание главного окна и первичная настройка
if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)
    db = DB()
    app.pack()
    root.title("Телефонная книга")
    root.geometry("665x450")
    root.resizable(False, False)
    root.mainloop()