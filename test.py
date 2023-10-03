# import tkinter as tk
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
