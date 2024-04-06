import time


class LevelTimer:
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.total_pause_time = 0
        self.pause_start_time = None

    def isRunning(self):
        return self.start_time is not None

    def start_level(self):
        if self.start_time is None:
            self.start_time = time.time()
        else:
            print('timer already started')

    def pause_level(self):
        self.pause_start_time = time.time()

    def resume_level(self):
        if self.pause_start_time is not None:
            self.total_pause_time += time.time() - self.pause_start_time
            self.pause_start_time = None

    def end_level(self):
        self.end_time = time.time()

    def get_elapsed_time(self):
        if self.start_time is not None and self.end_time is not None:
            elapsed_time = self.end_time - self.start_time - self.total_pause_time
            return elapsed_time
        else:
            return None

    def restart(self):
        self.start_time = time.time()
        self.end_time = None
        self.total_pause_time = 0
        self.pause_start_time = None
