import pyrebase
import json
from requests import HTTPError
import i18n
import i18n_config

firebase_config = {
    'apiKey': "AIzaSyBdTCFLpvIKzfEd5d9ReCZiR5Iqi0_dcwA",
    'authDomain': "arkanoid-dp.firebaseapp.com",
    'projectId': "arkanoid-dp",
    'storageBucket': "arkanoid-dp.appspot.com",
    'databaseURL': "https://arkanoid-dp-default-rtdb.europe-west1.firebasedatabase.app/",
    'messagingSenderId': "34979024552",
    'appId': "1:34979024552:web:83df42d0a395cd8234fc9d"
}

firebaseApp = pyrebase.initialize_app(firebase_config)

db = firebaseApp.database()
storage = firebaseApp.storage()
auth = firebaseApp.auth()


def sign_up(email, password, username, onerror=lambda e: print(e), onsuccess=lambda user: print(user)):
    try:
        user = auth.create_user_with_email_and_password(email, password)
        auth.update_profile(id_token=user['idToken'], display_name=username)
    except HTTPError as e:
        onerror(i18n.t(json.loads(e.strerror)['error']['message']))
    except Exception as e:
        onerror(i18n.t('ERROR') + "\t" + str(e))
    else:
        onsuccess(user)


def sign_in(email, password, onerror=lambda e: print(e), onsuccess=lambda user: print(user)):
    try:
        user = auth.sign_in_with_email_and_password(email, password)
    except HTTPError as e:
        onerror(i18n.t(json.loads(e.strerror)['error']['message']))
    except Exception as e:
        onerror(i18n.t('ERROR') + "\t" + str(e))
    else:
        onsuccess(user)


def restore_password(email: str, onerror=lambda e: print(e), onsuccess=lambda r: print(r)):
    try:
        result = auth.send_password_reset_email(email)
    except HTTPError as e:
        onerror(i18n.t(json.loads(e.strerror)['error']['message']))
    except Exception as e:
        onerror(i18n.t('ERROR') + "\t" + str(e))
    else:
        onsuccess(result)

# sign_up('nice.savonik@gmail.com', 'gavno228', 'Silent')
# sign_in('nice.savonik@gmail.com', 'gavno228')
# restore_password('nice.savonik@gmail.com')
