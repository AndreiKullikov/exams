import sqlite3
import tkinter as tk
from tkinter import messagebox

connection = sqlite3.connect('animal.db')
cursor = connection.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS animal (
        id INTEGER PRIMARY KEY,
        name TEXT,
        birthdate DATE,
        commands TEXT,
        type TEXT
    )
''')
connection.commit()

class animal:
    def __init__(self, name, birthdate, commands):
        self.name = name
        self.birthdate = birthdate
        self.commands = commands

    def show_commands(self):
        print(f"commands for animal {self.name}: {self.commands}")
        print(f"animal {self.name} successfully trained new commands!")

class pet_animal(animal):
    def __init__(self, name, birthdate, commands, type):
        super().__init__(name, birthdate, commands)
        self.type = type

    def show_особенности(self):
        print(f"Pet Features {self.name}: type - {self.type}")

class pack_animal(animal):
    def __init__(self, name, birthdate, commands, type):
        super().__init__(name, birthdate, commands)
        self.type = type

    def show_особенности(self):
        print(f"Features of the pack animal {self.name}: type - {self.type}")


class Counter:
    def __init__(self):
        self.count = 0

    def add(self):
        self.count += 1
Counter = Counter()


def train_commands(name, new_commands):
    try:
        cursor.execute('SELECT name, commands FROM animal WHERE name=?', (name,))
        animal = cursor.fetchone()
        if not animal:
            raise ValueError(f"animal  with the name '{name}' not found")
        
        old_commands = animal[1]
        new_commands = old_commands + ', ' + new_commands  # Adding a new command to old commands
        
        cursor.execute('UPDATE animal SET commands=? WHERE name=?', (new_commands, name))
        connection.commit()
        
        messagebox.showinfo("Success", f"animal {name}  has been successfully trained with the new command!")
    except Exception as e:
        messagebox.showerror("Error", f"Error  during command training: {e}")


def create_animal(type):
    try:
        name = entry_name_pet.get() if type == 'pet' else entry_name_pack.get()
        birthdate = entry_birthdate_pet.get() if type == 'pet' else entry_birthdate_pack.get()
        commands = entry_commands_pet.get() if type == 'pet' else entry_commands_pack.get()
        
        if name and birthdate and commands:
            Counter.add()
            type_animal = entry_type_pet.get() if type == 'pet' else entry_type_pack.get()

            cursor.execute('''
                INSERT INTO animal (name, birthdate, commands, type)
                VALUES (?, ?, ?, ?)
            ''', (name, birthdate, commands, type_animal))
            connection.commit()
            messagebox.showinfo("Success", f"animal {name} has been successfully added to the database!")
            
            # Creating an animal object based on typ
            if type == 'pet':
                return pet_animal(name, birthdate, commands, type_animal)
            elif type == 'pack':
                return pack_animal(name, birthdate, commands, type_animal)
        else:
            raise ValueError("Required fields are not filled in")
    except Exception as e:
        messagebox.showerror("Error", f"Error when creating an animal: {e}")


def show_all_animal():
    cursor.execute('SELECT * FROM animal')
    animal = cursor.fetchall()
    if animal:
        text = "A list of all the animals:\n"
        for animal in animal:
            commands = animal[3].split(', ')
            text += f"name: {animal[1]}, commands: {', '.join(commands)}  birthdate:{animal[2]}, type:{animal[4]}\n"
        messagebox.showinfo("animal", text)
    else:
        messagebox.showinfo("animal", "No animals in database")


root = tk.Tk()
root.title("Pet registry")

# Pet and pack animal frames
frame_pet = tk.Frame(root)
frame_pet.grid(row=0, column=0)

frame_pack = tk.Frame(root)
frame_pack.grid(row=1, column=0)

# Labels and Input Fields for Pets
label_name_pet = tk.Label(frame_pet, text="name:")
label_name_pet.grid(row=0, column=0)
entry_name_pet = tk.Entry(frame_pet)
entry_name_pet.grid(row=0, column=1)

label_birthdate_pet = tk.Label(frame_pet, text=" birthdate:")
label_birthdate_pet.grid(row=1, column=0)
entry_birthdate_pet = tk.Entry(frame_pet)
entry_birthdate_pet.grid(row=1, column=1)

label_commands_pet = tk.Label(frame_pet, text="commands:")
label_commands_pet.grid(row=2, column=0)
entry_commands_pet = tk.Entry(frame_pet)
entry_commands_pet.grid(row=2, column=1)

label_type_pet = tk.Label(frame_pet, text="type:")
label_type_pet.grid(row=3, column=0)
entry_type_pet = tk.Entry(frame_pet)
entry_type_pet.grid(row=3, column=1)

button_pet = tk.Button(frame_pet, text="Завести pet animal", command=lambda: create_animal('pet'))
button_pet.grid(row=4, columnspan=2)

# Метки и Поля ввода для Вьючного животного
label_name_pack = tk.Label(frame_pack, text="name:")
label_name_pack.grid(row=0, column=0)
entry_name_pack = tk.Entry(frame_pack)
entry_name_pack.grid(row=0, column=1)

label_new_commands = tk.Label(frame_pack, text="New commands:")
label_new_commands.grid(row=7, column=0)
entry_new_commands = tk.Entry(frame_pack)
entry_new_commands.grid(row=7, column=1)

label_select_animal = tk.Label(frame_pack, text="Select an animal for training:")
label_select_animal.grid(row=6, column=0)
entry_select_animal = tk.Entry(frame_pack)
entry_select_animal.grid(row=6, column=1)

label_birthdate_pack = tk.Label(frame_pack, text=" birthdate:")
label_birthdate_pack.grid(row=1, column=0)
entry_birthdate_pack = tk.Entry(frame_pack)
entry_birthdate_pack.grid(row=1, column=1)

label_commands_pack = tk.Label(frame_pack, text="commands:")
label_commands_pack.grid(row=2, column=0)
entry_commands_pack = tk.Entry(frame_pack)
entry_commands_pack.grid(row=2, column=1)

label_type_pack = tk.Label(frame_pack, text="type:")
label_type_pack.grid(row=3, column=0)
entry_type_pack = tk.Entry(frame_pack)
entry_type_pack.grid(row=3, column=1)

button_pack = tk.Button(frame_pack, text="Get a pack animal", command=lambda: create_animal('pack'))
button_pack.grid(row=4, columnspan=2)

button_pack = tk.Button(frame_pack, text="show all animals ", command=lambda: show_all_animal())
button_pack.grid(row=16, columnspan=4)
button_pack_обучение = tk.Button(frame_pack, text="Teach new commands ", command=lambda:train_commands(entry_select_animal.get(), entry_new_commands.get()))
button_pack_обучение.grid(row=8, columnspan=6)



root.mainloop()
