import time
from io import BytesIO
from tkinter import filedialog

import requests
from customtkinter import CTkFrame, CTkLabel, CTkImage, LEFT, CTkFont, CTkButton
from PIL import Image

import firebase


class AccountInfo(CTkFrame):
    avatar: CTkLabel = None

    def __init__(self, master: any, user, **kwargs):
        super().__init__(master, **kwargs)
        self.font = CTkFont(family="Helvetica", size=25, weight="bold")
        self.user = user
        self.user_info = firebase.auth.get_account_info(self.user['idToken'])
        print(self.user)
        print(self.user_info)
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
            storage_name = self.user['localId'] + "-" + str(time.time()) + "." + file_path.split(".")[-1]
            firebase.storage.child('avatars').child(storage_name).put(file_path, self.user['idToken'])
            url = firebase.storage.child('avatars').child(storage_name).get_url(self.user['idToken'])
            firebase.auth.update_profile(self.user['idToken'], photo_url=url)

            self.load_image(url)

    def load_image(self, url):
        response = requests.get(url)
        image_data = response.content
        image = Image.open(BytesIO(image_data))
        photo = CTkImage(light_image=image, dark_image=image, size=(35, 35))
        self.avatar.config(image=photo)

    def show(self):
        self.place(x=10, y=10)