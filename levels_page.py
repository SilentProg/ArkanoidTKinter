from functools import partial

import i18n
from customtkinter import DISABLED, NORMAL, CTkScrollableFrame, X, BOTH, CTkButton, TOP

import firebase
from constants import APP_WIDTH, APP_HEIGHT
from custom_components import ListView, CommunityLevelItem, LeaderBoard
from game_frame import GameBoard
from menu_page import MenuPage
from levels import Levels


class CampaignLevels(Levels):
    def __init__(self):
        super().__init__('levels')

    def get_next_level(self):
        for level in self.get_levels().each():
            if not level.val()['complete']:
                return level.val()
        return self.get_levels().each()[-1].val()


class LevelsPage(MenuPage):
    levels: Levels = None
    game: GameBoard = None

    def __init__(self, master: any, **kwargs):
        super().__init__(master, i18n.t('levels'), True, **kwargs)
        self.db = firebase.db

    def _init_components(self):
        super()._init_components()
        self.levels: CampaignLevels = None
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
        self.levels = CampaignLevels()
        self.list.clear()
        # print("--- Community Levels ---")
        next_level = True
        for level in self.levels.get_levels().each():
            # print(level.val())
            val = level.val()
            val['parent'] = self.levels.get_levels().key()
            val['key'] = level.key()
            item = CommunityLevelItem(self.list, val)

            if not val['complete'] and not next_level:
                item.play_button.configure(fg_color=i18n.t('disable_color'))
                item.play_button.configure(state=DISABLED)

            if not val['complete']:
                next_level = False

            item.creator.pack_forget()
            item.hp_counter.pack_forget()
            item.set_on_play(partial(self.play, val))
            item.set_on_leaderboard(partial(self.show_leaderboard, val))
            self.list.add_item(item)
