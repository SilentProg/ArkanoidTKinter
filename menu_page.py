from functools import partial
from customtkinter import CTkFrame, CTkLabel, CTkFont, LEFT, X, BOTH, CTkButton
from constants import APP_WIDTH, APP_HEIGHT


class MenuPage(CTkFrame):
    top_frame: CTkFrame = None
    button_back: CTkButton = None
    error_frame: CTkFrame = None
    error_label: CTkLabel = None
    menu_label: CTkLabel = None
    on_back = lambda s: print(f'On back clicked')

    def __init__(self, master: any, title: str, show_back: bool, **kwargs):
        super().__init__(master, **kwargs)
        self.menu_frame_width = APP_WIDTH // 4
        self.menu_frame_height = APP_HEIGHT // 2
        self.configure(width=self.menu_frame_width, height=self.menu_frame_height)
        self.elements_width = self.winfo_reqwidth() - 40
        self.elements_height = 40
        self.title = title
        self.show_back = show_back
        self.button_font = CTkFont(family="Helvetica", size=14, weight="bold")
        self._init_components()

    def _init_components(self):
        if self.show_back:
            self.top_frame = CTkFrame(self, width=self.winfo_reqwidth())
            self.top_frame.pack(fill=X, padx=5, pady=5)

            self.button_back = CTkButton(self.top_frame, text="<-", width=25, command=partial(self.on_back))
            self.button_back.pack(side=LEFT, padx=10)

            self.menu_label = CTkLabel(self.top_frame, text=self.title,
                                       font=CTkFont(family="Helvetica", size=20, weight="bold"))
            self.menu_label.pack(fill=X, padx=20, pady=10)
        else:
            self.menu_label = CTkLabel(self, text=self.title,
                                       font=CTkFont(family="Helvetica", size=20, weight="bold"))
            self.menu_label.pack(padx=20, pady=10)

        self.error_frame = CTkFrame(master=self)

        self.error_label = CTkLabel(master=self.error_frame, text_color='red',
                                    justify=LEFT,
                                    font=CTkFont(family="Helvetica", weight="bold", size=14))
        self.error_label.pack(padx=5, pady=5)

        self.error_frame.pack(fill=X, padx=20, pady=5)
        self.error_frame.pack_forget()

    def show_result(self, message):
        self.error_label.configure(text_color='green')
        self.show_message(message)

    def show_message(self, message):
        self.error_frame.pack_forget()
        self.error_label.configure(text=message)
        if self.error_label.cget('text_color') != 'red' and self.error_label.cget('text_color') != 'green':
            self.error_label.configure(text_color='#dce4ee')
        if self.show_back:
            self.error_frame.pack(after=self.top_frame, fill=X, pady=5, padx=20)
        else:
            self.error_frame.pack(after=self.menu_label, fill=X, pady=5, padx=20)

    def set_on_back(self, func):
        self.on_back = func
        self.button_back.configure(command=partial(func))

    def show_error(self, message):
        self.error_label.configure(text_color='red')
        self.show_message(message)

    def show(self):
        x = APP_WIDTH / 2 - self.winfo_reqwidth() / 2
        y = APP_HEIGHT / 2 - self.winfo_reqheight() / 2
        self.place(x=x, y=y)
