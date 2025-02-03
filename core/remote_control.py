import requests

class RemoteControl:
    def __init__(self, server_url):
        self.server_url = server_url

    def send_command(self, command):
        response = requests.post(f"{self.server_url}/command", json={"command": command})
        return response.json()
