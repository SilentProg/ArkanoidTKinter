from functools import partial

import i18n
from customtkinter import DISABLED, NORMAL, CTkScrollableFrame, X, BOTH, CTkButton, TOP

import firebase
from constants import APP_WIDTH, APP_HEIGHT
from custom_components import ListView, LevelItem, CommunityLevelItem
from game_frame import GameBoard
from menu_page import MenuPage
from levels import Levels


# class CommunityLevels:
#     def __init__(self):
#         self.db = firebase.db
#         self.auth = firebase.auth
#         self.uid = self.auth.current_user['localId']
#         self.levels = self.db.child('community-levels').order_by_child('public').equal_to(True).get()
#         self.complete_levels = self.db.child('users-data').child(self.uid).child(
#             'completed-community-levels').get()
#         print('--- Community Levels ---')
#         print(self.levels)
#         print(self.complete_levels)
#         self._init_complete()
#
#     def _init_complete(self):
#         if self.levels.val() is None:
#             return
#         for level in self.levels.each():
#             level.val()[
#                 'complete'] = True if self.complete_levels.val() and level.key() in self.complete_levels.val() else False
#
#     def get_levels(self):
#         return self.levels

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
            self.list.add_item(item)

    def _init_components(self):
        super()._init_components()
