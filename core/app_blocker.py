import psutil
import os

class AppBlocker:
    def __init__(self, blocked_apps_file):
        self.blocked_apps_file = blocked_apps_file

    def block_apps(self):
        with open(self.blocked_apps_file, "r") as file:
            blocked_apps = [app.strip() for app in file.readlines()]

        for process in psutil.process_iter(['name']):
            if process.info['name'] in blocked_apps:
                os.system(f"taskkill /F /IM {process.info['name']}")

    def is_blocked(self, app_name):
        with open(self.blocked_apps_file, "r") as file:
            return app_name.strip() in file.read()
