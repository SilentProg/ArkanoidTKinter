import firebase


class Levels:
    def __init__(self, level_type: str):
        self.type = level_type
        self.db = firebase.db
        self.auth = firebase.auth
        self.uid = self.auth.current_user['localId']
        self.levels = None
        if self.type == 'community':
            self.levels = self.db.child('community-levels').order_by_child('public').equal_to(True).get()
        else:
            self.levels = self.db.child('levels').get()

        self.complete_levels = self.db.child('users-data').child(self.uid).child(
            f'completed-' + 'community-levels' if self.type == 'community' else 'levels').get()
        self._init_complete()

    def _init_complete(self):
        if self.levels.val() is None:
            return
        for level in self.levels.each():
            level.val()[
                'complete'] = True if self.complete_levels.val() and level.key() in self.complete_levels.val() else False

    def get_levels(self):
        return self.levels
