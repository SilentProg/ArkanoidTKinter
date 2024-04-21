from functools import partial

import i18n

import firebase
import i18n_config
from customtkinter import BOTH, CTkToplevel, CTkLabel, CTkButton, CTkTabview, LEFT, Y, RIGHT, CTkImage
from tkinter import Menu
from tkinter.filedialog import askopenfilename
from constants import isAuth, isAdmin, centered_window
from custom_components import ListView, LevelItem
from custom_dialogs import InfoDialog, ConfirmDialog
from level_builder import LevelBuilder
from PIL import Image


class LevelEditor(CTkToplevel):
    def __init__(self):
        super().__init__()

        if not isAuth():
            InfoDialog({
                'title': i18n.t('auth-error'),
                'message': i18n.t('permission-denied')
            }).show()
            self.destroy()

        self.image_public = Image.open(f'assets/icons/public.png')
        self.icon_public = CTkImage(light_image=self.image_public, dark_image=self.image_public, size=(25, 25))
        self.image_private = Image.open(f'assets/icons/private.png')
        self.icon_private = CTkImage(light_image=self.image_private, dark_image=self.image_private, size=(25, 25))

        self.current_page = None
        self.app_width = 1200
        self.app_height = 660
        self.grab_set()
        centered_window(self, self.app_width, self.app_height, i18n.t('level-editor-title'), False)
        self.initMainMenu()
        self._init_levels_chooser()

    def _init_levels_chooser(self):
        self.tab_view = CTkTabview(self)
        if isAdmin():
            self.levels_tab = self.tab_view.add(i18n.t('levels'))
            self.community_tab = self.tab_view.add(i18n.t('community-levels'))
            self._init_levels(self.levels_tab)
            self._init_community_levels(self.community_tab)

        if isAuth() and not isAdmin():
            self.my_levels_tab = self.tab_view.add(i18n.t('my-levels'))
            self._init_my_levels(self.my_levels_tab)

        self._show_level_chooser()

    def _show_level_chooser(self):
        self.tab_view.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)

    def _init_community_levels(self, tab):
        self.community_levels_list = ListView(tab)
        self.community_levels_list.pack(expand=True, fill="both")

        community_levels = firebase.db.child('community-levels').get()
        if community_levels.val():
            self._convert_levels(community_levels, self.community_levels_list)

    def _init_my_levels(self, tab):
        self.my_levels_list = ListView(tab)
        self.my_levels_list.pack(expand=True, fill="both")
        my_levels = firebase.db.child('community-levels').order_by_child('creatorLocalId').equal_to(
            firebase.auth.current_user['localId']).get()
        if my_levels.val():
            self._convert_levels(my_levels, self.my_levels_list, True)

    def _init_levels(self, tab):
        self.levels_list = ListView(tab)
        self.levels_list.pack(expand=True, fill="both")

        levels = firebase.db.child('levels').get()
        if levels.val():
            self._convert_levels(levels, self.levels_list)

    def _convert_levels(self, levels, levels_list, additional_btn=False):
        for level in levels:
            val = level.val()
            val['key'] = level.key()
            val['parent'] = levels.key()
            if 'walls' not in val['level']:
                val['level']['walls'] = {}
            level_item = LevelItem(levels_list, val)
            level_item.set_on_delete(self.deleteLevel)
            level_item.set_on_load(self._load_level)
            if additional_btn:
                btn = CTkButton(level_item,
                                text=i18n.t('public') if val['public'] else i18n.t('private'),
                                fg_color=i18n.t('public_color') if val['public'] else i18n.t('private_color'),
                                image=self.icon_public if val['public'] else self.icon_private,
                                )
                btn.pack(side=RIGHT, padx=5, pady=5)
                btn.configure(command=partial(self._toggle_visibility, btn, val))

            levels_list.add_item(level_item)

    def _toggle_visibility(self, btn: CTkButton, level: {}):
        if not ConfirmDialog({'title': i18n.t('confirmation'), 'message': i18n.t('ask-toggle-visibility'),
                              'ok_text': i18n.t('yes')}).show():
            return

        firebase.db.child(level['parent']).child(level['key']).update({'public': not level['public']})
        btn.configure(text=i18n.t('public') if not level['public'] else i18n.t('private'),
                      fg_color=i18n.t('public_color') if not level['public'] else i18n.t('private_color'),
                      image=self.icon_public if not level['public'] else self.icon_private,
                      )

    def initMainMenu(self):
        menubar = Menu(self)
        self.config(menu=menubar)

        fileMenu = Menu(menubar, tearoff=0)
        levelMenu = Menu(menubar, tearoff=0)

        levelMenu.add_command(label=i18n.t('new-level'), command=self.newLevel)
        levelMenu.add_command(label=i18n.t('load-level'), command=self.openChooser)

        fileMenu.add_cascade(label=i18n.t('level'), menu=levelMenu)
        fileMenu.add_command(label=i18n.t('quit'), command=self.onExit)
        menubar.add_cascade(label=i18n.t('menu-file'), menu=fileMenu)

    def onExit(self):
        if ConfirmDialog(
                {'title': i18n.t('confirmation'), 'message': i18n.t('ask-quit'), 'ok_text': i18n.t('yes')}).show():
            self.destroy()

    # Метод створення нового рівня
    def newLevel(self):
        def create():  # підметод для створення рівня
            self.tab_view.destroy()  # прибираємо меню вибору рівня
            self.current_page = LevelBuilder(self, width=self.app_width, height=self.app_height)  # створюємо вікно редактора
            self.current_page.pack(fill=BOTH, expand=True)  # відображаємо вікно редактора

        #  перевіряємо чи є відкритий рівень
        if self.current_page: #  якщо є то запитуємо чи дійсно створити новий рівень
            answer = ConfirmDialog(
                {'title': i18n.t('confirmation'), 'message': i18n.t('ask-new-level'), 'ok_text': i18n.t('yes')}).show()
            if answer:
                #  яккщо користувач погодився створюємо рівень
                self.current_page.destroy()
                create()
        else:
            #  створюємо пустий рівень
            create()

    def deleteLevel(self, level):
        answer = ConfirmDialog(
            {'title': i18n.t('confirmation'), 'message': i18n.t('ask-delete-level'), 'ok_text': i18n.t('yes')}).show()
        if answer:
            firebase.db.child(level['parent']).child(level['key']).remove(token=firebase.auth.current_user['idToken'])

        return answer

    def openChooser(self):
        if not self.current_page:
            return 
        if self.current_page and not ConfirmDialog(
                {'title': i18n.t('confirmation'), 'message': i18n.t('ask-load-level'),
                 'ok_text': i18n.t('yes')}).show():
            return
        if self.current_page:
            self.current_page.destroy()
        self._init_levels_chooser()
        self._show_level_chooser()

    def _load_level_locale(self):
        import os

        def load():
            file_path = askopenfilename(title=i18n.t('load-level'), initialdir="{}\\levels".format(os.getcwd()),
                                        filetypes=((i18n.t('level-files'), "*.json"), ('All files', '*.*')))
            if file_path:
                self.current_page = LevelBuilder(self, file_path, width=self.app_width, height=self.app_height)
                self.current_page.pack(fill=BOTH, expand=True)

        if self.current_page:
            answer = ConfirmDialog(
                {'title': i18n.t('confirmation'), 'message': i18n.t('ask-load-level'), 'ok_text': i18n.t('yes')}).show()
            if answer:
                self.current_page.destroy()
                load()
        else:
            load()

    def _load_level(self, level):
        if self.current_page:
            self.current_page.destroy()
        if self.tab_view:
            self.tab_view.destroy()
        self.current_page = LevelBuilder(self, level, width=self.app_width, height=self.app_height)
        self.current_page.pack(fill=BOTH, expand=True)


def main():
    app = LevelEditor()
    app.mainloop()


if __name__ == '__main__':
    main()
