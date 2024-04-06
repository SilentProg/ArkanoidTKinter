from functools import partial

import i18n
from customtkinter import DISABLED, NORMAL, CTkScrollableFrame, X, BOTH, CTkButton, TOP

import firebase
from constants import APP_WIDTH, APP_HEIGHT
from custom_components import ListView, LevelItem, CommunityLevelItem
from game_frame import Levels, GameBoard
from menu_page import MenuPage


class CommunityLevels:
    def __init__(self):
        self.db = firebase.db
        self.auth = firebase.auth
        self.uid = self.auth.current_user['localId']
        self.levels = self.db.child('community-levels').order_by_child('public').equal_to(True).get()
        self.complete_levels = self.db.child('users-data').child(self.uid).child(
            'completed-community-levels').get()
        print('--- Community Levels ---')
        print(self.levels)
        print(self.complete_levels)
        self._init_complete()

    def _init_complete(self):
        if self.levels.val() is None:
            return
        for level in self.levels.each():
            level.val()['complete'] = True if self.complete_levels.val() and level.key() in self.complete_levels.val() else False



    def get_levels(self):
        return self.levels


class CommunityLevelsPage(MenuPage):
    game: GameBoard = None

    def __init__(self, master: any, **kwargs):
        super().__init__(master, i18n.t('community-levels'), True, **kwargs)
        self.levels = CommunityLevels()
        self.list = ListView(self)
        print("--- Community Levels ---")
        for level in self.levels.get_levels().each():
            print(level.val())
            # self.list.add_item(CommunityLevelItem(self.list, level))

        self.list.pack(side=TOP)

    def _init_components(self):
        super()._init_components()

    def loadLevel(self, level):
        if self.game:
            self.game.destroy()

        # self.game = GameBoard(self.master, True, f'levels/level_{level}.json', width=APP_WIDTH,
        #                       height=APP_HEIGHT)
        self.game.place(x=2, y=0)
