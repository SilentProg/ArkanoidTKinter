from functools import partial

import i18n
from customtkinter import DISABLED, NORMAL, CTkScrollableFrame, X, BOTH, CTkButton

from constants import APP_WIDTH, APP_HEIGHT
from game_frame import Levels, GameBoard
from menu_page import MenuPage


class LevelsPage(MenuPage):
    levels: Levels = None
    game: GameBoard = None

    def __init__(self, master: any, **kwargs):
        super().__init__(master, i18n.t('levels'), True, **kwargs)

    def _init_components(self):
        super()._init_components()
        self.levels = Levels()

        levels_frame = CTkScrollableFrame(self, height=100)
        levels_frame.pack(fill=X, padx=5, pady=5)

        level_number = 1
        row = 0
        col = 0
        for level in self.levels.levels:
            state = NORMAL
            color = 'green'
            if level_number > self.levels.last_level + 1:
                state = DISABLED
                color = 'gray'
            if level_number == self.levels.last_level + 1:
                color = 'blue'
            button = CTkButton(levels_frame, text=f"{level_number}", fg_color=color, width=55, height=55, state=state,
                               font=self.button_font, command=partial(self.loadLevel, level_number))
            button.grid(row=row, column=col, padx=5, pady=5)
            level_number += 1
            col += 1
            if col > 2:
                col = 0
                row += 1

    def loadLevel(self, level):
        if self.game:
            self.game.destroy()

        self.game = GameBoard(self.master, True, f'levels/level_{level}.json', width=APP_WIDTH,
                              height=APP_HEIGHT)
        self.game.place(x=2, y=0)
