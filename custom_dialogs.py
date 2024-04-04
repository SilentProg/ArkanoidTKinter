import customtkinter as ctk
import i18n
import i18n_config


class PromptSwitchDialog(ctk.CTkToplevel):
    def __init__(self, options: {}, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app_width = 400
        self.app_height = 170
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        window_title = options.get('title', i18n.t('level-editor-title'))
        entry_prompt = options.get('entry_prompt', i18n.t('entry_prompt'))
        switch_prompt = options.get('switch_prompt', i18n.t('switch_prompt'))
        ok_text = options.get('ok_text', i18n.t('ok'))
        cancel_text = options.get('cancel_text', i18n.t('cancel'))

        x = (screen_width // 2) - (self.app_width // 2)
        y = (screen_height // 2) - (self.app_height // 2)

        self.geometry(f"{self.app_width}x{self.app_height}+{x}+{y}")
        self.title(window_title)
        self.resizable(False, False)

        self.var = ctk.StringVar()
        self.grab_set()

        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.pack(fill=ctk.BOTH, padx=5, pady=5)

        self.buttons_frame = ctk.CTkFrame(self)
        self.buttons_frame.pack(fill=ctk.BOTH, padx=5, pady=5)

        self.label = ctk.CTkLabel(self.content_frame, text=entry_prompt, justify="left")
        self.entry = ctk.CTkEntry(self.content_frame, textvariable=self.var)
        self.ok_button = ctk.CTkButton(self.buttons_frame, text=ok_text, command=self.on_ok)
        self.cancel_button = ctk.CTkButton(self.buttons_frame, text=cancel_text, command=self.on_cancel)
        self.switch_var = ctk.StringVar(value="off")
        self.switch = ctk.CTkSwitch(self.content_frame, text=switch_prompt, command=self.switch_event,
                                    variable=self.switch_var, onvalue="on", offvalue="off")

        self.label.pack(side="top", fill="x", padx=5, pady=5)
        self.entry.pack(side="top", fill="x", padx=5, pady=5)
        self.switch.pack(side="top", fill="x", padx=5, pady=5)
        self.ok_button.pack(side="right", padx=5, pady=5)
        self.cancel_button.pack(side="right", padx=5, pady=5)

        self.entry.bind("<Return>", self.on_ok)

    def switch_event(self):
        print("switch toggled, current value:", self.switch_var.get())

    def on_cancel(self, event=None):
        self.var.set('')
        self.switch_var.set('off')
        self.on_ok()

    def on_ok(self, event=None):
        self.destroy()

    def show(self):
        self.wm_deiconify()
        self.entry.focus_force()
        self.wait_window()
        return {'entry_value': None if self.var.get() == '' else self.var.get(),
                'switch_value': False if self.switch_var.get() == 'off' else True
                }


class InfoDialog(ctk.CTkToplevel):
    def __init__(self, options: {}, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app_width = 400
        self.app_height = 100
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        window_title = options.get('title', i18n.t('level-editor-title'))
        message = options.get('message', i18n.t('message'))
        ok_text = options.get('ok_text', i18n.t('ok'))

        x = (screen_width // 2) - (self.app_width // 2)
        y = (screen_height // 2) - (self.app_height // 2)

        self.geometry(f"{self.app_width}x{self.app_height}+{x}+{y}")
        self.title(window_title)
        self.resizable(False, False)

        self.var = ctk.StringVar()
        self.grab_set()

        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.pack(fill=ctk.BOTH, padx=5, pady=5)

        self.buttons_frame = ctk.CTkFrame(self)
        self.buttons_frame.pack(fill=ctk.BOTH, padx=5, pady=5)

        self.label = ctk.CTkLabel(self.content_frame, text=message, justify="left")

        self.ok_button = ctk.CTkButton(self.buttons_frame, text=ok_text, command=self.on_ok)
        self.label.pack(side="top", fill="x", padx=5, pady=5)
        self.ok_button.pack(side="right", padx=5, pady=5)

    def on_ok(self, event=None):
        self.destroy()

    def show(self):
        self.wm_deiconify()
        self.wait_window()
