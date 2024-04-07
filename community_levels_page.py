from functools import partial
import i18n
from customtkinter import TOP
from constants import APP_WIDTH, APP_HEIGHT
from custom_components import ListView, CommunityLevelItem, LeaderBoard
from game_frame import GameBoard
from menu_page import MenuPage
from levels import Levels


class CommunityLevels(Levels):
    def __init__(self):
        super().__init__('community')


class CommunityLevelsPage(MenuPage):
    game: GameBoard = None

    def __init__(self, master: any, **kwargs):
        super().__init__(master, i18n.t('community-levels'), True, **kwargs)
        self.levels = None
        self.list = ListView(self)
        self._update()
        self.list.pack(side=TOP, padx=5, pady=5)

    def play(self, level):
        if self.game:
            self.game.destroy()

        self.game = GameBoard(self.master, True, level, True, True, width=APP_WIDTH,
                              height=APP_HEIGHT)
        self.game.set_on_return(self._update)

        self.game.place(x=2, y=0)

    def show_leaderboard(self, level):
        self.leaderboard = LeaderBoard(self.master, level)
        self.leaderboard.grab_set()
        self.leaderboard.show()

    def _update(self):
        self.levels = CommunityLevels()
        self.list.clear()
        # print("--- Community Levels ---")
        for level in self.levels.get_levels().each():
            # print(level.val())
            val = level.val()
            val['parent'] = self.levels.get_levels().key()
            val['key'] = level.key()
            item = CommunityLevelItem(self.list, val)
            item.set_on_play(partial(self.play, val))
            item.set_on_leaderboard(partial(self.show_leaderboard, val))
            self.list.add_item(item)

    def _init_components(self):
        super()._init_components()
