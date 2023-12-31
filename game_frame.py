import json
import os
from customtkinter import CTkFrame, CTkLabel, CTkFont, CTkButton, CTkImage
from tkinter import Canvas
from tkinter.messagebox import askquestion
from PIL import Image
import pygame
import configparser
import re


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
        self.settings = Settings()
        self.levels = Levels()
        pygame.mixer.init()
        self.channel = pygame.mixer.Channel(0)
        self.channel.set_volume(self.settings.getVolume())
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

    def restart(self, next_level: bool = False):
        self.canvas.delete("all")
        self.walls = []
        self.bricks = []
        self.points = 0
        self.level_info_frame.reInit()
        self.ball_vx, self.ball_vy = -5, -5
        self.ball_x, self.ball_y = self.size_w // 2, self.size_h // 2
        self.carriage_x = self.size_w // 2
        self.loadLevel(next_level)
        if not self.carriage_stop:
            self.carriage_stop = True
            self.ball_movement()

    def loadLevel(self, next_level: bool = False):
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

        if self.level and not next_level:
            load()
        elif self.level_path:
            try:
                print(self.level_path)
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

    def nextLevel(self):
        if self.levels.getLevelNumber() + 1 > len(self.levels.levels):
            return
        ans = askquestion("Наступний рівень", "Перейти до наступного рівня?")
        if ans == 'yes':
            self.level_path = f"levels/level_{self.levels.getLevelNumber() + 1}.json"
            self.restart(next_level=True)

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
        self.level_info_frame = LevelInfoFrame(self, self,
                                               width=self.size_w - 15,
                                               height=self.info_frame_size_h - 10)
        if self.showUi:
            self.level_info_frame.pack(padx=5, pady=5)

    def initGame(self):
        self.canvas = Canvas(self, width=self.size_w, height=self.size_h, bg='black')
        print(f'canvas size {self.canvas.winfo_reqwidth()} * {self.canvas.winfo_reqheight()}')
        self.canvas.focus_set()
        self.canvas.pack(padx=5, pady=5)

        self.loadLevel()

        if not self.pause:
            self.ball_movement()
        mouse, keyboard = self.settings.getControlsType()
        if keyboard:
            self.canvas.bind('<Key>', self.control)
            self.canvas.bind('<KeyPress>', self.control)
            self.canvas.bind('<KeyRelease>', self.control)
        if mouse:
            self.canvas.bind('<Motion>', self.motion)

    def ball_movement(self):
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
            self.channel.play(self.level_confirm_sound)
            self.canvas.create_text(self.size_w // 2, self.size_h // 2, text='You WIN!', fill='green', font=(None, 50))
            self.carriage_stop = False
            self.levels.updateLastFromPath(self.level_path, self.points)
            self.nextLevel()
            return

        if self.ball_y < (self.size_h - self.radius):
            if not self.pause:
                self.root.after(self.interval, self.ball_movement)
        else:
            if self.hp > 1:
                self.channel.play(self.hit_sound)
                self.hp -= 1
                self.level_info_frame.hpHit()
                self.ball_vy = -self.ball_vy
                self.root.after(self.interval, self.ball_movement)
            else:
                self.channel.play(self.level_failed_sound)
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
        right, left = self.settings.getKeyboardKeys()
        if self.pause:
            return
        x1, y1, x2, y2 = self.canvas.coords(self.carriage)
        if event.keysym == left and x1 + 20 >= 0:
            self.carriage_x -= 10
        if event.keysym == right and x2 - 20 <= self.size_w:
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


class LevelInfoFrame(CTkFrame):

    def __init__(self, master, board: GameBoard, **kwargs):
        super().__init__(master, **kwargs)
        self.level = board.level
        self.level_label = None
        self.level_score = None
        self.board: GameBoard = board
        self.hp = board.hp
        self.max_hp = board.hp
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

        button_pause = CTkButton(self, text="P", font=self.button_font, width=40, height=40,
                                 command=self.board.togglePause)
        button_pause.grid(row=0, column=1, padx=10, pady=10)

        button_restart = CTkButton(self, text="R", font=self.button_font, width=40, height=40,
                                   command=self.board.restart)
        button_restart.grid(row=0, column=2, padx=10, pady=10)

        self.level_label = CTkLabel(self, text="Level: {} |".format(self.board.levels.getLevelNumber() + 1),
                                    font=self.level_font)
        self.level_label.grid(row=0, column=3, padx=10, pady=10)

        self.level_score = CTkLabel(self, text="Score: {} |".format(0), font=self.level_font)
        self.level_score.grid(row=0, column=4, padx=10, pady=10)

        hp_label = CTkLabel(self, text="HP:", font=self.level_font)
        hp_label.grid(row=0, column=5, padx=10, pady=10)
        self.initHp()

    def reInit(self):
        self.setHp(self.max_hp)
        self.setScore(0)
        self.setLevel(self.board.levels.getLevelNumber() + 1)

    def initHp(self):
        print(self.hp)
        for image in self.hp_bar:
            image.destroy()
        self.hp_bar.clear()
        column = 6
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
        self.board.togglePause()
        self.after(100, self.board.destroy)
        # self.board.restart()
        # self.togglePause()
        # self.menu_click_sound.play()
        # self.hpHit()

    def setLevel(self, level):
        self.level_label.configure(text="Level: {} |".format(str(level)))

    def setScore(self, score):
        self.level_score.configure(text="Score: {} |".format(str(score)))


class Levels:
    def __init__(self) -> None:
        self.levels: []
        self.last_level: int = -1
        self.__config = configparser.ConfigParser()
        self.__load_levels()

    def updateLevels(self):
        self.__load_levels()

    def __load_levels(self):
        if not os.path.exists('conf/player.ini'):
            self.__config.add_section('Player')
            self.__config.set('Player', 'level', '1')
            self.__reWrite()
        self.__config.read('conf/player.ini')
        self.last_level = int(self.__config.get('Player', 'level'))
        self.levels = [f for f in os.listdir('levels') if re.match(r'^level_\d+\.json$', f)]

    def __reWrite(self):
        with open('conf/player.ini', 'w') as configfile:
            self.__config.write(configfile)

    def getLevelNumber(self):
        self.__load_levels()
        return self.last_level

    def __getLevelNumber(self, level_path):
        start_index = level_path.find("_") + 1
        end_index = level_path.find(".json")
        number_str = level_path[start_index:end_index]
        return int(number_str)

    def updateLastFromPath(self, level_number: str, score: int):
        level_number = self.__getLevelNumber(level_number)
        self.updateLast(level_number, score)

    def updateLast(self, level_number: int, score: int):
        last = int(self.__config.get('Player', 'level'))
        if level_number > last:
            self.last_level = level_number
            self.__config.set('Player', 'level', str(level_number))
        level = f'{level_number}'
        try:
            sc = int(self.__config.get(level, 'score'))
            if sc < score:
                self.__config.set(level, 'score', str(score))
        except:
            self.__config.add_section(level)
            self.__config.set(level, 'score', str(score))
            self.__config.set(level, 'confirm', '1')
        self.__reWrite()


class Settings:
    def __init__(self) -> None:
        self.__config = configparser.ConfigParser()
        if not os.path.exists('conf/settings.ini'):
            self.__config.add_section('Sounds')
            self.__config.add_section('Controls')
            self.__config.set('Sounds', 'volume', str(100))
            self.__config.set('Controls', 'mouse', str(True))
            self.__config.set('Controls', 'keyboard', str(True))
            self.__config.set('Controls', 'move_right', 'Right')
            self.__config.set('Controls', 'move_left', 'Left')
            self.__reWrite()
        self.__config.read('conf/settings.ini')

    def __reWrite(self):
        with open('conf/settings.ini', 'w') as configfile:
            self.__config.write(configfile)

    def updateVolume(self, volume: int):
        self.__config.set('Sounds', 'volume', str(volume))
        self.__reWrite()

    def updateMouseControl(self, mouse_control):
        self.__config.set('Controls', 'mouse', mouse_control)
        self.__reWrite()

    def updateKeyboardControl(self, keyboard_control):
        self.__config.set('Controls', 'keyboard', keyboard_control)
        self.__reWrite()

    def updateMoveRight(self, move_right: str):
        self.__config.set('Controls', 'move_right', move_right)
        self.__reWrite()

    def updateMoveLeft(self, move_left: str):
        self.__config.set('Controls', 'move_left', move_left)
        self.__reWrite()

    def getVolume(self):
        return int(self.__config.get("Sounds", 'volume'))

    def getControlsType(self):
        mouse = False
        keyboard = False

        if self.__config.get("Controls", 'mouse') == 'True':
            mouse = True
        if self.__config.get("Controls", 'keyboard') == 'True':
            keyboard = True

        return mouse, keyboard

    def getKeyboardKeys(self):
        return self.__config.get("Controls", 'move_right'), self.__config.get("Controls", 'move_left')
