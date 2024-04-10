import i18n
import i18n_config
import firebase
from custom_dialogs import InfoDialog

APP_WIDTH = 1000
APP_HEIGHT = 640
ADMIN_EMAIL = 'arkanoid-admin@gmail.com'
LOCALES_PATH = 'locales'


def isAuth():
    return firebase.auth.current_user is not None


def isAdmin():
    if firebase.auth.current_user is None:
        return False
    return firebase.auth.current_user['email'] == ADMIN_EMAIL


def centered_window(window, width, height, title, resizable):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")
    window.title(title)
    window.resizable(resizable, resizable)


def list_to_dict(lst):
    return {str(index): value for index, value in enumerate(lst) if value is not None}
