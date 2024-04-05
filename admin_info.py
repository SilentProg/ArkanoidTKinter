from customtkinter import CTkFrame, CTkImage, CTkLabel, LEFT, CTkFont
from PIL import Image
import i18n
import i18n_config


class AdminInfo(CTkFrame):
    def __init__(self, master: any, **kwargs):
        super().__init__(master, **kwargs)
        self.font = CTkFont(family="Helvetica", size=25, weight="bold")
        image = Image.open('assets/icons/warning.png')
        icon = CTkImage(light_image=image, dark_image=image, size=(40, 40))
        self.warning_icon = CTkLabel(self, width=40, height=40, image=icon, text="")
        self.warning_icon.pack(side=LEFT, padx=10, pady=10)

        self.info_label = CTkLabel(self, text=i18n.t('admin-status'), text_color="#fce0a2", font=self.font)
        self.info_label.pack(side=LEFT, padx=10, pady=10)

    def show(self):
        self.grid(row=0, column=1)
