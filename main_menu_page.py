import i18n
from customtkinter import CTkButton
from menu_page import MenuPage


class MainMenuPage(MenuPage):
    def __init__(self, master: any, **kwargs):
        self.buttons: {} = {}
        self.buttons_elements: [] = []
        super().__init__(master, i18n.t('menu'), False, **kwargs)

    def _init_components(self):
        super()._init_components()

    def init_buttons(self):
        for key, value in self.buttons.items():
            button = CTkButton(self, text=key, width=self.elements_width, height=self.elements_height,
                               font=self.button_font, command=value)
            button.pack(padx=20, pady=5 if key != i18n.t('quit') else 15)
            self.buttons_elements.append(button)

    def add_button(self, title, callback):
        self.buttons[title] = callback

    def clear(self):
        self.buttons.clear()
        for button in self.buttons_elements:
            button.destroy()
        self.buttons_elements.clear()
