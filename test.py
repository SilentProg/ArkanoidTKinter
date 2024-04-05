import tkinter as tk

import customtkinter as ctk

# from math import sqrt
#
# radius = 20
# diameter = 2 * radius
# a = int(2 * (sqrt(2) / 2 * radius))
#
#
# def check_collision():
#     ball_x1, ball_y1, ball_x2, ball_y2 = canvas.coords(ball)
#     rect_x1, rect_y1, rect_x2, rect_y2 = canvas.coords(rectangle)
#
#     if (ball_x2 >= rect_x1 and ball_x1 <= rect_x2 and
#             ball_y2 >= rect_y1 and ball_y1 <= rect_y2):
#         # Визначення сторони удару
#         if ball_x2 >= rect_x1 and ball_x1 <= rect_x1 - diameter and ball_y2 - radius <= rect_y2 and ball_y1 + radius >= rect_y1:
#             result.set("Зліва")
#         elif ball_x1 <= rect_x2 and ball_x2 >= rect_x2 + diameter and ball_y2 - radius <= rect_y2 and ball_y1 + radius >= rect_y1:
#             result.set("Справа")
#         elif ball_y2 >= rect_y1 and ball_y1 <= rect_y1 and ball_x1 + radius >= rect_x1 and ball_x2 - radius <= rect_x2:
#             result.set("Зверху")
#         elif ball_y1 >= rect_y2 and ball_y2 >= rect_y2 and ball_x1 + radius >= rect_x1 and ball_x2 - radius <= rect_x2:
#             result.set("Знизу")
#         else:
#             result.set("Зсередини")
#     else:
#         result.set("Немає зіткнення")
#
#
# def move_ball(event):
#     if event.keysym == "Left":
#         canvas.move(ball, -5, 0)
#     elif event.keysym == "Right":
#         canvas.move(ball, 5, 0)
#     elif event.keysym == "Up":
#         canvas.move(ball, 0, -5)
#     elif event.keysym == "Down":
#         canvas.move(ball, 0, 5)
#     check_collision()
#
#
# # Створення вікна
# window = tk.Tk()
# window.title("Перевірка сторони удару і керування м'ячем")
#
# canvas = tk.Canvas(window, width=400, height=300)
# canvas.pack()
#
# # Створення прямокутника
# rectangle = canvas.create_rectangle(150, 150, 250, 250, fill="blue")
#
# # Створення м'яча
# # ball = canvas.create_oval(190, 100, 210, 120, fill="red")
# ball = canvas.create_oval(15 - radius, 10 - radius, 15 + radius, 10 + radius, fill='red')
# canvas.move(ball, 100, 100)
# result = tk.StringVar()
# result_label = tk.Label(window, textvariable=result)
# result_label.pack()
#
# check_button = tk.Button(window, text="Перевірити колізію", command=check_collision)
# check_button.pack()
#
# # Додавання обробки клавіш
# window.bind("<Left>", move_ball)
# window.bind("<Right>", move_ball)
# window.bind("<Up>", move_ball)
# window.bind("<Down>", move_ball)
#
# window.mainloop()

# import tkinter as tk
#
#
# def create_list(root, items):
#     row = 0
#     col = 0
#
#     for item in items:
#         frame = tk.Frame(root, width=100, height=100, borderwidth=1, relief="solid")
#         frame.grid(row=row, column=col, padx=5, pady=5)
#         button = tk.Button(frame, text=item)
#         button.pack(fill="both", expand=True)
#
#         col += 1
#         if col > 3:
#             col = 0
#             row += 1
#
#
# if __name__ == "__main__":
#     root = tk.Tk()
#     root.title("Список с кнопками")
#
#     items = ["Элемент 1", "Элемент 2", "Элемент 3", "Элемент 4",
#              "Элемент 5", "Элемент 6", "Элемент 7", "Элемент 8",
#              "Элемент 9", "Элемент 10", "Элемент 11", "Элемент 12"]
#
#     create_list(root, items)
#
#     root.mainloop()

# import tkinter as tk
# from tkinter import messagebox


# def open_modal_window():
#     modal_window = tk.Toplevel(root)
#     modal_window.title("Модальное окно")
#
#     # Установить модальный режим для модального окна
#     modal_window.grab_set()
#
#     # Создать некоторый контент для модального окна
#     label = tk.Label(modal_window, text="Это модальное окно")
#     label.pack(padx=20, pady=20)
#
#     # Функция, которая будет вызываться при закрытии модального окна
#     def on_close():
#         modal_window.grab_release()
#         modal_window.destroy()
#
#     # Создать кнопку для закрытия модального окна
#     close_button = tk.Button(modal_window, text="Закрыть", command=on_close)
#     close_button.pack(pady=10)
#
#
# if __name__ == "__main__":
#     root = tk.Tk()
#     root.title("Главное окно")
#
#     # Создать кнопку для открытия модального окна
#     open_button = tk.Button(root, text="Открыть модальное окно", command=open_modal_window)
#     open_button.pack(padx=20, pady=20)
#
#     root.mainloop()

# import tkinter as tk
#
# def on_button_click():
#     button.config(text="Натисніть клавішу...")
#     root.bind("<Key>", update_button_text)
#
# def update_button_text(event):
#     button.config(text=event.keysym)
#     root.unbind("<Key>")
#
# root = tk.Tk()
# root.title("Tkinter Клавіші")
#
# button = tk.Button(root, text="Right", command=on_button_click)
# button.pack(padx=20, pady=20)
#
# root.mainloop()
# import i18n_config
# i18n.set('locale', 'ua')
# i18n.set('filename_format', '{locale}.{format}')
# i18n.set('file_format', 'json')
# i18n.load_path.append('locales')
# print(i18n.t('test'))

# from cryptography.fernet import Fernet
#
# # Generate a key
# key = Fernet.generate_key()
# cipher_suite = Fernet(key)
#
# # Encrypt the original string
# original_string = b"Secret message"
# cipher_text = cipher_suite.encrypt(original_string)
#
# # Decrypt back to the original string
# decrypted_string = cipher_suite.decrypt(cipher_text)
#
# print("Original String:", original_string.decode())
# print("Decrypted String:", decrypted_string.decode())
#

import i18n
from customtkinter import CTkFrame

import firebase
import i18n_config
from custom_dialogs import InfoDialog


# app = customtkinter.CTk()
# app.geometry("400x300")
#
#
# def button_click_event():
#     # dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="Test")
#     # print("Number:", dialog.get_input())
#     file_name = customtkinter.CTkInputDialog(title=i18n.t('level-save'), text=i18n.t('ask-level-title'))
#     print("Name:", file_name.get_input())
#
#
# button = customtkinter.CTkButton(app, text="Open Dialog", command=button_click_event)
# button.pack(padx=20, pady=20)
#
# app.mainloop()

class ListView(ctk.CTkScrollableFrame):
    def __init__(self, master: any, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(width=300, height=600)
        self.items = []

    def add_item(self, item: CTkFrame):
        self.items.append(item)
        item.pack(side=ctk.TOP, fill=ctk.BOTH, expand=True,  padx=5, pady=5)


class LevelItem(CTkFrame):
    def __init__(self, master: any, level: {}, **kwargs):
        super().__init__(master, **kwargs)
        self.frame = CTkFrame(self)

        self.level = level

        self.title_label = ctk.CTkLabel(self.frame, text=level['title'], width=200, justify='left')
        self.title_label.pack(side=ctk.LEFT, padx=10, pady=10)

        self.creator = ctk.CTkLabel(self.frame, text=i18n.t('creator-name', creator=level['creatorName']))
        self.creator.pack(side=ctk.LEFT, padx=10, pady=10)

        self.hp_counter = ctk.CTkLabel(self.frame, text=i18n.t('hp-double-dot-number', hp=level['level']['hp']))
        self.hp_counter.pack(side=ctk.LEFT, padx=10, pady=10)

        self.button = ctk.CTkButton(self.frame, text="test", command=lambda: print(level['key']))
        self.button.pack(side=ctk.LEFT)

        self.frame.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)



def main():
    root = ctk.CTk()
    root.title("Custom List View")
    root.geometry("600x400")

    custom_list_view = ListView(root)
    custom_list_view.pack(expand=True, fill="both")

    for level in firebase.db.child('community-levels').get().each():
        val = level.val()
        val['key'] = level.key()
        custom_list_view.add_item(LevelItem(custom_list_view, val))

    root.mainloop()


if __name__ == "__main__":
    main()
