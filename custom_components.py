import i18n
import i18n_config
from customtkinter import CTkScrollableFrame, CTkFrame, TOP, BOTH, CTkLabel, LEFT, CTkButton, RIGHT, CTkImage, X
from PIL import Image


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

    def set_on_play(self, func):
        self.play_button.configure(command=func)
