from customtkinter import CTk, CTkFrame, CTkButton, CTkLabel, BOTH
from tkinter import Menu, Canvas
from level_builder import LevelBuilder


class App(CTk):
    def __init__(self):
        super().__init__()
        self.current_page = None
        self.app_width = 1265
        self.app_height = 650
        self.initUI()
        self.initMainMenu()
        self.newLevel()

    def initUI(self):
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
        controlMenu = Menu(menubar, tearoff=0)

        levelMenu.add_command(label="Новий рівень", command=self.newLevel)
        levelMenu.add_command(label="Завантажити рівень", command=self.onExit)

        controlMenu.add_command(label="Блок")
        controlMenu.add_command(label="Каретка")
        controlMenu.add_command(label="Фон")

        fileMenu.add_cascade(label="Рівень", menu=levelMenu)
        fileMenu.add_cascade(label="Елементи керування", menu=controlMenu)
        fileMenu.add_command(label="Вихід", command=self.onExit)
        menubar.add_cascade(label="Файл", menu=fileMenu)

    def onExit(self):
        self.quit()

    def newLevel(self):
        self.current_page = LevelBuilder(self, width=self.app_width, height=self.app_height)
        self.current_page.pack(fill=BOTH, expand=True)
def main():
    app = App()
    app.mainloop()


if __name__ == '__main__':
    main()
