from functools import partial

from PIL import Image
from customtkinter import CTk, CTkFrame, CTkButton, CTkLabel, CTkFont, LEFT, X, DISABLED, NORMAL, BOTH, \
    CTkScrollableFrame, CTkImage, CTkSlider, CTkCheckBox, RIGHT, IntVar, StringVar
from tkinter.messagebox import askyesno as confirmation
from game_frame import GameBoard, Levels, Settings
from level_editor import LevelEditor


class App(CTk):
    app_width = 1000
    app_height = 640
    menu_frame: CTkFrame = None
    main_menu_frame: CTkFrame = None
    current_menu: CTkFrame = None
    game = -1

    def __init__(self):
        super().__init__()
        self.button_font = CTkFont(family="Helvetica", size=14, weight="bold")
        self.initUI()
        self.levels = Levels()
        self.settings = Settings()
        self.initMainMenu()

    def initUI(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width // 2) - (self.app_width // 2)
        y = (screen_height // 2) - (self.app_height // 2)

        self.geometry(f"{self.app_width}x{self.app_height}+{x}+{y}")
        self.title("Arkanoid")
        self.resizable(False, False)

    def initMainMenu(self):
        menu_frame = self.__createMenuFrame()
        menu_label = CTkLabel(menu_frame, text="Menu", font=CTkFont(family="Helvetica", size=36, weight="bold"))
        menu_label.pack(padx=20, pady=10)

        button_width = menu_frame.winfo_reqwidth() - 40
        button_height = 40

        start_button = CTkButton(menu_frame, text="Start", width=button_width, height=button_height,
                                 font=self.button_font, command=self.startGame)
        start_button.pack(padx=20, pady=5)
        levels_button = CTkButton(menu_frame, text="Levels", width=button_width, height=button_height,
                                  font=self.button_font, command=self.openLevels)
        levels_button.pack(padx=20, pady=5)
        levels_editor = CTkButton(menu_frame, text="Levels editor", width=button_width, height=button_height,
                                  font=self.button_font, command=self.openLevelEditor)
        levels_editor.pack(padx=20, pady=5)
        settings_button = CTkButton(menu_frame, text="Settings", width=button_width, height=button_height,
                                    font=self.button_font, command=self.openSettings)
        settings_button.pack(padx=20, pady=5)
        quit_button = CTkButton(menu_frame, text="Quit", width=button_width, height=button_height,
                                font=self.button_font,
                                command=self.onExit)
        quit_button.pack(padx=20, pady=15)

        self.main_menu_frame = menu_frame
        self.menu_frame = menu_frame

    def showMenuSetting(self):
        menu_frame = self.__createMenuFrame()
        top_frame, button_back, menu_label = self.__createMenuTitle(menu_frame, "Settings")

        volume_frame = CTkFrame(menu_frame, width=self.main_menu_frame.winfo_reqwidth())
        volume_frame.pack(fill=X, padx=5, pady=5)

        image = Image.open('assets/icons/voice.png')
        icon = CTkImage(light_image=image, dark_image=image, size=(40, 40))
        image_volume = CTkLabel(volume_frame, width=40, height=40, image=icon, text="")
        image_volume.pack(side=LEFT, padx=5, pady=5)

        volume = IntVar(value=self.settings.getVolume())
        slider_volume = CTkSlider(volume_frame, from_=0, to=100, variable=volume, number_of_steps=5)
        slider_volume.pack(fill=BOTH, padx=5, pady=20)

        frame_control = CTkFrame(menu_frame, width=self.main_menu_frame.winfo_reqwidth())
        frame_control.pack(fill=X, padx=5, pady=5)

        mouse, keyboard = self.settings.getControlsType()
        mouse_control = StringVar(value=str(mouse))
        keyboard_control = StringVar(value=str(keyboard))
        check_mouse_control = CTkCheckBox(frame_control, font=self.button_font, text="Mouse control",
                                          variable=mouse_control, onvalue="True", offvalue="False")
        if not mouse_control:
            check_mouse_control.deselect()
        check_mouse_control.pack(fill=X, padx=5, pady=5)

        check_keyboard_control = CTkCheckBox(frame_control, font=self.button_font, text="Keyboard control",
                                             variable=keyboard_control, onvalue="True", offvalue="False")
        if not keyboard_control:
            check_mouse_control.deselect()
        check_keyboard_control.pack(fill=X, padx=5, pady=5)

        frame_right = CTkFrame(frame_control, fg_color='transparent')
        frame_right.pack(fill=X)

        right, left = self.settings.getKeyboardKeys()
        button_right = CTkButton(frame_right, width=40, height=40, text=right)
        button_right.configure(command=partial(self.readKey, button_right))
        button_right.pack(side=RIGHT, padx=5, pady=5)

        label_right = CTkLabel(frame_right, text="Move right", justify=LEFT, font=self.button_font)
        label_right.pack(fill=X, padx=5, pady=10)

        frame_left = CTkFrame(frame_control, fg_color='transparent')
        frame_left.pack(fill=X)

        button_left = CTkButton(frame_left, width=40, height=40, text=left)
        button_left.configure(command=partial(self.readKey, button_left))
        button_left.pack(side=RIGHT, padx=5, pady=5)

        label_left = CTkLabel(frame_left, text="Move left", justify=LEFT, font=self.button_font)
        label_left.pack(fill=X, padx=5, pady=10)

        frame_save = CTkFrame(menu_frame)
        frame_save.pack(fill=X, padx=5, pady=15)

        save_button = CTkButton(frame_save, text="Save",
                                font=self.button_font,
                                command=partial(self.onSaveSettings, slider_volume, check_mouse_control, check_keyboard_control,
                                                button_right, button_left))
        save_button.pack(fill=X, padx=5, pady=5)

        if self.menu_frame:
            self.menu_frame.destroy()
            self.menu_frame = menu_frame

    def readKey(self, button: CTkButton):
        button.configure(text="...")
        self.bind("<Key>", partial(self.updateButtonControl, button))

    def updateButtonControl(self, button, event):
        button.configure(text=event.keysym)
        self.unbind("<Key>")

    def onSaveSettings(self, volume: CTkSlider, mouse_control: CTkCheckBox, keyboard_control: CTkCheckBox, right: CTkButton, left: CTkButton):
        print(volume.get(), mouse_control.get(), keyboard_control.get(), right.cget("text"), left.cget("text"))
        self.settings.updateVolume(int(volume.get()))
        self.settings.updateMouseControl(mouse_control.get())
        self.settings.updateKeyboardControl(keyboard_control.get())
        self.settings.updateMoveRight(right.cget("text"))
        self.settings.updateMoveLeft(left.cget("text"))
        print("Save")

    def showMenuLevels(self):
        menu_frame = self.__createMenuFrame()
        top_frame, button_back, menu_label = self.__createMenuTitle(menu_frame, "Levels")

        levels_frame = CTkScrollableFrame(menu_frame, height=100)
        levels_frame.pack(fill=X, padx=5, pady=5)

        level_number = 1
        row = 0
        col = 0
        for level in self.levels.levels:
            state = NORMAL
            color = 'green'
            if level_number > self.levels.last_level + 1:
                state = DISABLED
                color = 'gray'
            if level_number == self.levels.last_level + 1:
                color = 'blue'
            button = CTkButton(levels_frame, text=f"{level_number}", fg_color=color, width=55, height=55, state=state,
                               font=self.button_font, command=partial(self.loadLevel, level_number))
            button.grid(row=row, column=col, padx=5, pady=5)
            level_number += 1
            col += 1
            if col > 2:
                col = 0
                row += 1

        if self.menu_frame:
            self.menu_frame.destroy()
            self.menu_frame = menu_frame

    def __backToMainMenu(self):
        if self.main_menu_frame:
            self.menu_frame.destroy()
            self.initMainMenu()

    def __createMenuTitle(self, root, title):
        top_frame = CTkFrame(root, width=root.winfo_reqwidth())
        top_frame.pack(fill=X, padx=5, pady=5)

        button_back = CTkButton(top_frame, text="<-", width=25, command=self.__backToMainMenu)
        button_back.pack(side=LEFT, padx=10)

        menu_label = CTkLabel(top_frame, text=title, font=CTkFont(family="Helvetica", size=36, weight="bold"))
        menu_label.pack(fill=X, padx=20, pady=10)

        return top_frame, button_back, menu_label

    def __createMenuFrame(self):
        menu_frame_width = self.app_width // 4
        menu_frame_height = self.app_height // 2
        menu_frame_x = self.app_width // 2 - menu_frame_width // 2
        menu_frame_y = self.app_height // 2 - menu_frame_height // 2
        menu_frame = CTkFrame(self, width=menu_frame_width, height=menu_frame_height)
        menu_frame.place(x=menu_frame_x, y=menu_frame_y)

        return menu_frame

    def onExit(self):
        answer = confirmation(title='Confirmation', message='Are you sure that you want to quit?')
        if answer:
            self.destroy()

    def loadLevel(self, level):
        self.game = None
        self.game = GameBoard(self, True, f'levels/level_{level}.json', width=self.app_width,
                              height=self.app_height)
        self.game.place(x=2, y=0)

    def startGame(self):
        self.game = None
        level = self.levels.last_level + 1
        if level > len(self.levels.levels):
            level = self.levels.last_level
        self.game = GameBoard(self, True, f'levels/level_{level}.json', width=self.app_width,
                              height=self.app_height)
        self.game.place(x=2, y=0)

    def openLevelEditor(self):
        LevelEditor()

    def openLevels(self):
        self.showMenuLevels()

    def openSettings(self):
        self.showMenuSetting()


def main():
    app = App()
    app.mainloop()


if __name__ == '__main__':
    main()
