import socket

class NetworkUtils:
    @staticmethod
    def is_site_blocked(site):
        try:
            socket.gethostbyname(site)
            return False
        except socket.gaierror:
            return True
