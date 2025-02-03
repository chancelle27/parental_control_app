import time

class TimeUtils:
    @staticmethod
    def current_timestamp():
        return int(time.time())

    @staticmethod
    def seconds_to_hours(seconds):
        return seconds / 3600
