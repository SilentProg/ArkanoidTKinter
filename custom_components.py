import i18n

import firebase
import i18n_config
from customtkinter import CTkScrollableFrame, CTkFrame, TOP, BOTH, CTkLabel, LEFT, CTkButton, RIGHT, CTkImage, X
from PIL import Image

from menu_page import MenuPage


class ListView(CTkScrollableFrame):
    def __init__(self, master: any, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(width=400, height=300)
        self.items = []

    def add_item(self, item: CTkFrame):
        self.items.append(item)
        item.pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=5)

    def clear(self):
        for item in self.items:
            item.destroy()
        self.items.clear()


class LevelItem(CTkFrame):
    def __init__(self, master: any, level: {}, **kwargs):
        super().__init__(master, **kwargs)

        self.level = level

        self.title_label = CTkLabel(self, text=level['title'], width=200, justify='left')
        self.title_label.pack(side=LEFT, padx=10, pady=10)

        self.creator = CTkLabel(self, text=i18n.t('creator-name', creator=level['creatorName']))
        self.creator.pack(side=LEFT, padx=10, pady=10)

        self.hp_counter = CTkLabel(self, text=i18n.t('hp-double-dot-number', hp=level['level']['hp']))
        self.hp_counter.pack(side=LEFT, padx=10, pady=10)

        image = Image.open('assets/icons/trash.png')
        icon = CTkImage(dark_image=image, light_image=image, size=(25, 25))
        self.delete_button = CTkButton(self, image=icon, text="", fg_color='red', width=30)
        self.delete_button.pack(side=RIGHT, padx=5, pady=5)

        image = Image.open('assets/icons/settings.png')
        icon = CTkImage(dark_image=image, light_image=image, size=(25, 25))
        self.load_button = CTkButton(self, text="", image=icon, width=30)
        self.load_button.pack(side=RIGHT, padx=5, pady=5)

    def set_on_delete(self, func):
        def delete(level):
            if func(level):
                self.pack_forget()
                self.destroy()

        self.delete_button.configure(command=lambda: delete(self.level))

    def set_on_load(self, func):
        self.load_button.configure(command=lambda: func(self.level))


class CommunityLevelItem(CTkFrame):
    def __init__(self, master: any, level: {}, **kwargs):
        super().__init__(master, **kwargs)
        self.level = level
        self.title_label = CTkLabel(self, text=level['title'], width=150, justify='left')
        self.title_label.pack(side=LEFT, fill=X, expand=True, padx=10, pady=10)

        self.creator = CTkLabel(self, text=level['creatorName'])
        self.creator.pack(side=LEFT, padx=10, pady=10)

        self.hp_counter = CTkLabel(self, text=i18n.t('hp-double-dot-number', hp=level['level']['hp']))
        self.hp_counter.pack(side=LEFT, padx=10, pady=10)

        image = Image.open('assets/icons/play.png')
        icon = CTkImage(dark_image=image, light_image=image)
        self.play_button = CTkButton(self, image=icon, text='', width=25)
        self.play_button.pack(side=RIGHT, padx=10, pady=10)
        if level['complete']:
            self.play_button.configure(fg_color=i18n.t('complete_color'))

        image = Image.open('assets/icons/leadership.png')
        icon = CTkImage(dark_image=image, light_image=image)
        self.leaderboard_button = CTkButton(self, image=icon, text='', width=25)
        self.leaderboard_button.pack(side=RIGHT, padx=5, pady=10)

    def set_on_leaderboard(self, func):
        self.leaderboard_button.configure(command=func)

    def set_on_play(self, func):
        self.play_button.configure(command=func)


class LeaderBoardItem(CTkFrame):
    def __init__(self, master: any, number: int, result: dict, **kwargs):
        super().__init__(master, **kwargs)
        self.result = result

        self.number_label = number
        self.number_label = CTkLabel(self, width=20, text="№"+str(number))
        self.number_label.pack(side=LEFT, padx=5, pady=5)

        self.display_name = CTkLabel(self, text=result['displayName'])
        self.display_name.pack(side=LEFT, padx=5, pady=5)

        self.score_label = CTkLabel(self, text=i18n.t('score-count', n=result['score']))
        self.score_label.pack(side=LEFT, padx=5, pady=5)

        self.spent_hp = CTkLabel(self, text=i18n.t('v-hp-double-dot-number', hp=result['spent-hp']))
        self.spent_hp.pack(side=LEFT, padx=5, pady=5)

        self.time = CTkLabel(self, text=i18n.t('spent-time', time=round(result['time'], 4)))
        self.time.pack(side=LEFT, padx=5, pady=5)


class LeaderBoard(MenuPage):
    def __init__(self, master: any, level: dict, **kwargs):
        super().__init__(master, 'Лідери', True, **kwargs)
        self.level = level
        self.level_title_frame = CTkFrame(self)

        self.level_title_label = CTkLabel(self.level_title_frame, text=self.level['title'])
        self.level_title_label.pack(side=TOP, padx=5, pady=5)

        self.level_title_frame.pack(side=TOP, fill=X, expand=True, padx=5, pady=5)

        self.list = ListView(self)

        items = firebase.db.child('leaderboards').child(level['key']).order_by_child('time').get()
        counter = 0
        if items.val() is not None:
            for item in items.each():
                val = item.val()
                print(val)
                counter += 1
                self.list.add_item(LeaderBoardItem(self.list, counter, val))

        self.list.pack(side=TOP, padx=5, pady=5)

    def _init_components(self):
        super()._init_components()
        self.button_back.configure(text='×')
        self.set_on_back(self.destroy)


