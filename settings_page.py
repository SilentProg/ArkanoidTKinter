from functools import partial

import i18n
import pygame
from customtkinter import CTkButton, CTkFrame, CTkLabel, CTkSlider, CTkCheckBox, X, LEFT, BOTH, CTkImage, IntVar, \
    StringVar, CTkFont, RIGHT, CTkComboBox, CTkOptionMenu

import i18n_config
from game_frame import Settings
from menu_page import MenuPage
from PIL import Image


class Language:
    def __init__(self, code, title):
        self.code = code
        self.title = title

    def __str__(self):
        return self.title


class SettingsPage(MenuPage):
    volume_frame: CTkFrame = None
    icon: CTkImage = None
    image_volume: CTkLabel = None
    volume: IntVar = None
    slider_volume: CTkSlider = None
    frame_control: CTkFrame = None
    mouse_control: StringVar = None
    keyboard_control: StringVar = None
    check_mouse_control: CTkCheckBox = None

    def __init__(self, master: any, **kwargs):
        self.settings = Settings()
        self.button_font = CTkFont(family="Helvetica", size=14, weight="bold")
        super().__init__(master, i18n.t('settings'), True, **kwargs)

    def _init_components(self):
        super()._init_components()
        self.volume_frame = CTkFrame(self, width=self.winfo_reqwidth())
        self.volume_frame.pack(fill=X, padx=5, pady=5)

        image = Image.open('assets/icons/voice.png')
        self.icon = CTkImage(light_image=image, dark_image=image, size=(40, 40))
        self.image_volume = CTkLabel(self.volume_frame, width=40, height=40, image=self.icon, text="")
        self.image_volume.pack(side=LEFT, padx=5, pady=5)

        self.volume = IntVar(value=self.settings.getVolume())
        self.slider_volume = CTkSlider(self.volume_frame, from_=0, to=100, variable=self.volume, number_of_steps=5)
        self.slider_volume.pack(fill=BOTH, padx=5, pady=20)

        self.frame_control = CTkFrame(self, width=self.winfo_reqwidth())
        self.frame_control.pack(fill=X, padx=5, pady=5)

        mouse, keyboard = self.settings.getControlsType()
        effects, background = self.settings.getSounds()
        self.mouse_control = StringVar(value=str(mouse))
        self.keyboard_control = StringVar(value=str(keyboard))
        self.effects_enabled = StringVar(value=str(effects))
        self.background_enabled = StringVar(value=str(background))

        self.check_effects = CTkCheckBox(self.frame_control, font=self.button_font,
                                         text=i18n.t("effects"),
                                         variable=self.effects_enabled, onvalue="True", offvalue="False")
        self.check_effects.pack(fill=X, padx=5, pady=5)
        self.check_background = CTkCheckBox(self.frame_control, font=self.button_font,
                                            text=i18n.t("background"),
                                            variable=self.background_enabled, onvalue="True", offvalue="False")
        self.check_background.pack(fill=X, padx=5, pady=5)

        self.check_mouse_control = CTkCheckBox(self.frame_control, font=self.button_font, text=i18n.t("mouse-control"),
                                               variable=self.mouse_control, onvalue="True", offvalue="False")
        if not self.mouse_control:
            self.check_mouse_control.deselect()
        self.check_mouse_control.pack(fill=X, padx=5, pady=5)

        self.check_keyboard_control = CTkCheckBox(self.frame_control, font=self.button_font,
                                                  text=i18n.t("keyboard-control"),
                                                  variable=self.keyboard_control, onvalue="True", offvalue="False")
        if not self.keyboard_control:
            self.check_mouse_control.deselect()
        self.check_keyboard_control.pack(fill=X, padx=5, pady=5)

        frame_right = CTkFrame(self.frame_control, fg_color='transparent')
        frame_right.pack(fill=X)

        right, left = self.settings.getKeyboardKeys()
        button_right = CTkButton(frame_right, width=50, height=40, text=right)
        button_right.configure(command=partial(self.readKey, button_right))
        button_right.pack(side=RIGHT, padx=5, pady=5)

        label_right = CTkLabel(frame_right, text=i18n.t('move-right'), justify='left', font=self.button_font)
        label_right.pack(side=LEFT, fill=X, padx=5, pady=10)

        frame_left = CTkFrame(self.frame_control, fg_color='transparent')
        frame_left.pack(fill=X)

        button_left = CTkButton(frame_left, width=50, height=40, text=left)
        button_left.configure(command=partial(self.readKey, button_left))
        button_left.pack(side=RIGHT, padx=5, pady=5)

        label_left = CTkLabel(frame_left, text=i18n.t('move-left'), font=self.button_font)
        label_left.pack(side=LEFT, fill=X, padx=5, pady=10)

        label_language = CTkLabel(self.frame_control, text=i18n.t('language'), font=self.button_font)
        label_language.pack(side=LEFT, fill=X, padx=5, pady=10)
        languages = self.settings.getAllLanguages()

        combobox = CTkOptionMenu(self.frame_control, values=list(languages.values()))
        combobox.set(self.settings.getLanguage()['name']),
        combobox.pack(side=RIGHT, fill=X, expand=True, padx=5, pady=10)

        frame_save = CTkFrame(self)
        frame_save.pack(fill=X, padx=5, pady=5)

        save_button = CTkButton(frame_save, text=i18n.t('save'),
                                font=self.button_font,
                                height=self.elements_height,
                                command=partial(self.onSaveSettings, self.slider_volume, self.check_mouse_control,
                                                self.check_keyboard_control,
                                                button_right, button_left, combobox))
        save_button.pack(fill=X, padx=5, pady=5)

    def readKey(self, button: CTkButton):
        button.configure(text="...")
        self.master.bind("<Key>", partial(self.updateButtonControl, button))

    def updateButtonControl(self, button, event):
        button.configure(text=event.keysym)
        self.master.unbind("<Key>")

    def onSaveSettings(self, volume: CTkSlider, mouse_control: CTkCheckBox, keyboard_control: CTkCheckBox,
                       right: CTkButton, left: CTkButton, language: CTkOptionMenu):
        print(volume.get(), mouse_control.get(), keyboard_control.get(), right.cget("text"), left.cget("text"))
        self.settings.updateVolume(int(volume.get()))
        self.settings.updateMouseControl(mouse_control.get())
        self.settings.updateKeyboardControl(keyboard_control.get())
        self.settings.updateMoveRight(right.cget("text"))
        self.settings.updateMoveLeft(left.cget("text"))
        self.settings.updateLanguage(language.get())
        self.settings.updateSoundsEffects(self.effects_enabled.get())
        old_back = self.settings.getBackgroundEnabled()
        self.settings.updateSoundsBackground(self.background_enabled.get())
        self.show_result(i18n.t('saved'))
        pygame.mixer.music.set_volume(volume.get()/500)
        if self.background_enabled.get() == 'False':
            pygame.mixer.music.stop()
        elif not old_back:
            pygame.mixer.music.play(loops=-1)
        print("Save")
