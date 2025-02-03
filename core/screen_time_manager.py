import time

class ScreenTimeManager:
    def __init__(self):
        self.start_time = None
        self.usage_limit = 3600  # Par défaut, 1 heure

    def start_session(self):
        self.start_time = time.time()

    def get_elapsed_time(self):
        if self.start_time:
            return time.time() - self.start_time
        return 0

    def is_limit_reached(self):
        return self.get_elapsed_time() >= self.usage_limit
