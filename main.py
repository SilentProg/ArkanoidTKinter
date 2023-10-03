from customtkinter import CTk, CTkFrame, CTkButton, CTkLabel, CTkFont
from tkinter.messagebox import askyesno as ConfirmDialog
from game_engine.game_frame import GameBoard


class App(CTk):
    app_width = 1080
    app_height = 720
    menu_frame = -1
    game = -1

    def __init__(self):
        super().__init__()
        self.initUI()
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
        menu_frame_width = self.app_width // 4
        menu_frame_height = self.app_height // 2
        menu_frame_x = self.app_width // 2 - menu_frame_width // 2
        menu_frame_y = self.app_height // 2 - menu_frame_height // 2
        self.menu_frame = CTkFrame(self, width=menu_frame_width, height=menu_frame_height)

        self.menu_frame.place(x=menu_frame_x, y=menu_frame_y)

        menu_label = CTkLabel(self.menu_frame, text="Menu", font=CTkFont(family="Helvetica", size=36, weight="bold"))
        menu_label.pack(padx=20, pady=10)

        button_width = menu_frame_width - 40
        button_height = 40
        button_font = CTkFont(family="Helvetica", size=14, weight="bold")

        start_button = CTkButton(self.menu_frame, text="Start", width=button_width, height=button_height, font=button_font, command=self.startGame)
        start_button.pack(padx=20, pady=5)
        levels_button = CTkButton(self.menu_frame, text="Levels", width=button_width, height=button_height, font=button_font)
        levels_button.pack(padx=20, pady=5)
        levels_editor = CTkButton(self.menu_frame, text="Levels editor", width=button_width, height=button_height,
                                  font=button_font)
        levels_editor.pack(padx=20, pady=5)
        settings_button = CTkButton(self.menu_frame, text="Settings", width=button_width, height=button_height,
                                    font=button_font)
        settings_button.pack(padx=20, pady=5)
        quit_button = CTkButton(self.menu_frame, text="Quit", width=button_width, height=button_height, font=button_font,
                                command=self.onExit)
        quit_button.pack(padx=20, pady=15)

    def onExit(self):
        answer = ConfirmDialog(title='Confirmation', message='Are you sure that you want to quit?')
        if answer:
            self.destroy()

    def startGame(self):
        if self.game == -1:
            self.game = GameBoard(self, True, 'levels/level_1.json', width=self.app_width, height=self.app_height)
            self.game.place(x=2, y=0)
            # self.menu_frame.destroy()


def main():
    app = App()
    app.mainloop()


if __name__ == '__main__':
    main()
