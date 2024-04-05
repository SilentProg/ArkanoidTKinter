import i18n
import i18n_config
import firebase
from custom_dialogs import InfoDialog

APP_WIDTH = 1000
APP_HEIGHT = 640
ADMIN_EMAIL = 'arkanoid-admin@gmail.com'


def isAuth():
    return firebase.auth.current_user is not None


def isAdmin():
    if firebase.auth.current_user is None:
        return False
    return firebase.auth.current_user['email'] == ADMIN_EMAIL
