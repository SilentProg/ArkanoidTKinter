from functools import partial

import i18n

import firebase
import i18n_config
from customtkinter import CTkFrame, CTkButton, CTkLabel, CTkFont, CTkEntry, LEFT, BOTH

from constants import APP_WIDTH, APP_HEIGHT
from menu_page import MenuPage


class RegisterPage(MenuPage):
    username_entry: CTkEntry = None
    email_entry: CTkEntry = None
    password_entry: CTkEntry = None
    password_confirm_entry: CTkEntry = None
    reg_frame: CTkFrame = None
    sign_in_label: CTkLabel = None
    sign_up_button: CTkButton = None
    on_login = lambda self, event: print('On sign in clicked')
    on_success = lambda self, user: print(f'Sign Up successful: {user}')

    def __init__(self, master: any, **kwargs):
        super().__init__(master, i18n.t('sign-up'), False, **kwargs)

    def _init_components(self):
        super()._init_components()
        self.username_entry = CTkEntry(master=self, width=self.elements_width, height=self.elements_height,
                                       placeholder_text=i18n.t('username'))
        self.username_entry.pack(padx=0, pady=5)

        self.email_entry = CTkEntry(master=self, width=self.elements_width, height=self.elements_height,
                                    placeholder_text=i18n.t('email'))
        self.email_entry.pack(padx=0, pady=5)

        self.password_entry = CTkEntry(master=self, width=self.elements_width, height=self.elements_height,
                                       placeholder_text=i18n.t('password'), show='*')
        self.password_entry.pack(padx=0, pady=5)

        self.password_confirm_entry = CTkEntry(master=self, width=self.elements_width, height=self.elements_height,
                                               placeholder_text=i18n.t('password-confirm'), show='*')
        self.password_confirm_entry.pack(padx=0, pady=5)

        self.reg_frame = CTkFrame(master=self)

        self.sign_in_label = CTkLabel(self.reg_frame, text=i18n.t('ask-have-account'), cursor="hand2",
                                      font=CTkFont(family="Helvetica", size=14, underline=True))
        self.sign_in_label.pack(pady=5, padx=5, side=LEFT)
        self.sign_in_label.bind("<Button-1>", partial(self.on_login))

        self.reg_frame.pack(fill=BOTH, expand=1, padx=20, pady=5)

        self.sign_up_button = CTkButton(self, text=i18n.t('sign-up-process'), cursor="hand2", width=self.elements_width,
                                        height=self.elements_height,
                                        command=self.sign_up,
                                        font=CTkFont(family="Helvetica", size=14, weight="bold"))
        self.sign_up_button.pack(padx=20, pady=10)

    # Метод реєстрації
    def sign_up(self):
        self.error_frame.pack_forget()  # прибираємо помилку
        username = self.username_entry.get()  # отримуємо nickname
        email = self.email_entry.get()  # отримуємо email
        password = self.password_entry.get()  # отримуємо пароль
        password_confirm = self.password_confirm_entry.get()  # отримуємо пароль підтвердження
        # перевіряємо дані
        if username == '' or email == '' or password == '' or password_confirm == '':
            self.show_error(i18n.t('MISSING_DATA'))
            return
        if password != password_confirm:
            self.show_error(i18n.t('PASSWORD_MISMATCH'))
            return
        # Реєструємо користувача
        firebase.sign_up(email, password, username,
                         onerror=lambda e: self.show_error(e),
                         onsuccess=self.on_success)

    def set_on_login(self, on_login):
        self.on_login = on_login
        self.sign_in_label.bind("<Button-1>", lambda s: self.on_login())

    def set_on_success(self, on_success):
        self.on_success = on_success
