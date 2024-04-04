import time
from tkinter import filedialog, Label
from customtkinter import CTkFrame, CTkLabel, CTkImage, LEFT, CTkFont, CTkButton
from PIL import Image, ImageTk
import requests
import firebase
import io


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
        avatar = firebase.db.child(self.user['localId']).child('avatar').child('url').get().val()
        if avatar is None:
            image = Image.open('assets/icons/avatar.png')
            icon = CTkImage(light_image=image, dark_image=image, size=(40, 40))
        else:
            icon = self.load_image(avatar)

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
            avatar = firebase.db.child(self.user['localId']).child('avatar').child('path').get().val()
            if avatar:
                firebase.storage.delete('avatars/' + str(avatar), token=self.user['idToken'])

            storage_name = self.user['localId'] + "-" + str(time.time()) + "." + file_path.split(".")[-1]
            firebase.storage.child('avatars').child(storage_name).put(file_path, self.user['idToken'])
            url = firebase.storage.child('avatars').child(storage_name).get_url(self.user['idToken'])
            firebase.db.child(self.user['localId']).child('avatar').set({'url': url, 'path': storage_name})
            self.avatar.configure(image=self.load_image(url + "&auth=" + self.user['localId']))

    def load_image(self, url):
        icon = WebImage(url, self.user['idToken']).get()
        icon = CTkImage(light_image=icon, dark_image=icon, size=(40, 40))
        return icon

    def show(self):
        self.place(x=10, y=10)


class WebImage:
    def __init__(self, url, token):
        headers = {"Authorization": "Firebase " + token}
        with requests.get(url, headers=headers) as u:
            raw_data = u.content
        self.image = Image.open(io.BytesIO(raw_data))

    def get(self):
        return self.image
