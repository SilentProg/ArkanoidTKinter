from tkinter.simpledialog import askstring

import i18n

import firebase
import i18n_config
from PIL import Image
from customtkinter import CTkFrame, LEFT, CTkButton, CTkLabel, TOP, CTkFont, X, CTkEntry, StringVar, RIGHT, Y, \
    CTkOptionMenu
from tkinter import Canvas, Menu, CURRENT
from tkinter.colorchooser import askcolor
from tkinter.messagebox import showwarning

from constants import APP_WIDTH, APP_HEIGHT
from custom_dialogs import PromptSwitchDialog, InfoDialog
from game_frame import GameBoard
import json


class LBControlPanel(CTkFrame):
    def __init__(self, master, board: GameBoard, **kwargs):
        super().__init__(master, **kwargs)
        self.context_menu = None
        self.frame_color_ball = None
        self.ball_color = 'white'
        self.current_object = None
        self.frame_color_carriage = None
        self.carriage_color = 'white'
        self.font_small = CTkFont(family="Helvetica", size=14, weight="bold")
        self.font_big = CTkFont(family="Helvetica", size=36, weight="bold")
        self.current_color = 'white'
        self.frame_current_color = None
        self.wall_width = StringVar(value='100')
        self.wall_height = StringVar(value='40')
        self.button_try_reset_str = StringVar(value=i18n.t('try'))
        self.option_menu_str = StringVar(value=board.hp)
        self.level: {} = board.level
        self.level_const: {} = board.level
        self.board = board
        self.canvas = board.getCanvas()
        self.initUI()

    def initUI(self):
        frame_bricks = CTkFrame(self, width=self.winfo_reqwidth() - 10, height=200)
        frame_bricks.pack(fill=X, side=TOP, padx=5, pady=5)

        label_list_colors = CTkLabel(frame_bricks, text=i18n.t('choose-color'),
                                     width=frame_bricks.winfo_reqwidth() - 10,
                                     font=self.font_small, corner_radius=50)
        label_list_colors.pack(fill=X, padx=5, pady=5)

        frame_color = CTkFrame(frame_bricks)
        frame_color.pack(fill=X, padx=5, pady=5)

        self.frame_current_color = CTkFrame(frame_color, width=30, height=30, fg_color='white')
        self.frame_current_color.pack(padx=5, pady=5, side=LEFT)

        button_choose_color = CTkButton(frame_color, text=i18n.t('choose'), width=100, command=self.chooseColor)
        button_choose_color.pack(fill=X, padx=5, pady=5)

        button_add_brick = CTkButton(frame_bricks,
                                     text=i18n.t('add-brick'),
                                     command=self.addBrick)
        button_add_brick.pack(fill=X, padx=5, pady=5)

        frame_walls = CTkFrame(self, width=self.winfo_reqwidth() - 10)
        frame_walls.pack(fill=X, padx=5, pady=5)

        label_wall_width = CTkLabel(frame_walls, text=i18n.t('wall-w-h'), font=self.font_small,
                                    width=frame_walls.winfo_reqwidth() - 10)
        label_wall_width.pack(fill=X, padx=5, pady=5)

        entry_wall_width = CTkEntry(frame_walls, placeholder_text="100", textvariable=self.wall_width)
        entry_wall_width.pack(fill=X, padx=5, pady=5)

        entry_wall_height = CTkEntry(frame_walls, placeholder_text="100", textvariable=self.wall_height)
        entry_wall_height.pack(fill=X, padx=5, pady=5)

        button_add_brick = CTkButton(frame_walls,
                                     text=i18n.t('add-wall'),
                                     command=self.addWall)
        button_add_brick.pack(fill=X, padx=5, pady=5)

        frame_ball = CTkFrame(self, width=self.winfo_reqwidth() - 10)
        frame_ball.pack(fill=X, padx=5, pady=5)

        label_ball_color = CTkLabel(frame_ball, text=i18n.t('ball-color'), font=self.font_small,
                                    width=frame_ball.winfo_reqwidth() - 10)
        label_ball_color.pack(fill=X, padx=5, pady=5)

        frame_color_ball_container = CTkFrame(frame_ball)
        frame_color_ball_container.pack(fill=X, padx=5, pady=5)

        self.frame_color_ball = CTkFrame(frame_color_ball_container, width=30, height=30, fg_color='white')
        self.frame_color_ball.pack(padx=5, pady=5, side=LEFT)

        button_choose_ball_color = CTkButton(frame_color_ball_container, text=i18n.t('choose'), width=100,
                                             command=self.chooseBallColor)
        button_choose_ball_color.pack(fill=X, padx=5, pady=5)

        frame_carriage = CTkFrame(self, width=self.winfo_reqwidth() - 10)
        frame_carriage.pack(fill=X, padx=5, pady=5)

        label_carriage_color = CTkLabel(frame_carriage, text=i18n.t('carriage-color'), font=self.font_small,
                                        width=frame_carriage.winfo_reqwidth() - 10)
        label_carriage_color.pack(fill=X, padx=5, pady=5)

        frame_color_carriage_container = CTkFrame(frame_carriage)
        frame_color_carriage_container.pack(fill=X, padx=5, pady=5)

        self.frame_color_carriage = CTkFrame(frame_color_carriage_container, width=30, height=30, fg_color='white')
        self.frame_color_carriage.pack(padx=5, pady=5, side=LEFT)

        button_choose_carriage_color = CTkButton(frame_color_carriage_container, text=i18n.t('choose'), width=100,
                                                 command=self.chooseCarriageColor)
        button_choose_carriage_color.pack(fill=X, padx=5, pady=5)

        frame_hp = CTkFrame(self)
        frame_hp.pack(fill=X, padx=5, pady=5)

        option_menu_hp = CTkOptionMenu(frame_hp, values=[i18n.t('hp-double-dot-number', hp='1'),
                                                         i18n.t('hp-double-dot-number', hp='2'),
                                                         i18n.t('hp-double-dot-number', hp='3')],
                                       variable=self.option_menu_str)
        option_menu_hp.pack(fill=X, padx=5, pady=5)

        frame_control_buttons = CTkFrame(self)
        frame_control_buttons.pack(fill=X, padx=5, pady=5)

        button_try_reset = CTkButton(frame_control_buttons, textvariable=self.button_try_reset_str,
                                     command=self.tryReset)
        button_try_reset.pack(fill=X, padx=5, pady=5)

        button_save = CTkButton(frame_control_buttons, text=i18n.t('save'), command=self.saveLevel)
        button_save.pack(fill=X, padx=5, pady=5)

        self.context_menu = Menu(self, tearoff=0)
        self.context_menu.add_command(label=i18n.t('delete'), command=self.deleteObj)
        self.canvas.bind("<Button-3>", self.show_context_menu)

        def validate_input(line):
            if line == "" or line.isdigit():
                return True
            else:
                return False

        validate_func = self.register(validate_input)
        entry_wall_width.configure(validate="key", validatecommand=(validate_func, "%P"))
        entry_wall_height.configure(validate="key", validatecommand=(validate_func, "%P"))

    def getLevel(self) -> {}:
        return self.level

    def tryReset(self):

        if self.button_try_reset_str.get() == i18n.t('try'):
            self.level = self.level_const
            self.button_try_reset_str.set(i18n.t('reset'))
            self.board.togglePause()
        else:
            self.level_const = self.level
            self.button_try_reset_str.set(i18n.t('try'))
            self.board.restart()
            self.board.togglePause()

    def show_context_menu(self, event):
        obj = self.canvas.find_withtag(CURRENT)
        if len(obj) == 0 or obj[0] in [self.canvas.find_withtag('ball')[0], self.canvas.find_withtag('carriage')[0]]:
            return
        self.current_object = obj[0]
        self.context_menu.post(event.x_root, event.y_root)

    def deleteObj(self):
        print("delete")
        print(self.current_object)
        if self.current_object is not None:
            self.canvas.delete(self.current_object)
            if str(self.current_object) in self.level['bricks']:
                del self.level['bricks'][(str(self.current_object))]
            if str(self.current_object) in self.level['walls']:
                del self.level['walls'][str(self.current_object)]
            self.current_object = None

    def saveLevel(self):
        self.updateAllObjs()
        result = PromptSwitchDialog({'title': i18n.t('level-save'),
                                     'entry_prompt': i18n.t('ask-level-title'),
                                     'switch_prompt': i18n.t('ask-make-public'),
                                     'ok_text': i18n.t('save')}
                                    ).show()
        file_name = result['entry_value']
        public = result['switch_value']
        # json_string = json.dumps(self.level, indent=4)

        if file_name:
            firebase.db.child("community-levels").push({
                'creatorName': firebase.auth.current_user['displayName'],
                'creatorLocalId': firebase.auth.current_user['localId'],
                'public': public,
                'title': file_name,
                'level': self.level
            })
            InfoDialog({
                'title': i18n.t('level-save'),
                'message': i18n.t('level-saved')
            }).show()
            # with open("levels/{}.json".format(file_name), "w") as json_file:
            #     json_file.write(json_string)

    def addBrick(self):
        print("block_added")
        brick_w = 100
        brick_h = 40
        x1, y1, x2, y2 = self.calcPos(brick_w, brick_h)
        id_brick = self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.current_color)
        self.board.bricks.append(id_brick)
        self.level['bricks'][str(id_brick)] = {
            'x1': x1,
            'y1': y1,
            'x2': x2,
            'y2': y2,
            'fill': str(self.current_color)
        }

    def addWall(self):
        if not self.wall_height.get() or not self.wall_width.get():
            showwarning(i18n.t('Warning'), i18n.t('invalid-size'))
            return
        print("wall_added")
        wall_w = int(self.wall_width.get())
        wall_h = int(self.wall_height.get())
        x1, y1, x2, y2 = self.calcPos(wall_w, wall_h)
        id_wall = self.canvas.create_rectangle(x1, y1, x2, y2, fill='#561243', outline='#a2227e')
        self.board.walls.append(id_wall)
        self.level['walls'][str(id_wall)] = {
            'x1': x1,
            'y1': y1,
            'x2': x2,
            'y2': y2,
            'fill': '#561243',
            'outline': '#a2227e'
        }

    def calcPos(self, w, h):
        canvas_w = self.canvas.winfo_reqwidth()
        canvas_h = self.canvas.winfo_reqheight()
        x = canvas_w // 2 - w // 2
        y = canvas_h - 150 - h // 2
        return x, y, x + w, y + h

    def chooseColor(self):
        self.current_color = askcolor(title=i18n.t('choose-color-brick'))[1]
        if self.current_color:
            self.frame_current_color.configure(fg_color=self.current_color)

    def chooseBallColor(self):
        self.ball_color = askcolor(title=i18n.t('choose-color-ball'))[1]
        if self.ball_color:
            self.frame_color_ball.configure(fg_color=self.ball_color)
            self.canvas.itemconfigure(self.canvas.find_withtag('ball')[0], fill=self.ball_color)
            self.level['ball']['color'] = str(self.ball_color)

    def chooseCarriageColor(self):
        self.carriage_color = askcolor(title=i18n.t('choose-color-carriage'))[1]
        if self.carriage_color:
            self.frame_color_carriage.configure(fg_color=self.carriage_color)
            self.canvas.itemconfigure(self.canvas.find_withtag('carriage')[0], fill=self.carriage_color)
            self.level['carriage']['color'] = str(self.carriage_color)

    def updateObj(self, current_obj):
        if not current_obj:
            return
        print("Current obj: {}".format(current_obj))
        print("Level obj: {}".format(self.level))
        x1, y1, x2, y2 = self.canvas.coords(current_obj)
        fill_color = self.canvas.itemcget(current_obj, 'fill')
        outline_color = self.canvas.itemcget(current_obj, 'outline')
        if str(current_obj) in self.level['bricks']:
            print("update brick")
            self.level['bricks'].update(
                {
                    str(current_obj): {
                        'x1': x1,
                        'y1': y1,
                        'x2': x2,
                        'y2': y2,
                        'fill': fill_color
                    }
                }
            )
            print(self.level['bricks'])
        if str(current_obj) in self.level['walls']:
            print("update wall")
            self.level['walls'].update({
                str(current_obj): {
                    'x1': x1,
                    'y1': y1,
                    'x2': x2,
                    'y2': y2,
                    'fill': fill_color,
                    'outline': outline_color
                }
            })
            print(self.level['walls'])

    def updateAllObjs(self):
        hp = self.option_menu_str.get()
        if hp == i18n.t('hp-double-dot-number', hp=1):
            self.level['hp'] = 1
        elif hp == i18n.t('hp-double-dot-number', hp=2):
            self.level['hp'] = 1
        elif hp == i18n.t('hp-double-dot-number', hp=3):
            self.level['hp'] = 3
        self.canvas.itemconfigure(self.canvas.find_withtag('carriage')[0], fill=self.carriage_color)
        self.level['carriage']['color'] = str(self.carriage_color)
        self.canvas.itemconfigure(self.canvas.find_withtag('ball')[0], fill=self.ball_color)
        self.level['ball']['color'] = str(self.ball_color)


class LevelBuilder(CTkFrame):
    def __init__(self, master, level_path: str = None, **kwargs):
        super().__init__(master, **kwargs)
        self.canvas: Canvas = Canvas(self)
        self.current_object = None
        self.current_object_w = 0
        self.current_object_h = 0
        self.start_x = None
        self.start_y = None
        self.level_path = level_path
        self.object_center_x = None
        self.object_center_y = None

        self.control_panel: LBControlPanel = None
        self.initUI()

    def initUI(self):
        game_board = GameBoard(self, False, self.level_path, True, width=APP_WIDTH, height=APP_HEIGHT)

        self.canvas = game_board.getCanvas()
        self.control_panel = LBControlPanel(self, game_board, width=190, height=self.master.winfo_height() - 10)
        self.control_panel.pack(side=RIGHT, fill=Y, padx=5, pady=5)
        # game_board.pack(padx=5, pady=5)
        game_board.place(x=0, y=0)

        # self.canvas = Canvas(self, width=1060, height=630, bg='black')
        # self.canvas.pack(side=LEFT)

        self.canvas.bind("<ButtonPress-1>", self.start_drag)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drag)
        self.canvas.bind("<B1-Motion>", self.drag)

    def find_center(self, item):
        x1, y1, x2, y2 = self.canvas.coords(item)
        return (x1 + x2) / 2, (y1 + y2) / 2

    def start_drag(self, event):
        self.current_object = self.canvas.find_closest(event.x, event.y)[0]
        if self.current_object in [self.canvas.find_withtag('ball')[0], self.canvas.find_withtag('carriage')[0]]:
            self.current_object = None
            return
        self.object_center_x, self.object_center_y = self.find_center(self.current_object)
        x1, y1, x2, y2 = self.canvas.coords(self.current_object)
        self.current_object_w = x2 - x1
        self.current_object_h = y2 - y1
        self.start_x = event.x
        self.start_y = event.y

    def stop_drag(self, event):
        self.control_panel.updateObj(self.current_object)
        self.current_object = None
        self.current_object_w = 0
        self.current_object_h = 0

    def drag(self, event):
        if self.current_object:
            delta_x = event.x - self.start_x
            delta_y = event.y - self.start_y
            new_center_x = self.object_center_x + delta_x
            new_center_y = self.object_center_y + delta_y
            new_x = round(new_center_x / 10) * 10
            new_y = round(new_center_y / 10) * 10
            self.canvas.coords(self.current_object, new_x - self.current_object_w / 2,
                               new_y - self.current_object_h / 2, new_x + self.current_object_w / 2,
                               new_y + self.current_object_h / 2)
