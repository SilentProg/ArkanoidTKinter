from tkinter import StringVar

import i18n
from customtkinter import CTkFrame, CTkLabel, CTkFont, CTkEntry, CTkButton, LEFT, BOTH, CTkCheckBox

import firebase
from functools import partial

import i18n_config
from menu_page import MenuPage
from session import Session


class LoginPage(MenuPage):
    email_entry: CTkEntry = None
    password_entry: CTkEntry = None
    reg_frame: CTkFrame = None
    sign_up_label: CTkLabel = None
    forget_label: CTkLabel = None
    sign_in_button: CTkButton = None
    remember_me_checkbox: CTkCheckBox = None
    remember_me_var: StringVar = None
    session: Session = None
    on_register = lambda self, event: print('On register click')
    on_success = lambda self, user: print(f'Auth successful: {user}')

    def __init__(self, master: any, **kwargs):
        super().__init__(master, i18n.t('sign-in'), False, **kwargs)
        self.session = Session()

    def _init_components(self):
        super()._init_components()

        self.email_entry = CTkEntry(master=self, width=self.elements_width, height=self.elements_height,
                                    placeholder_text=i18n.t('email'))
        self.email_entry.pack(padx=0, pady=5)

        self.password_entry = CTkEntry(master=self, width=self.elements_width, height=self.elements_height,
                                       placeholder_text=i18n.t('password'), show='*')
        self.password_entry.pack(padx=0, pady=5)

        self.remember_me_var = StringVar(value='False')
        self.remember_me_checkbox = CTkCheckBox(self, font=CTkFont(family="Helvetica", size=14),
                                                text=i18n.t("remember-me"),
                                                width=self.elements_width, height=self.elements_height,
                                                variable=self.remember_me_var, onvalue="True", offvalue="False")

        self.remember_me_checkbox.pack(padx=0, pady=5)

        self.reg_frame = CTkFrame(master=self)

        self.sign_up_label = CTkLabel(self.reg_frame, text=i18n.t('sign-up'), cursor="hand2",
                                      font=CTkFont(family="Helvetica", size=14, underline=True))
        self.sign_up_label.pack(pady=5, padx=5, side=LEFT)
        self.sign_up_label.bind("<Button-1>", self.on_register)

        self.forget_label = CTkLabel(self.reg_frame, text=i18n.t('forget-password'), cursor="hand2",
                                     font=CTkFont(family="Helvetica", size=14, underline=True))
        self.forget_label.pack(pady=5, padx=5, side=LEFT)
        self.forget_label.bind("<Button-1>", partial(self.restore_password))

        self.reg_frame.pack(fill=BOTH, expand=1, padx=20, pady=5)

        self.sign_in_button = CTkButton(self, text=i18n.t('sign-in-process'), cursor="hand2",
                                        width=self.elements_width, height=self.elements_height,
                                        font=CTkFont(family="Helvetica", size=14, weight="bold"),
                                        command=self.sign_in)
        self.sign_in_button.pack(padx=20, pady=10)

    def set_on_success(self, onsuccess):
        self.on_success = onsuccess

    def set_on_register(self, on_register):
        self.on_register = on_register
        self.sign_up_label.bind("<Button-1>", lambda s: self.on_register())

    def restore_password(self, event):
        firebase.restore_password(self.email_entry.get(),
                                  onerror=lambda e: self.show_error(e),
                                  onsuccess=lambda r: self.show_result(i18n.t('EMAIL_SEND')))

    def sign_in(self):
        self.error_frame.pack_forget()
        firebase.sign_in(self.email_entry.get(), self.password_entry.get(),
                         onerror=lambda e: self.show_error(e),
                         onsuccess=self.on_auth_success)

    def on_auth_success(self, user):
        if self.remember_me_var.get() == 'True':
            self.session.write_credentials({
                'email': self.email_entry.get().encode(),
                'password': self.password_entry.get().encode()
            })
        self.on_success(user)

    def check_session(self):
        if not self.session.has():
            return False
        credentials = self.session.read_credentials()
        self.email_entry.insert(0, credentials['email'])
        self.password_entry.insert(0, credentials['password'])
        self.sign_in()
        return True
