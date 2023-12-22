from customtkinter import BOTH, CTkToplevel, CTkLabel, CTkButton
from tkinter import Menu
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import askyesno as ConfirmDialog

from level_builder import LevelBuilder


class LevelEditor(CTkToplevel):
    def __init__(self):
        super().__init__()
        self.current_page = None
        self.app_width = 1210
        self.app_height = 650
        self.initUI()
        self.initMainMenu()

    def initUI(self):
        self.grab_set()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width // 2) - (self.app_width // 2)
        y = (screen_height // 2) - (self.app_height // 2)

        self.geometry(f"{self.app_width}x{self.app_height}+{x}+{y}")
        self.title("Arkanoid | Level builder")
        self.resizable(False, False)

    def initMainMenu(self):
        menubar = Menu(self)
        self.config(menu=menubar)

        fileMenu = Menu(menubar, tearoff=0)
        levelMenu = Menu(menubar, tearoff=0)

        levelMenu.add_command(label="Новий рівень", command=self.newLevel)
        levelMenu.add_command(label="Завантажити рівень", command=self.loadLevel)

        fileMenu.add_cascade(label="Рівень", menu=levelMenu)
        fileMenu.add_command(label="Вихід", command=self.onExit)
        menubar.add_cascade(label="Файл", menu=fileMenu)

    def onExit(self):
        answer = ConfirmDialog(title='Confirmation', message='Are you sure that you want to quit?')
        if answer:
            self.destroy()

    def newLevel(self):
        def create():
            self.current_page = LevelBuilder(self, width=self.app_width, height=self.app_height)
            self.current_page.pack(fill=BOTH, expand=True)

        if self.current_page:
            answer = ConfirmDialog(title='Confirmation', message='Are you sure that you want to create new level?')
            if answer:
                self.current_page.destroy()
                create()
        else:
            create()

    def loadLevel(self):
        import os

        def load():
            file_path = askopenfilename(title="Load level", initialdir="{}\\levels".format(os.getcwd()),
                                        filetypes=(("Level files", "*.json"), ('All files', '*.*')))
            if file_path:
                self.current_page = LevelBuilder(self, file_path, width=self.app_width, height=self.app_height)
                self.current_page.pack(fill=BOTH, expand=True)

        if self.current_page:
            answer = ConfirmDialog(title='Confirmation', message='Are you sure that you want to load level?')
            if answer:
                self.current_page.destroy()
                load()
        else:
            load()


def main():
    app = LevelEditor()
    app.mainloop()


if __name__ == '__main__':
    main()
