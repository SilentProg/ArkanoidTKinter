import firebase

# Клас Рівнів
class Levels:
    def __init__(self, level_type: str):
        self.type = level_type  # Тип рівнів
        self.db = firebase.db  # Отримуємо посилання на БД
        self.auth = firebase.auth  # Отримуємо посилання на сервіс авторизації
        self.uid = self.auth.current_user['localId']  # отримуємо Id поточного гравця
        self.levels = None  # ініціалізовуємо зміну рівнів
        # Отримуємо рівні згідно отриманого типу
        if self.type == 'community':
            self.levels = self.db.child('community-levels').order_by_child('public').equal_to(True).get()
        else:
            self.levels = self.db.child('levels').get()
        # Отримуємо завершені рівні гравця
        self.complete_levels = self.db.child('users-data').child(self.uid).child(f'completed-' + ('community-levels' if self.type == 'community' else 'levels')).shallow().get()
        # Ініціалізовуємо пройдені рівні
        self._init_complete()

    def _init_complete(self):
        print('complete levels')
        if self.levels.val() is None:
            return
        for level in self.levels.each():
            level.val()[
                'complete'] = True if self.complete_levels.val() and level.key() in self.complete_levels.val() else False
            print(level.val())

    def get_levels(self):
        return self.levels
