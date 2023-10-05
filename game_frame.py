import json
import os
from customtkinter import CTkFrame, CTkLabel, CTkFont, CTkButton, CTkImage
from tkinter import Canvas
from PIL import Image
import pygame
import configparser
import re

class LevelInfoFrame(CTkFrame):

    def __init__(self, master, level, hp, toggle_pause, restart, **kwargs):
        super().__init__(master, **kwargs)
        self.level = level
        self.level_label = None
        self.level_score = None
        self.hp = hp
        self.restart = restart
        self.togglePause = toggle_pause
        self.max_hp = hp
        self.hp_bar = []
        self.hp_icon = Image.open('assets\\icons\\hp.png')
        self.hp_broken_icon = Image.open('assets\\icons\\hp_broken.png')
        self.button_font = CTkFont(family="Helvetica", size=14, weight="bold")
        self.level_font = CTkFont(family="Helvetica", size=36, weight="bold")
        self.menu_click_sound = pygame.mixer.Sound("assets/sounds/menu_click.wav")
        self.initUI()

    def setHp(self, hp):
        self.hp = hp
        self.max_hp = hp
        self.initHp()

    def setMaxHp(self, max_hp):
        self.max_hp = max_hp
        self.initHp()

    def initUI(self):
        button_menu = CTkButton(self, text="Menu", font=self.button_font, height=40, command=self.returnToMenu)
        button_menu.grid(row=0, column=0, padx=10, pady=10)

        self.level_label = CTkLabel(self, text="Level: {} |".format(1), font=self.level_font)
        self.level_label.grid(row=0, column=1, padx=10, pady=10)

        self.level_score = CTkLabel(self, text="Score: {} |".format(0), font=self.level_font)
        self.level_score.grid(row=0, column=2, padx=10, pady=10)

        hp_label = CTkLabel(self, text="HP:", font=self.level_font)
        hp_label.grid(row=0, column=3, padx=10, pady=10)
        self.initHp()

    def reInit(self):
        self.setHp(self.max_hp)
        self.setScore(0)
        self.setLevel(self.level)

    def initHp(self):
        print(self.hp)
        for image in self.hp_bar:
            image.destroy()
        self.hp_bar.clear()
        print(os.getcwd())
        column = 4
        for i in range(self.hp):
            hp_image = CTkImage(dark_image=self.hp_icon, light_image=self.hp_icon, size=(50, 50))
            image = CTkLabel(self, image=hp_image, text="")
            image.grid(row=0, column=column, padx=5, pady=5)
            self.hp_bar.append(image)
            column += 1

    def hpHit(self):
        if self.hp == 0:
            return
        hp_broken_image = CTkImage(dark_image=self.hp_broken_icon, light_image=self.hp_broken_icon, size=(50, 50))
        self.hp_bar[self.max_hp - self.hp].configure(require_redraw=True, image=hp_broken_image)
        self.hp -= 1

    def returnToMenu(self):
        self.restart()
        # self.togglePause()
        self.menu_click_sound.play()
        # self.hpHit()

    def setLevel(self, level):
        self.level_label.configure(text="Level: {} |".format(str(level)))

    def setScore(self, score):
        self.level_score.configure(text="Score: {} |".format(str(score)))


class GameBoard(CTkFrame):
    def __init__(self, master, show_ui, level_name, pause: bool = False, **kwargs):
        super().__init__(master, **kwargs)
        self.level: {} = None
        self.level_path = level_name
        self.brick_h = None
        self.brick_w = None
        self.carriage = None
        self.ball = None
        self.canvas = None
        self.level_info_frame: LevelInfoFrame = None
        self.info_frame_size_h = 100
        self.size_w = int(kwargs.get("width")) - 20
        self.size_h = int(kwargs.get("height")) - self.info_frame_size_h + 10
        self.radius = 15
        self.diameter = 2 * self.radius
        self.carriage_w = 200
        self.carriage_h = 10
        self.carriage_x = self.size_w // 2
        self.carriage_stop = True
        # self.interval = 30
        self.interval = 15
        self.points = 0
        self.hp = 3
        self.root = self.master
        self.string, self.column = 2, 3
        self.bricks_zone = 0.2
        self.bricks = []
        self.walls = []
        pygame.mixer.init()
        self.hit_sound = pygame.mixer.Sound("assets/sounds/hit_received.wav")
        self.level_failed_sound = pygame.mixer.Sound("assets/sounds/level_failed.wav")
        self.level_confirm_sound = pygame.mixer.Sound("assets/sounds/level_confirm.wav")
        self.pause = pause
        self.ball_x, self.ball_y = self.size_w // 2, self.size_h // 2
        self.ball_vx, self.ball_vy = -5, -5
        self.showUi = show_ui
        self.initUI()
        self.initGame()

    def togglePause(self):
        self.pause = not self.pause
        if self.pause:
            self.canvas.unbind('<Key>')
            self.canvas.unbind('<KeyPress>')
            self.canvas.unbind('<KeyRelease>')
            self.canvas.unbind('<Motion>')
        else:
            self.canvas.bind('<Key>', self.control)
            self.canvas.bind('<KeyPress>', self.control)
            self.canvas.bind('<KeyRelease>', self.control)
            self.canvas.bind('<Motion>', self.motion)
            self.ball_movement()

    def restart(self):

        self.canvas.delete("all")
        self.walls = []
        self.bricks = []
        self.hp = 3
        self.points = 0
        self.level_info_frame.reInit()
        self.ball_vx, self.ball_vy = -5, -5
        self.ball_x, self.ball_y = self.size_w // 2, self.size_h // 2
        self.carriage_x = self.size_w // 2
        self.loadLevel()
        if not self.carriage_stop:
            self.carriage_stop = True
            self.ball_movement()

    def loadLevel(self):
        self.ball = self.canvas.create_oval(self.ball_x - self.radius, self.ball_y - self.radius,
                                            self.ball_x + self.radius, self.ball_y + self.radius,
                                            fill='white',
                                            tags='ball')

        self.carriage = self.canvas.create_rectangle(self.carriage_x - self.carriage_w // 2, self.size_h,
                                                     self.carriage_x + self.carriage_w // 2,
                                                     self.size_h - self.carriage_h,
                                                     fill='white',
                                                     tags='carriage')

        def load():
            self.hp = int(self.level['hp'])
            self.level_info_frame.setHp(self.hp)
            self.canvas.itemconfigure(self.canvas.find_withtag('carriage')[0], fill=self.level['carriage']['color'])
            self.canvas.itemconfigure(self.canvas.find_withtag('ball')[0], fill=self.level['ball']['color'])

            self.loadItems(self.level['bricks'], self.bricks)
            self.loadItems(self.level['walls'], self.walls)

        if self.level:
            load()
        elif self.level_path:
            try:
                with open(self.level_path, "r") as json_file:
                    self.level = json.load(json_file)
                    load()
            except FileNotFoundError:
                print('File not found')
        else:
            if self.level:
                return
            self.level = {
                "hp": 1,
                "ball": {
                    "color": "white"
                },
                "carriage": {
                    "color": "white"
                },
                "bricks": {},
                "walls": {}
            }

    def loadItems(self, items: {}, array):
        items_keys = list(items.keys())
        print(type(items_keys))
        for i in range(0, len(items_keys)):
            key = items_keys[i]
            print(items[key])
            if items[key] == {}:
                continue
            x1 = int(items[key]['x1'])
            y1 = int(items[key]['y1'])
            x2 = int(items[key]['x2'])
            y2 = int(items[key]['y2'])
            fill_color = items[key]['fill']
            outline_color = 'white'
            if 'outline' in items[key]:
                outline_color = items[key]['outline']
            id_item = self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color, outline=outline_color)
            items.pop(key)
            items[str(id_item)] = {
                'x1': x1,
                'y1': y1,
                'x2': x2,
                'y2': y2,
                'fill': fill_color,
                'outline': outline_color
            }
            array.append(id_item)

    def getCanvas(self) -> Canvas:
        return self.canvas

    def initUI(self):
        self.level_info_frame = LevelInfoFrame(self, "1", self.hp, self.togglePause, self.restart,
                                               width=self.size_w - 15,
                                               height=self.info_frame_size_h - 10)
        if self.showUi:
            self.level_info_frame.pack(padx=5, pady=5)

    def initGame(self):
        self.canvas = Canvas(self, width=self.size_w, height=self.size_h, bg='black')
        self.canvas.focus_set()
        self.canvas.pack(padx=5, pady=5)

        self.loadLevel()

        if not self.pause:
            self.ball_movement()
        self.canvas.bind('<Key>', self.control)
        self.canvas.bind('<KeyPress>', self.control)
        self.canvas.bind('<KeyRelease>', self.control)
        self.canvas.bind('<Motion>', self.motion)

    def ball_movement(self):
        print("move")
        print(self.level['bricks'])
        self.ball_x, self.ball_y = self.ball_x + self.ball_vx, self.ball_y + self.ball_vy
        self.canvas.coords(self.ball, self.ball_x - self.radius, self.ball_y - self.radius, self.ball_x + self.radius,
                           self.ball_y + self.radius)

        if self.ball_y <= self.radius:
            self.ball_vy = abs(self.ball_vy)
        if self.ball_x <= self.radius or self.ball_x >= self.size_w - self.radius:
            self.ball_vx = -self.ball_vx

        carriage_x1, carriage_y1, carriage_x2, carriage_y2 = self.canvas.coords(self.carriage)

        if carriage_x1 <= self.ball_x <= carriage_x2 and self.ball_y == self.size_h - (self.radius + self.carriage_h):
            self.ball_vy = -self.ball_vy
            self.update_point()

        ball_x1, ball_y1, ball_x2, ball_y2 = self.canvas.coords(self.ball)
        overlap = self.canvas.find_overlapping(ball_x1, ball_y1, ball_x2, ball_y2)

        ball_x1, ball_y1, ball_x2, ball_y2 = self.canvas.coords(self.ball)
        for ovr in overlap:
            if ovr in self.walls:  # or ovr in self.bricks:
                rect_x1, rect_y1, rect_x2, rect_y2 = self.canvas.coords(ovr)
                if (ball_x2 >= rect_x1 and ball_x1 <= rect_x2 and
                        ball_y2 >= rect_y1 and ball_y1 <= rect_y2):
                    # Визначення сторони удару
                    if ball_x2 >= rect_x1 and ball_x1 <= rect_x1 - self.diameter and ball_y2 - self.radius <= rect_y2 and ball_y1 + self.radius >= rect_y1:
                        print("Зліва")
                        self.ball_vx = -self.ball_vx
                    elif ball_x1 <= rect_x2 and ball_x2 >= rect_x2 + self.diameter and ball_y2 - self.radius <= rect_y2 and ball_y1 + self.radius >= rect_y1:
                        print("Справа")
                        self.ball_vx = -self.ball_vx
                    elif ball_y2 >= rect_y1 and ball_y1 <= rect_y1 and ball_x1 + self.radius >= rect_x1 and ball_x2 - self.radius <= rect_x2:
                        print("Зверху")
                        self.ball_vy = -self.ball_vy
                    elif ball_y1 >= rect_y2 and ball_y2 >= rect_y2 and ball_x1 + self.radius >= rect_x1 and ball_x2 - self.radius <= rect_x2:
                        print("Знизу")
                        self.ball_vy = -self.ball_vy
                    else:
                        print("Всередені")
                        self.ball_vx = -self.ball_vx
                else:
                    print("Немає зіткнення")
            # if ovr in self.bricks:
            #     self.canvas.delete(ovr)
            #     self.bricks.pop(self.bricks.index(ovr))
            #     self.update_point()

        brick = self.crash_a_brick()
        if brick in self.bricks:
            self.ball_vy = -self.ball_vy
            self.canvas.delete(brick)
            self.bricks.pop(self.bricks.index(brick))
            self.update_point()

        if len(self.bricks) == 0:
            self.level_confirm_sound.play()
            self.canvas.create_text(self.size_w // 2, self.size_h // 2, text='You WIN!', fill='green', font=(None, 50))
            self.carriage_stop = False
            return

        if self.ball_y < (self.size_h - self.radius):
            if not self.pause:
                self.root.after(self.interval, self.ball_movement)
        else:
            if self.hp > 1:
                self.hit_sound.play()
                self.hp -= 1
                self.level_info_frame.hpHit()
                self.ball_vy = -self.ball_vy
                self.root.after(self.interval, self.ball_movement)
            else:
                self.level_failed_sound.play()
                self.hp -= 1
                self.level_info_frame.hpHit()
                self.canvas.create_text(self.size_w // 2, self.size_h // 2, text='GAME OVER', fill='red',
                                        font=(None, 50))
                self.carriage_stop = False

    def crash_a_brick(self):
        for brick in self.bricks:
            brick_x1, brick_y1, brick_x2, brick_y2 = self.canvas.coords(brick)
            if brick_x1 < self.ball_x < brick_x2 and (
                    brick_y1 < self.ball_y + self.radius < brick_y2 or brick_y1 < self.ball_y - self.radius < brick_y2):
                return brick

    def update_point(self):
        self.points += 1
        self.level_info_frame.setScore(self.points)

    def control(self, event):
        if self.pause:
            return
        x1, y1, x2, y2 = self.canvas.coords(self.carriage)
        if event.keysym == 'Left' and x1 + 20 >= 0:
            self.carriage_x -= 10
        if event.keysym == 'Right' and x2 - 20 <= self.size_w:
            self.carriage_x += 10

        if self.carriage_stop:
            self.canvas.coords(self.carriage, self.carriage_x - self.carriage_w // 2, self.size_h,
                               self.carriage_x + self.carriage_w // 2, self.size_h - self.carriage_h)

    def motion(self, event):
        if self.pause:
            return
        x, y = event.x, event.y
        self.carriage_x = x
        x1 = self.carriage_x - self.carriage_w // 2
        x2 = self.carriage_x + self.carriage_w // 2
        if self.carriage_stop:
            if x1 + 20 >= 0 and x2 - 20 <= self.size_w:
                self.canvas.coords(self.carriage, self.carriage_x - self.carriage_w // 2, self.size_h,
                                   self.carriage_x + self.carriage_w // 2, self.size_h - self.carriage_h)


class Levels:
    def __init__(self) -> None:
        self.levels = None
        self.levels: []
        self.last_level: int = -1
        self.__load_levels()

    def __load_levels(self):
        config = configparser.ConfigParser()
        config.read('conf/player.ini')
        self.last_level = int(config.get('player', 'level'))
        self.levels = [f for f in os.listdir('levels') if re.match(r'^level_\d+\.json$', f)]
