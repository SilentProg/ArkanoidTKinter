import time
from tkinter import filedialog

from customtkinter import CTkFrame, CTkLabel, CTkImage, LEFT, CTkFont, CTkButton
from PIL import Image

import firebase


class AccountInfo(CTkFrame):
    avatar: CTkLabel = None

    def __init__(self, master: any, user, **kwargs):
        super().__init__(master, **kwargs)
        self.font = CTkFont(family="Helvetica", size=25, weight="bold")
        self.user = user
        self._init_components()

    def _init_components(self):
        image = Image.open('assets/icons/avatar.png')
        icon = CTkImage(light_image=image, dark_image=image, size=(40, 40))
        self.avatar = CTkLabel(self, width=40, height=40, image=icon, text="", cursor="hand2")
        self.avatar.pack(side=LEFT, padx=10, pady=10)
        self.avatar.bind("<Button-1>", self.on_change_avatar)

        self.display_name_label = CTkLabel(self, text=self.user['displayName'], font=self.font)
        self.display_name_label.pack(side=LEFT, padx=10, pady=10)

        image = Image.open('assets/icons/logout.png')
        icon = CTkImage(light_image=image, dark_image=image, size=(35, 35))
        self.log_out_button = CTkButton(self, font=self.font, text="", image=icon, width=40, height=40)
        self.log_out_button.pack(side=LEFT, padx=10, pady=10)

    def set_on_logout(self, on_logout):
        self.log_out_button.configure(command=on_logout)

    def on_change_avatar(self, event):
        print('click')
        file_path = filedialog.askopenfilename(
            filetypes=[("Картинки", "*.png;*.jpg;*.jpeg")]
        )

        if file_path:
            print(self.user)
            storage_name = self.user['localId'] + "-" + str(time.time())
            firebase.storage.child('avatars').child().put()
            print("Selected file:", file_path)
        else:
            print("File selection canceled.")

    def show(self):
        self.place(x=10, y=10)
