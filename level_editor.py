import i18n

import firebase
import i18n_config
from customtkinter import BOTH, CTkToplevel, CTkLabel, CTkButton, CTkTabview, LEFT, Y
from tkinter import Menu
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import askyesno as ConfirmDialog

from constants import isAuth, isAdmin
from custom_components import ListView, LevelItem
from custom_dialogs import InfoDialog
from level_builder import LevelBuilder


class LevelEditor(CTkToplevel):
    def __init__(self):
        super().__init__()

        if not isAuth():
            InfoDialog({
                'title': i18n.t('auth-error'),
                'message': i18n.t('permission-denied')
            }).show()
            self.destroy()

        self.current_page = None
        self.app_width = 1200
        self.app_height = 660
        self.initUI()
        self.initMainMenu()
        self._init_components()

    def _init_components(self):
        self.tab_view = CTkTabview(self)
        if isAdmin():
            tab = self.tab_view.add(i18n.t('levels'))
            levels_list = ListView(tab)
            levels_list.pack(expand=True, fill="both")

            for level in firebase.db.child('community-levels').get().each():
                val = level.val()
                val['key'] = level.key()
                levels_list.add_item(LevelItem(levels_list, val))



        self.tab_view.add(i18n.t('title'))

        self.tab_view.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)



    def initUI(self):
        self.grab_set()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (self.app_width // 2)
        y = (screen_height // 2) - (self.app_height // 2)
        self.geometry(f"{self.app_width}x{self.app_height}+{x}+{y}")
        self.title(i18n.t('level-editor-title'))
        self.resizable(False, False)

    def initMainMenu(self):
        menubar = Menu(self)
        self.config(menu=menubar)

        fileMenu = Menu(menubar, tearoff=0)
        levelMenu = Menu(menubar, tearoff=0)

        levelMenu.add_command(label=i18n.t('new-level'), command=self.newLevel)
        levelMenu.add_command(label=i18n.t('load-level'), command=self.loadLevel)

        fileMenu.add_cascade(label=i18n.t('level'), menu=levelMenu)
        fileMenu.add_command(label=i18n.t('quit'), command=self.onExit)
        menubar.add_cascade(label=i18n.t('menu-file'), menu=fileMenu)

    def onExit(self):
        answer = ConfirmDialog(title=i18n.t('confirmation'), message=i18n.t('ask-quit'))
        if answer:
            self.destroy()

    def newLevel(self):
        def create():
            self.current_page = LevelBuilder(self, width=self.app_width, height=self.app_height)
            self.current_page.pack(fill=BOTH, expand=True)

        if self.current_page:
            answer = ConfirmDialog(title=i18n.t('confirmation'), message=i18n.t('ask-new-level'))
            if answer:
                self.current_page.destroy()
                create()
        else:
            create()

    def loadLevel(self):
        import os

        def load():
            file_path = askopenfilename(title=i18n.t('load-level'), initialdir="{}\\levels".format(os.getcwd()),
                                        filetypes=((i18n.t('level-files'), "*.json"), ('All files', '*.*')))
            if file_path:
                self.current_page = LevelBuilder(self, file_path, width=self.app_width, height=self.app_height)
                self.current_page.pack(fill=BOTH, expand=True)

        if self.current_page:
            answer = ConfirmDialog(title=i18n.t('confirmation'), message=i18n.t('ask-load-level'))
            if answer:
                self.current_page.destroy()
                load()
        else:
            load()


def main():
    app = LevelEditor()
    app.mainloop()


if __name__ == '__main__':
    main()
