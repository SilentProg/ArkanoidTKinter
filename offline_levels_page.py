from functools import partial

import i18n
from customtkinter import DISABLED, NORMAL, CTkScrollableFrame, X, BOTH, CTkButton

import firebase
from constants import APP_WIDTH, APP_HEIGHT
from game_frame import GameBoard, Levels
from menu_page import MenuPage


class LevelsPage(MenuPage):
    levels: Levels = None
    game: GameBoard = None

    def __init__(self, master: any, **kwargs):
        super().__init__(master, i18n.t('levels'), True, **kwargs)

    def _init_components(self):
        super()._init_components()
        self.levels = Levels()



    def loadLevel(self, level):
        if self.game:
            self.game.destroy()

        self.game = GameBoard(self.master, True, f'levels/level_{level}.json', width=APP_WIDTH,
                              height=APP_HEIGHT)
        self.game.place(x=2, y=0)
