import pyrebase
import json
from requests import HTTPError

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


def sign_up(email, password, username, onerror, onsuccess):
    try:
        user = auth.create_user_with_email_and_password(email, password)
        print(user)
    except HTTPError as e:
        data = json.loads(e.strerror)['error']
        match data['message']:
            case 'EMAIL_EXISTS':
                print("Sign up error: Email exists")
            case 'INVALID_EMAIL':
                print("Sign up error: Invalid email")
            case 'WEAK_PASSWORD : Password should be at least 6 characters':
                print('Sign up error: Weak password')
    except Exception:
        print("Виникла помилка")
    else:
        print("Успішно")


def sign_in(email, password, username, onerror, onsuccess):
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        print(user)
    except HTTPError as e:
        data = json.loads(e.strerror)['error']
        print(data)
        match data['message']:
            case 'INVALID_EMAIL':
                print("Sign in error: Invalid email")
            case 'INVALID_LOGIN_CREDENTIALS':
                print('Sign in error: Invalid data')
    except Exception:
        print("Виникла помилка")
    else:
        print("Успішно")
