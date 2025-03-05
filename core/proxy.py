import socketserver
from http.server import SimpleHTTPRequestHandler
from urllib.parse import urlparse
import json

BLOCKED_SITES_FILE = "blocked_sites.json"

# Charger la liste des sites bloqués
def load_blocked_sites():
    try:
        with open(BLOCKED_SITES_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

class ProxyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        blocked_sites = load_blocked_sites()
        parsed_url = urlparse(self.path)
        hostname = parsed_url.netloc
        
        if any(blocked in hostname for blocked in blocked_sites):
            self.send_response(403)
            self.end_headers()
            self.wfile.write(b"Access Denied: This site is blocked.")
            return
        
        super().do_GET()

if __name__ == "__main__":
    PORT = 8080
    with socketserver.TCPServer(("", PORT), ProxyHandler) as httpd:
        print(f"Proxy running on port {PORT}...")
        httpd.serve_forever()
