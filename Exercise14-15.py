import sqlite3
import tkinter as tk
from tkinter import messagebox

connection = sqlite3.connect('реестр_животных.db')
cursor = connection.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Животные (
        id INTEGER PRIMARY KEY,
        название TEXT,
        дата_рождения DATE,
        команды TEXT,
        тип TEXT
    )
''')
connection.commit()

class Животное:
    def __init__(self, название, дата_рождения, команды):
        self.название = название
        self.дата_рождения = дата_рождения
        self.команды = команды

    def показать_команды(self):
        print(f"Команды для животного {self.название}: {self.команды}")
        print(f"Животное {self.название} успешно обучено новым командам!")

class Домашнее_животное(Животное):
    def __init__(self, название, дата_рождения, команды, тип):
        super().__init__(название, дата_рождения, команды)
        self.тип = тип

    def показать_особенности(self):
        print(f"Особенности домашнего животного {self.название}: Тип - {self.тип}")

class Вьючное_животное(Животное):
    def __init__(self, название, дата_рождения, команды, тип):
        super().__init__(название, дата_рождения, команды)
        self.тип = тип

    def показать_особенности(self):
        print(f"Особенности вьючного животного {self.название}: Тип - {self.тип}")


class Счетчик:
    def __init__(self):
        self.count = 0

    def add(self):
        self.count += 1
счетчик = Счетчик()


def обучить_командам(название, новые_команды):
    try:
        cursor.execute('SELECT название, команды FROM Животные WHERE название=?', (название,))
        животное = cursor.fetchone()
        if not животное:
            raise ValueError(f"Животное с именем '{название}' не найдено")
        
        старые_команды = животное[1]
        новые_команды = старые_команды + ', ' + новые_команды  # Добавляем новую команду к старым командам
        
        cursor.execute('UPDATE Животные SET команды=? WHERE название=?', (новые_команды, название))
        connection.commit()
        
        messagebox.showinfo("Успех", f"Животное {название} успешно обучено новой команде!")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при обучении команде: {e}")


def создать_животное(тип):
    try:
        название = entry_название_домашнее.get() if тип == 'домашнее' else entry_название_вьючное.get()
        дата_рождения = entry_дата_рождения_домашнее.get() if тип == 'домашнее' else entry_дата_рождения_вьючное.get()
        команды = entry_команды_домашнее.get() if тип == 'домашнее' else entry_команды_вьючное.get()
        
        if название and дата_рождения and команды:
            счетчик.add()
            тип_животного = entry_тип_домашнее.get() if тип == 'домашнее' else entry_тип_вьючное.get()

            cursor.execute('''
                INSERT INTO Животные (название, дата_рождения, команды, тип)
                VALUES (?, ?, ?, ?)
            ''', (название, дата_рождения, команды, тип_животного))
            connection.commit()
            messagebox.showinfo("Успех", f"Животное {название} успешно добавлено в базу данных!")
            
            # Создание объекта животного на основе типа
            if тип == 'домашнее':
                return Домашнее_животное(название, дата_рождения, команды, тип_животного)
            elif тип == 'вьючное':
                return Вьючное_животное(название, дата_рождения, команды, тип_животного)
        else:
            raise ValueError("Не заполнены обязательные поля")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при создании животного: {e}")


def показать_всех_животных():
    cursor.execute('SELECT * FROM Животные')
    животные = cursor.fetchall()
    if животные:
        текст = "Список всех заведенных животных:\n"
        for животное in животные:
            команды = животное[3].split(', ')
            текст += f"Название: {животное[1]}, Команды: {', '.join(команды)}  Дата рождения:{животное[2]}, Тип:{животное[4]}\n"
        messagebox.showinfo("Животные", текст)
    else:
        messagebox.showinfo("Животные", "Нет заведенных животных")


root = tk.Tk()
root.title("Реестр домашних животных")

# Фреймы для домашнего и вьючного животного
frame_домашнее = tk.Frame(root)
frame_домашнее.grid(row=0, column=0)

frame_вьючное = tk.Frame(root)
frame_вьючное.grid(row=1, column=0)

# Метки и Поля ввода для Домашнего животного
label_название_домашнее = tk.Label(frame_домашнее, text="Название:")
label_название_домашнее.grid(row=0, column=0)
entry_название_домашнее = tk.Entry(frame_домашнее)
entry_название_домашнее.grid(row=0, column=1)

label_дата_рождения_домашнее = tk.Label(frame_домашнее, text="Дата рождения:")
label_дата_рождения_домашнее.grid(row=1, column=0)
entry_дата_рождения_домашнее = tk.Entry(frame_домашнее)
entry_дата_рождения_домашнее.grid(row=1, column=1)

label_команды_домашнее = tk.Label(frame_домашнее, text="Команды:")
label_команды_домашнее.grid(row=2, column=0)
entry_команды_домашнее = tk.Entry(frame_домашнее)
entry_команды_домашнее.grid(row=2, column=1)

label_тип_домашнее = tk.Label(frame_домашнее, text="Тип:")
label_тип_домашнее.grid(row=3, column=0)
entry_тип_домашнее = tk.Entry(frame_домашнее)
entry_тип_домашнее.grid(row=3, column=1)

button_домашнее = tk.Button(frame_домашнее, text="Завести домашнее животное", command=lambda: создать_животное('домашнее'))
button_домашнее.grid(row=4, columnspan=2)

# Метки и Поля ввода для Вьючного животного
label_название_вьючное = tk.Label(frame_вьючное, text="Название:")
label_название_вьючное.grid(row=0, column=0)
entry_название_вьючное = tk.Entry(frame_вьючное)
entry_название_вьючное.grid(row=0, column=1)

label_новые_команды = tk.Label(frame_вьючное, text="Новые команды:")
label_новые_команды.grid(row=7, column=0)
entry_новые_команды = tk.Entry(frame_вьючное)
entry_новые_команды.grid(row=7, column=1)

label_выбор_животного = tk.Label(frame_вьючное, text="Выберите животное для обучения:")
label_выбор_животного.grid(row=6, column=0)
entry_выбор_животного = tk.Entry(frame_вьючное)
entry_выбор_животного.grid(row=6, column=1)

label_дата_рождения_вьючное = tk.Label(frame_вьючное, text="Дата рождения:")
label_дата_рождения_вьючное.grid(row=1, column=0)
entry_дата_рождения_вьючное = tk.Entry(frame_вьючное)
entry_дата_рождения_вьючное.grid(row=1, column=1)

label_команды_вьючное = tk.Label(frame_вьючное, text="Команды:")
label_команды_вьючное.grid(row=2, column=0)
entry_команды_вьючное = tk.Entry(frame_вьючное)
entry_команды_вьючное.grid(row=2, column=1)

label_тип_вьючное = tk.Label(frame_вьючное, text="Тип:")
label_тип_вьючное.grid(row=3, column=0)
entry_тип_вьючное = tk.Entry(frame_вьючное)
entry_тип_вьючное.grid(row=3, column=1)

button_вьючное = tk.Button(frame_вьючное, text="Завести вьючное животное", command=lambda: создать_животное('вьючное'))
button_вьючное.grid(row=4, columnspan=2)

button_вьючное = tk.Button(frame_вьючное, text="Показать всех животных ", command=lambda: показать_всех_животных())
button_вьючное.grid(row=16, columnspan=4)
button_вьючное_обучение = tk.Button(frame_вьючное, text="Обучить новым командам ", command=lambda: обучить_командам(entry_выбор_животного.get(), entry_новые_команды.get()))
button_вьючное_обучение.grid(row=8, columnspan=6)



root.mainloop()
