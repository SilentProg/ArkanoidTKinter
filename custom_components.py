import i18n
import i18n_config
from customtkinter import CTkScrollableFrame, CTkFrame, TOP, BOTH, CTkLabel, LEFT, CTkButton


class ListView(CTkScrollableFrame):
    def __init__(self, master: any, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(width=300, height=600)
        self.items = []

    def add_item(self, item: CTkFrame):
        self.items.append(item)
        item.pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=5)


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

