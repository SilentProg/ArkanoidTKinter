import json
import os
from datetime import datetime

import i18n
from customtkinter import CTkFrame, CTkLabel, CTkFont, CTkButton, CTkImage
from tkinter import Canvas
from tkinter.messagebox import askquestion
from PIL import Image
import pygame
import configparser
import re

import firebase
import i18n_config
from LevelTimer import LevelTimer
from constants import LOCALES_PATH, list_to_dict
from custom_dialogs import InfoDialog, ConfirmDialog


class GameBoard(CTkFrame):
    def __init__(self, master, show_ui, level_name, pause: bool = False, show_start=False, **kwargs):
        super().__init__(master, **kwargs)
        self.on_return = None
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
        self.channel = pygame.mixer.Channel(0)
        self.channel.set_volume(self.settings.getVolume() / 100)
        if not self.settings.getEffectsEnabled():
            self.channel.set_volume(0)
        self.hit_sound = pygame.mixer.Sound("assets/sounds/hit_received.mp3")
        self.collide_sound = pygame.mixer.Sound("assets/sounds/block_collide.mp3")
        self.countdown_sound = pygame.mixer.Sound("assets/sounds/pause_countdown.mp3")
        self.level_failed_sound = pygame.mixer.Sound("assets/sounds/level_failed.mp3")
        self.level_confirm_sound = pygame.mixer.Sound("assets/sounds/level_confirm.mp3")
        self.pause = pause
        self.ball_x, self.ball_y = self.size_w // 2, self.size_h - self.radius - 15
        self.ball_vx, self.ball_vy = -5, -5
        self.showUi = show_ui
        self.level_timer = LevelTimer()
        self.initUI()
        self.initGame()
        if show_start:
            self.after(200, self.askPlay)

    def askPlay(self):
        if ConfirmDialog({
            'title': i18n.t('level'),
            'message': i18n.t('press-to-play'),
            'ok_text': i18n.t('play')
        }).show():
            self.togglePause()
            if not self.level_timer.isRunning():
                self.level_timer.start_level()
        else:
            self.level_info_frame.returnToMenu()

    def togglePause(self):
        self.pause = not self.pause
        if not self.level_timer.isRunning():
            self.level_timer.start_level()
        self.level_info_frame.button_pause.configure(
            image=self.level_info_frame.play_icon if self.pause else self.level_info_frame.pause_icon
        )
        if self.pause:
            self.canvas.unbind('<Key>')
            self.canvas.unbind('<KeyPress>')
            self.canvas.unbind('<KeyRelease>')
            self.canvas.unbind('<Motion>')
            self.level_timer.pause_level()
        else:
            mouse, keyboard = self.settings.getControlsType()
            if keyboard:
                self.canvas.bind('<Key>', self.control)
                self.canvas.bind('<KeyPress>', self.control)
                self.canvas.bind('<KeyRelease>', self.control)
            if mouse:
                self.canvas.bind('<Motion>', self.motion)
            if self.settings.getEffectsEnabled():
                self.channel.play(self.countdown_sound)
                while self.channel.get_busy():
                    pygame.time.wait(100)
            self.level_timer.resume_level()
            self.ball_movement()

    def restart(self, next_level: bool = False):
        self.level_timer.restart()
        self.canvas.delete("all")
        self.walls = []
        self.bricks = []
        self.points = 0
        self.level_info_frame.reInit()
        self.ball_vx, self.ball_vy = -5, -5
        self.ball_x, self.ball_y = self.size_w // 2, self.size_h - self.radius - 15
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

            self.loadItems(self.level.get('bricks', {}), self.bricks)
            self.loadItems(self.level.get('walls', {}), self.walls)

        if self.level and not next_level:
            load()
        elif self.level_path and isinstance(self.level_path, str):
            try:
                print(self.level_path)
                with open(self.level_path, "r") as json_file:
                    self.level = json.load(json_file)
                    load()
            except FileNotFoundError:
                print('File not found')
        elif self.level_path and isinstance(self.level_path, dict):
            self.level = self.level_path['level']
            if 'bricks' in self.level_path:
                self.level['bricks'] = list_to_dict(self.level['bricks']) if isinstance(self.level["bricks"],
                                                                                        list) else self.level.get(
                    'bricks', {})
            if 'walls' in self.level_path:
                self.level['walls'] = list_to_dict(self.level['walls']) if isinstance(self.level["walls"],
                                                                                      list) else self.level.get('walls',
                                                                                                                {})

            load()
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
        ans = askquestion(i18n.t('next-level'), i18n.t('ask-next-level'))
        if ans == 'yes':
            self.level_path = f"levels/level_{self.levels.getLevelNumber() + 1}.json"
            self.restart(next_level=True)

    # метод завантаження блоків
    def loadItems(self, items: {}, array):
        #  перетворюємо список у словник
        if isinstance(items, list):
            items = {index: value for index, value in enumerate(items) if value is not None} if isinstance(items,
                                                                                                           list) else items
        items_keys = list(items.keys())
        # Проходимо по усім елементам словника
        for i in range(0, len(items_keys)):
            key = items_keys[i]
            # Перевіряємо на пусте значення
            if items[key] == {}:
                continue
            # Отримуємо координати та кольори
            x1 = int(items[key]['x1'])
            y1 = int(items[key]['y1'])
            x2 = int(items[key]['x2'])
            y2 = int(items[key]['y2'])
            fill_color = items[key]['fill']
            outline_color = 'white'
            if 'outline' in items[key]:
                outline_color = items[key]['outline']
            # створює об'єкт на ігровому полі
            id_item = self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color, outline=outline_color)
            items.pop(key)  # Вилучаємо зі списку
            # додаємо із новим ключем
            items[str(id_item)] = {'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2, 'fill': fill_color, 'outline': outline_color}
            array.append(id_item)  # додаємо id до списку

    def getCanvas(self) -> Canvas:
        return self.canvas

    def initUI(self):
        self.level_info_frame = LevelInfoFrame(self, self,
                                               width=self.size_w - 15,
                                               height=self.info_frame_size_h - 10)
        self.level_info_frame.button_pause.configure(
            image=self.level_info_frame.play_icon if self.pause else self.level_info_frame.pause_icon
        )
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
            self.channel.play(self.collide_sound)
            self.ball_vy = abs(self.ball_vy)
        if self.ball_x <= self.radius or self.ball_x >= self.size_w - self.radius:
            self.channel.play(self.collide_sound)
            self.ball_vx = -self.ball_vx

        carriage_x1, carriage_y1, carriage_x2, carriage_y2 = self.canvas.coords(self.carriage)

        if carriage_x1 <= self.ball_x <= carriage_x2 and self.ball_y == self.size_h - (self.radius + self.carriage_h):
            self.channel.play(self.collide_sound)
            self.ball_vy = -self.ball_vy
            self.update_point()

        ball_x1, ball_y1, ball_x2, ball_y2 = self.canvas.coords(self.ball)
        overlap = self.canvas.find_overlapping(ball_x1, ball_y1, ball_x2, ball_y2)
        # отримуємо координати м'яча
        ball_x1, ball_y1, ball_x2, ball_y2 = self.canvas.coords(self.ball)
        for ovr in overlap:
            if ovr in self.walls:
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

                    self.channel.play(self.collide_sound)
                else:
                    print("Немає зіткнення")
            # if ovr in self.bricks:
            #     self.canvas.delete(ovr)
            #     self.bricks.pop(self.bricks.index(ovr))
            #     self.update_point()

        brick = self.crash_a_brick()
        if brick in self.bricks:
            self.channel.play(self.collide_sound)
            self.ball_vy = -self.ball_vy
            self.canvas.delete(brick)
            self.bricks.pop(self.bricks.index(brick))
            self.update_point()

        # якщо блоки закінчились
        if len(self.bricks) == 0:
            # Виводимо інворацію про перемогу
            self.channel.play(self.level_confirm_sound)
            self.canvas.create_text(self.size_w // 2, self.size_h // 2, text=i18n.t('win'), fill='green',
                                    font=(None, 50))
            self.carriage_stop = False
            self.level_timer.end_level()
            # готуємо дані для запису у БД
            if isinstance(self.level_path, dict):
                firebase.db.child('users-data').child(firebase.auth.current_user['localId']).child(
                    'completed-' + self.level_path['parent']).child(self.level_path['key']).push(
                    {
                        'date': datetime.now().isoformat(),
                        'score': self.points,
                        'time': self.level_timer.get_elapsed_time(),
                        'spent-hp': self.level_info_frame.max_hp - self.level_info_frame.hp
                    }
                )
                # знайти найкращій результат та записуємо до лідер бордів
                test = firebase.db.child('users-data').child(firebase.auth.current_user['localId']).child(
                    'completed-' + self.level_path['parent']).child(self.level_path['key']).order_by_child(
                    'time').limit_to_first(1).get().val()
                test = test.get(list(test.keys())[0])
                test['displayName'] = firebase.auth.current_user['displayName']
                # Записуємо результат у БД
                firebase.db.child('leaderboards').child(self.level_path['key']).child(
                    firebase.auth.current_user['localId']).set(test)
                # повертаємо до головного меню
                self.after(1000, self.level_info_frame.returnToMenu)
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
                self.canvas.create_text(self.size_w // 2, self.size_h // 2, text=i18n.t('game-over'), fill='red',
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

    # метод керування ракеткою
    def control(self, event):
        # отримання клавіш керування із налаштувань
        right, left = self.settings.getKeyboardKeys()
        # Перевірка на паузу
        if self.pause:
            return
        # отримуємо поточні координати ракетки
        x1, y1, x2, y2 = self.canvas.coords(self.carriage)
        # Переміщуємо ракетку
        if event.keysym == left and x1 + 20 >= 0:
            self.carriage_x -= 10
        if event.keysym == right and x2 - 20 <= self.size_w:
            self.carriage_x += 10
        # перевірка на подію припинення гри
        if self.carriage_stop:
            self.canvas.coords(self.carriage, self.carriage_x - self.carriage_w // 2, self.size_h,
                               self.carriage_x + self.carriage_w // 2, self.size_h - self.carriage_h)

    # метод керування мишкою
    def motion(self, event):
        # Перевірка на паузу
        if self.pause:
            return
        # отримуємо координати мищі
        x, y = event.x, event.y
        self.carriage_x = x
        # пересуваємо каретку
        x1 = self.carriage_x - self.carriage_w // 2
        x2 = self.carriage_x + self.carriage_w // 2
        if self.carriage_stop:
            if x1 + 20 >= 0 and x2 - 20 <= self.size_w:
                self.canvas.coords(self.carriage, self.carriage_x - self.carriage_w // 2, self.size_h,
                                   self.carriage_x + self.carriage_w // 2, self.size_h - self.carriage_h)

    # метод повернення
    def set_on_return(self, _update):
        self.on_return = _update


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
        image = Image.open("assets/icons/pause.png")
        self.pause_icon = CTkImage(light_image=image, dark_image=image)
        image = Image.open("assets/icons/play.png")
        self.play_icon = CTkImage(light_image=image, dark_image=image)
        image = Image.open("assets/icons/restart.png")
        self.restart_icon = CTkImage(light_image=image, dark_image=image)
        self.button_pause = None
        self.initUI()

    def setHp(self, hp):
        self.hp = hp
        self.max_hp = hp
        self.initHp()

    def setMaxHp(self, max_hp):
        self.max_hp = max_hp
        self.initHp()

    def initUI(self):
        button_menu = CTkButton(self, text=i18n.t('menu'), font=self.button_font, height=40, command=self.returnToMenu)
        button_menu.grid(row=0, column=0, padx=10, pady=10)

        self.button_pause = CTkButton(self, text='', image=self.pause_icon, font=self.button_font, width=40, height=40,
                                      command=self.board.togglePause)
        self.button_pause.grid(row=0, column=1, padx=10, pady=10)

        button_restart = CTkButton(self, text='', image=self.restart_icon, font=self.button_font, width=40, height=40,
                                   command=self.board.restart)
        button_restart.grid(row=0, column=2, padx=10, pady=10)

        self.level_label = CTkLabel(self, text=self.board.level_path[
            'title'] if self.board.level_path and 'title' in self.board.level_path else '',
                                    font=self.level_font)
        self.level_label.grid(row=0, column=3, padx=10, pady=10)

        self.level_score = CTkLabel(self, text=i18n.t('score-count', n='0'), font=self.level_font)
        self.level_score.grid(row=0, column=4, padx=10, pady=10)

        hp_label = CTkLabel(self, text=i18n.t('hp-double-dot'), font=self.level_font)
        hp_label.grid(row=0, column=5, padx=10, pady=10)
        self.initHp()

    def reInit(self):
        self.setHp(self.max_hp)
        self.setScore(0)

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
        if not self.board.pause:
            self.board.togglePause()
        self.board.on_return()
        self.after(100, self.board.destroy)

        # self.board.restart()
        # self.togglePause()
        # self.menu_click_sound.play()
        # self.hpHit()

    def setLevel(self, level):
        self.level_label.configure(text=i18n.t('level-number', n=str(level)))

    def setScore(self, score):
        self.level_score.configure(text=i18n.t('score-count', n=str(score)))


class Settings:
    def __init__(self) -> None:
        self.__config = configparser.ConfigParser()
        if not os.path.exists('conf/settings.ini'):
            self.__config.add_section('Sounds')
            self.__config.add_section('Controls')
            self.__config.add_section('Language')
            self.__config.set('Sounds', 'volume', str(100))
            self.__config.set('Sounds', 'effects', str(True))
            self.__config.set('Sounds', 'background', str(True))
            self.__config.set('Controls', 'mouse', str(True))
            self.__config.set('Controls', 'keyboard', str(True))
            self.__config.set('Controls', 'move_right', 'Right')
            self.__config.set('Controls', 'move_left', 'Left')
            self.__config.set('Language', 'default', 'ua')
            self.__reWrite()
        self.__config.read('conf/settings.ini')

    def __reWrite(self):
        with open('conf/settings.ini', 'w') as configfile:
            self.__config.write(configfile)

    def updateLanguage(self, language: str):
        for key, value in self.getAllLanguages().items():
            if value == language:
                self.__config.set('Language', 'default', key)
                self.__reWrite()
                break

    def updateVolume(self, volume: int):
        self.__config.set('Sounds', 'volume', str(volume))
        self.__reWrite()

    def updateSoundsEffects(self, enabled: bool):
        self.__config.set('Sounds', 'effects', str(enabled))
        self.__reWrite()

    def updateSoundsBackground(self, enabled: bool):
        self.__config.set('Sounds', 'background', str(enabled))
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

    def getEffectsEnabled(self):
        return self.__config.get("Sounds", 'effects') == 'True'

    def getBackgroundEnabled(self):
        return self.__config.get("Sounds", 'background') == 'True'

    def getSounds(self):
        effects = False
        background = False

        try:
            effects = self.__config.get("Sounds", 'effects') == 'True'
            background = self.__config.get("Sounds", 'background') == 'True'
        except:
            self.updateSoundsBackground(True)
            self.updateSoundsEffects(True)
            return True, True

        return effects, background

    def getLanguage(self):
        code = self.__config.get('Language', 'default')
        return {'code': code, 'name': self.getAllLanguages()[code]}

    def getAllLanguages(self):
        from os import listdir
        json_files = [file for file in listdir(LOCALES_PATH) if file.endswith('.json')]
        languages = {}
        for file in json_files:
            split = file.split('.')
            if len(split) != 3:
                continue
            languages[split[1]] = split[0]
        return languages

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
