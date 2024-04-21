import i18n
import pygame

import i18n_config
from customtkinter import CTk, CTkFrame, END
from tkinter.messagebox import askyesno as confirmation

from account_info import AccountInfo
from admin_info import AdminInfo
from community_levels_page import CommunityLevelsPage
from custom_dialogs import ConfirmDialog
from levels_page import LevelsPage, CampaignLevels
from game_frame import GameBoard, Settings
from level_editor import LevelEditor
import firebase
from login_page import LoginPage
from constants import APP_WIDTH, APP_HEIGHT, isAdmin
from menu_page import MenuPage
from register_page import RegisterPage
from session import Session
from settings_page import SettingsPage
from main_menu_page import MainMenuPage


class App(CTk):
    app_width = APP_WIDTH
    app_height = APP_HEIGHT
    menu_frame: MenuPage = None
    main_menu_frame: CTkFrame = None
    current_menu: CTkFrame = None
    game: GameBoard = None
    login_page: LoginPage = None
    register_page: RegisterPage = None
    account_info: AccountInfo = None
    community_levels_page: CommunityLevelsPage = None
    levels_page: LevelsPage = None
    admin_info: AdminInfo = None
    user = None

    def __init__(self):
        super().__init__()
        self.initUI()
        self.settings = Settings()
        pygame.mixer.init()
        pygame.mixer.music.load("assets/sounds/loop.mp3")
        pygame.mixer.music.set_volume(self.settings.getVolume()/500)
        if self.settings.getBackgroundEnabled():
            self.after(200, lambda: pygame.mixer.music.play(loops=-1))

        self.background_music = pygame.mixer.Sound("assets/sounds/loop.mp3")
        self.login_page = LoginPage(self)
        self.register_page = RegisterPage(self)
        self.settings_page = SettingsPage(self)

        self.login_page.set_on_register(lambda: self.__show_page(self.register_page))
        self.login_page.set_on_success(self.authUser)
        self.register_page.set_on_success(self.regUser)
        self.register_page.set_on_login(lambda: self.__show_page(self.login_page))

        self.settings_page.set_on_back(self.on_settings_back)
        self.mainMenuPage = MainMenuPage(self)

        if not self.login_page.check_session():
            self.__show_page(self.login_page)

        # print(f"User: {self.user}")

    def on_settings_back(self):
        self.backToMainMenu()
        self.settings_page.error_frame.pack_forget()

    def initUI(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width // 2) - (self.app_width // 2)
        y = (screen_height // 2) - (self.app_height // 2)

        self.geometry(f"{self.app_width}x{self.app_height}+{x}+{y}")
        self.title(i18n.t('game-title'))
        self.resizable(False, False)

    def authUser(self, user):
        self.user = user

        self.mainMenuPage.add_button(i18n.t('play'), self.startGame)
        self.mainMenuPage.add_button(i18n.t('levels'), self._show_levels)
        self.mainMenuPage.add_button(i18n.t('community-levels'), self._show_community_levels)
        self.mainMenuPage.add_button(i18n.t('level-editor'), lambda: LevelEditor())
        self.mainMenuPage.add_button(i18n.t('settings'), lambda: self.__show_page(self.settings_page))

        if isAdmin():
            self.admin_info = AdminInfo(self)
            self.admin_info.show()

        self.mainMenuPage.add_button(i18n.t('quit'), self.onExit)
        self.mainMenuPage.init_buttons()

        self.account_info = AccountInfo(self, user)
        self.account_info.set_on_logout(self.logout)
        self.account_info.show()
        self.__show_page(self.mainMenuPage)

    def _show_levels(self):
        if self.levels_page:
            self.levels_page.destroy()
        self.levels_page = LevelsPage(self)
        self.levels_page.set_on_back(self.backToMainMenu)
        self.__show_page(self.levels_page)

    def _show_community_levels(self):
        if self.community_levels_page:
            self.community_levels_page.destroy()
        self.community_levels_page = CommunityLevelsPage(self)
        self.community_levels_page.set_on_back(self.backToMainMenu)
        self.__show_page(self.community_levels_page)

    def logout(self):
        session = Session()
        session.delete_credentials()
        self.login_page.email_entry.delete(0, END)
        self.login_page.password_entry.delete(0, END)

        if self.mainMenuPage:
            self.mainMenuPage.clear()

        if self.account_info:
            self.account_info.destroy()

        if self.admin_info:
            self.admin_info.destroy()

        self.__show_page(self.login_page)

    def regUser(self, user):
        self.user = user
        self.__show_page(self.login_page)

    def __show_page(self, page):
        if self.menu_frame:
            self.menu_frame.place_forget()

        self.menu_frame = page
        self.menu_frame.show()

    def backToMainMenu(self):
        self.__show_page(self.mainMenuPage)

    def onExit(self):
        if ConfirmDialog({'title': i18n.t('confirmation'), 'message': i18n.t('ask-quit'), 'ok_text': i18n.t('yes')}).show():
            self.destroy()

    def startGame(self):
        self._show_levels()
        self.levels_page.play(self.levels_page.levels.get_next_level())
        # if self.game:
        #     self.game.destroy()
        #
        # level = self.levels_page.levels.last_level + 1
        # if level > len(self.levels_page.levels.levels):
        #     level = self.levels_page.levels.last_level
        # self.game = GameBoard(self, True, f'levels/level_{level}.json', width=self.app_width,
        #                       height=self.app_height)
        # self.game.place(x=2, y=0)


def main():
    app = App()
    app.mainloop()


if __name__ == '__main__':
    main()
